import mido
import time
import matplotlib.pyplot as plt

open_ports = mido.get_input_names()

Akai_index = open_ports.index("Akai APC40 0")

start_time = time.time()
messages = []

def process_Akai(arg: mido.messages.messages.Message):
    current_time = time.time()
    if arg.type == "control_change" and arg.control in [48, 49, 50, 51, 52, 53, 54, 55, 15]:
        message = {
            "controller": "Akai",
            "control": arg.control,
            "value": arg.value,
            "time": current_time - start_time,
        }
        messages.append(message)

port_Akai = mido.open_input(open_ports[Akai_index], callback=process_Akai)
input("Press Enter to stop recording...")
port_Akai.close()

import json

with open("Akai_data.json", "w") as f:
    json.dump(messages, f)