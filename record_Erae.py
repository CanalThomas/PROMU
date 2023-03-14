import mido
import time
import matplotlib.pyplot as plt

open_ports = mido.get_input_names()

Erae_index = open_ports.index("Erae Touch 0")
# print(Erae_index)

record_time = 5.0  # seconds
start_time = time.time()
messages = []

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
            messages.append(message)
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
            messages.append(message)
        case _:
            pass

port_Erae = mido.open_input(open_ports[Erae_index], callback=process_Erae)
# portB = mido.open_input(open_ports[1], callback=do_whatever)
# portC = mido.open_input(open_ports[2], callback=do_whateverB)
# portD = mido.open_input(open_ports[3], callback=do_whatever)
# time.sleep(record_time)
input("Press Enter to stop recording...")
# portD.close()
# portC.close()
# portB.close()
port_Erae.close()

X, Y = [], []
# iteration sur les impacts ("note_on")
for mess in filter(lambda d: d["controller"] == "Erae" and d["type"] == "note_on", messages):
    print(mess)
    # on prend les changements de contrôle qui suivent ("control_change")
    first_X = next(filter(lambda d: d["controller"] == "Erae" and d["type"] == "control_change" and d["control"] == 60 and d["time"] >= mess["time"], messages))
    first_Y = next(filter(lambda d: d["controller"] == "Erae" and d["type"] == "control_change" and d["control"] == 61 and d["time"] >= mess["time"], messages))
    X.append(first_X["value"])
    Y.append(first_Y["value"])

print(len(X), len(Y))

import json

with open("X.json", "w") as f:
    json.dump(X, f)

with open("Y.json", "w") as g:
    json.dump(Y, g)

# fig, ax = plt.subplots()
# ax.set_xlim(0, 128)
# ax.set_ylim(0, 128)
# ax.scatter(X, Y)
# fig.show()