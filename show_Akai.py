import json
import matplotlib.pyplot as plt
import numpy as np

from typing import Dict


def load_Akai_data():
    with open("records/Akai_data.json", "r") as f:
        Akai_data = json.load(f)
    return Akai_data


def load_target() -> Dict[str, int]:
    with open("records/target.json", "r") as f:
        d_target = json.load(f)
    return d_target


def main():
    Akai_data = load_Akai_data()
    d_target = load_target()

    # data_dict will have the following shape:
    # {
    #   control_0: [(time_0_0, value_0_0), (time_0_1, value_0_1), ...],
    #   control_1: [(time_1_0, value_1_0), (time_1_1, value_1_1), ...],
    #   ...
    # }
    data_dict = {}

    map_controller = {
        48: "Sustain",
        49: "Damp",
        50: "Inharmonicity",
        51: "Squareness",
        15: "Pitch",
    }

    map_colors = {
        48: "#002AFF",
        49: "#7BFF00",
        50: "#FF6600",
        51: "#00FF99",
        15: "#E500FF",
    }

    for elem in Akai_data:
        control = elem["control"]
        time = elem["time"]
        value = elem["value"]
        data_dict.setdefault(control, []).append((time, value))

    plt.figure(num="Show Akai")
    for control, item in data_dict.items():
        np_item = np.array(item)
        plt.step(np_item[:, 0], np_item[:, 1], label=map_controller[control], color=map_colors[control])
    
    for control, item in d_target.items():
        if control in ["48", "49", "50", "51", "15"]:
            plt.axhline(y=item, color=map_colors[int(control)], linestyle=":", alpha=.4)

    plt.xlabel("Temps (s)")
    plt.ylabel("Valeur MIDI")
    plt.legend(loc="upper left")
    plt.title("Changement des valeurs de chaque potard en fonction du temps")
    plt.show()


if __name__ == "__main__":
    main()
