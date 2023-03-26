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


def process_data():
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

    return data_dict, map_controller, map_colors, d_target


def sub_main_Akai(ax: plt.Axes, first_time_stroke: float = 0):
    data_dict, map_controller, map_colors, d_target = process_data()

    for control, item in data_dict.items():
        np_item = np.array(item)
        ax.step(np_item[:, 0] - first_time_stroke, np_item[:, 1], label=map_controller[control], color=map_colors[control])
    
    for control, item in d_target.items():
        if control in ["48", "49", "50", "51", "15"]:
            ax.axhline(y=item, color=map_colors[int(control)], linestyle=":", alpha=.4)

    ax.set_ylabel("MIDI value")
    ax.legend(loc="upper left")


def main():
    _, ax1 = plt.subplots()
    plt.get_current_fig_manager().set_window_title("Show Akai")
    sub_main_Akai(ax1)
    ax1.set_title("Changement des valeurs de chaque potard en fonction du temps")
    plt.show()


if __name__ == "__main__":
    main()
