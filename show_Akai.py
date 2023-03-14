import json
import matplotlib.pyplot as plt
import numpy as np

with open("Akai_data.json", "r") as f:
    Akai_data = json.load(f)

# data_dict will have the following shape:
# {
#   control_0: [(time_0_0, value_0_0), (time_0_1, value_0_1), ...],
#   control_1: [(time_1_0, value_1_0), (time_1_1, value_1_1), ...],
#   ...
# }
data_dict = {}

for elem in Akai_data:
    control = elem["control"]
    time = elem["time"]
    value = elem["value"]
    data_dict.setdefault(control, []).append((time, value))

for control, item in data_dict.items():
    np_item = np.array(item)
    plt.plot(np_item[:, 0], np_item[:, 1], label=control)

plt.legend(loc="upper right")
plt.title("Changement des valeurs de chaque potard en fonction du temps")
plt.show()