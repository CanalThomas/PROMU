import json
import matplotlib.pyplot as plt
import numpy as np


def load_Akai_data():
    with open("records/Akai_data.json", "r") as f:
        Akai_data = json.load(f)
    return Akai_data


def main():
    Akai_data = load_Akai_data()

    # data_dict will have the following shape:
    # {
    #   control_0: [(time_0_0, value_0_0), (time_0_1, value_0_1), ...],
    #   control_1: [(time_1_0, value_1_0), (time_1_1, value_1_1), ...],
    #   ...
    # }
    data_dict = {}

    map_controller = {
        48: "1",
        49: "2",
        50: "3",
        51: "4",
        52: "5",
        53: "6",
        54: "7",
        55: "8",
        15: "slider",
    }

    for elem in Akai_data:
        control = elem["control"]
        time = elem["time"]
        value = elem["value"]
        data_dict.setdefault(control, []).append((time, value))

    plt.figure(num="Show Akai")
    for control, item in data_dict.items():
        np_item = np.array(item)
        plt.plot(np_item[:, 0], np_item[:, 1], label=map_controller[control])

    plt.xlabel("Temps (s)")
    plt.ylabel("Valeur MIDI")
    plt.legend(loc="upper right")
    plt.title("Changement des valeurs de chaque potard en fonction du temps")
    plt.show()


if __name__ == "__main__":
    main()
