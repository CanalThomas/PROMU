import mido
import time


open_ports = mido.get_input_names()
Erae_indexes = [open_ports.index(l) for l in open_ports if l.startswith("Erae Touch")]
Akai_indexes = [open_ports.index(l) for l in open_ports if l.startswith("Akai APC40")]

assert Erae_indexes != [], "Erae Touch is not plugged in"
assert Akai_indexes != [], "Akai APC40 is not plugged in"

Erae_index = Erae_indexes[0]
Akai_index = Akai_indexes[0]

start_time = time.time()
messages_Akai, message_Erae = [], []

def process_Erae(arg: mido.messages.messages.Message):
    current_time = time.time()
    match arg.type:
        case "note_on":
            message = {
                "controller": "Erae",
                "type": arg.type,
                # "channel": arg.channel,
                # "note": arg.note,
                # "velocity": arg.velocity,
                "time": current_time - start_time,
                # "arg": arg,
            }
            message_Erae.append(message)
        case "control_change":
            message = {
                "controller": "Erae",
                "type": arg.type,
                # "channel": arg.channel,
                "control": arg.control,
                "value": arg.value,
                "time": current_time - start_time,
                # "arg": arg,
            }
            message_Erae.append(message)
        case _:
            pass

def process_Akai(arg: mido.messages.messages.Message):
    current_time = time.time()
    if arg.type == "control_change" and arg.control in [48, 49, 50, 51, 52, 53, 54, 55, 15]:
        message = {
            "controller": "Akai",
            "control": arg.control,
            "value": arg.value,
            "time": current_time - start_time,
        }
        messages_Akai.append(message)

port_Erae = mido.open_input(open_ports[Erae_index], callback=process_Erae)
port_Akai = mido.open_input(open_ports[Akai_index], callback=process_Akai)
input("Press Enter to stop recording...")
port_Akai.close()
port_Erae.close()

X, Y = [], []
# iteration sur les impacts ("note_on")
for mess in filter(lambda d: d["controller"] == "Erae" and d["type"] == "note_on", message_Erae):
    # on prend les changements de contrôle qui suivent ("control_change")
    first_X = next(filter(lambda d: d["controller"] == "Erae" and d["type"] == "control_change" and d["control"] == 60 and d["time"] >= mess["time"], message_Erae))
    first_Y = next(filter(lambda d: d["controller"] == "Erae" and d["type"] == "control_change" and d["control"] == 61 and d["time"] >= mess["time"], message_Erae))
    X.append(first_X["value"])
    Y.append(first_Y["value"])

import json

with open("X.json", "w") as f:
    json.dump(X, f)

with open("Y.json", "w") as g:
    json.dump(Y, g)

with open("Akai_data.json", "w") as f:
    json.dump(messages_Akai, f)
