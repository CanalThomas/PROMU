import matplotlib.pyplot as plt
from process_midi import measure_loss
from tqdm import trange
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


d = {
    "velocity": 0, # velocity of the stroke
    "60": 64, # X - Erae
    "61": 64, # Y - Erae
    "48": 64, # sustain
    "49": 64, # damp
    "50": 64, # inharmonicity
    "51": 64, # squareness
    "15": 64, # pitch
}


d_target = {
    "velocity": 0, # velocity of the stroke
    "60": 64, # X - Erae
    "61": 64, # Y - Erae
    "48": 64, # sustain
    "49": 64, # damp
    "50": 64, # inharmonicity
    "51": 64, # squareness
    "15": 64, # pitch
}


def main():
    T = list(range(0, 128, 8))
    L = []
    for midi_value in trange(0, 128, 8):
        d["50"] = midi_value
        loss = measure_loss(d, d_target)
        L.append(loss)
    plt.step(T, L)
    plt.show()


if __name__ == "__main__":
    main()
