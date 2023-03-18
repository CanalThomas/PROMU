import mido
import time
import warnings
import os
import json

import process_midi


open_ports = mido.get_input_names()
Erae_indexes = [open_ports.index(l) for l in open_ports if l.startswith("Erae Touch")]
Akai_indexes = [open_ports.index(l) for l in open_ports if l.startswith("Akai APC40")]

assert Erae_indexes != [], "Erae Touch is not plugged in"
assert Akai_indexes != [], "Akai APC40 is not plugged in"

Erae_index = Erae_indexes[0]
Akai_index = Akai_indexes[0]

target_parameters = {
    "velocity": 0, # velocity of the stroke
    60: 64, # X - Erae
    61: 64, # Y - Erae
    48: 64, # sustain
    49: 64, # damp
    50: 64, # inharmonicity
    51: 64, # squareness
    15: 64, # pitch
}

global_parameters = {
    "velocity": 0, # velocity of the stroke
    60: 64, # X - Erae
    61: 64, # Y - Erae
    48: 64, # sustain
    49: 64, # damp
    50: 64, # inharmonicity
    51: 64, # squareness
    15: 64, # pitch
}

first_time = True
start_time = time.time()
messages_Akai, message_Erae = [], []

def process_Erae(arg: mido.messages.messages.Message):
    current_time = time.time()

    match arg.type:
        case "note_on":
            if first_time:
                start_time = current_time
                first_time = False
            message = {
                "controller": "Erae",
                "type": arg.type,
                "velocity": arg.velocity,
                "time": current_time - start_time,
            }
            message_Erae.append(message)
            global_parameters["velocity"] = arg.velocity
        case "control_change":
            if not first_time:
                message = {
                    "controller": "Erae",
                    "type": arg.type,
                    "control": arg.control,
                    "value": arg.value,
                    "time": current_time - start_time,
                }
                message_Erae.append(message)
                global_parameters[arg.control] = arg.value
        case _:
            pass

def process_Akai(arg: mido.messages.messages.Message):
    if first_time:
        if arg.type == "control_change" and arg.control in [48, 49, 50, 51, 15]:
            global_parameters[arg.control] = arg.value
    else:
        current_time = time.time()
        if arg.type == "control_change" and arg.control in [48, 49, 50, 51, 15]:
            message = {
                "controller": "Akai",
                "control": arg.control,
                "value": arg.value,
                "time": current_time - start_time,
            }
            messages_Akai.append(message)
            global_parameters[arg.control] = arg.value

port_Erae = mido.open_input(open_ports[Erae_index], callback=process_Erae)
port_Akai = mido.open_input(open_ports[Akai_index], callback=process_Akai)
input("Press Enter to stop recording...")
port_Akai.close()
port_Erae.close()

def transform(x):
    if x <= 64:
        y = 0.003125 * x # 0.003125 = 0.2 / 64
    else:
        y = 0.0125 * x - 0.6 # 0.0125 = 0.8 / 64
    if y < 0 or y > 1:
        warnings.warn("Transformed velocity value not in [0, 1]", RuntimeWarning)
    return y

XYat = []
# iteration sur les impacts ("note_on")
for mess in filter(lambda d: d["controller"] == "Erae" and d["type"] == "note_on", message_Erae):
    velocity = transform(mess["velocity"])

    # on prend les changements de contrôle qui suivent ("control_change")
    X = next(filter(lambda d: d["controller"] == "Erae" and d["type"] == "control_change" and d["control"] == 60 and d["time"] >= mess["time"], message_Erae))
    Y = next(filter(lambda d: d["controller"] == "Erae" and d["type"] == "control_change" and d["control"] == 61 and d["time"] >= mess["time"], message_Erae))
    
    time_stroke = max(mess["time"], X["time"], Y["time"])
    
    XYat.append((X["value"], Y["value"], velocity, time_stroke))

os.makedirs("records", exist_ok=True)

with open("records/XYat.json", "w") as f:
    json.dump(XYat, f)

with open("records/Akai_data.json", "w") as g:
    json.dump(messages_Akai, g)

with open("records/target.json", "w") as h:
    json.dump(target_parameters, h)
