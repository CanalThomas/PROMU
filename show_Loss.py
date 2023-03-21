import matplotlib.pyplot as plt
import numpy as np
import json
import auraloss
from show_Akai import load_Akai_data
from show_Erae import load_Erae_data
from process_midi import measure_loss
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from typing import List, Dict


def select_midi(data: List[Dict[str, str | int | float]], time: float, channel: int, target: int) -> int:
    for event in data:
        if event["control"] == channel and event["time"] >= time:
            return event["value"]

    return target


def load_data():
    """
    This function loads Akai, Erae Touch data of the experiment.
    It loads target values.
    Then it creates arrays of all parameters of both devices when a "note-on" event occurs on the Erae Touch.
    Then it computes the loss between the soundwave resulting from the latter parameters and the target soundwave.

    Outputs:
    (
        list[float], # time of each stroke
        list[float], # loss value at each time
    )
    """
    Akai_data = load_Akai_data()
    X, Y, alpha, times_strokes = load_Erae_data()

    with open("records/target.json", "r") as f:
        d_target = json.load(f)

    mrstft = auraloss.freq.MultiResolutionSTFTLoss()

    time = []
    loss = []

    first_time_stroke = times_strokes[0]

    for x, y, velocity, time_stroke in zip(X, Y, alpha, times_strokes):
        d = {}
        d["velocity"] = velocity
        d["60"] = x
        d["61"] = y
        for midi_channel in ["48", "49", "50", "51", "15"]:
            d[midi_channel] = select_midi(Akai_data, time_stroke, midi_channel, d_target[midi_channel])
        loss_stroke = measure_loss(d, d_target, mrstft)

        time.append(time_stroke - first_time_stroke)
        loss.append(loss_stroke)

    return time, loss


def main():
    time, loss = load_data()
    plt.figure(num="Show Loss")
    plt.plot(time, loss)
    plt.title("MultiResolutionSTFTLoss := f(time)")
    plt.show()


if __name__ == "__main__":
    main()
