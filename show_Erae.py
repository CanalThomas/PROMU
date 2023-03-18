import json
import matplotlib.pyplot as plt
import numpy as np


def load_Erae_data():
    with open("records/XYat.json", "r") as f:
        XYat = json.load(f)
        np_XYat = np.array(XYat)

    X, Y, alpha, time_stroke = np_XYat[:, 0], np_XYat[:, 1], np_XYat[:, 2], np_XYat[:, 3]

    return X, Y, alpha, time_stroke


def main():
    X, Y, alpha, _ = load_Erae_data()

    plt.figure(num="Show Erae")
    plt.axvline(x=64, color="#888888", linestyle=":", alpha=.4)
    plt.axhline(y=64, color="#888888", linestyle=":", alpha=.4)
    plt.scatter(X, Y, color="#63AA29", alpha=alpha, edgecolors="none")
    plt.xlim(0, 128)
    plt.ylim(0, 128)
    plt.xticks([])
    plt.yticks([])
    plt.title("Représentation de là où on tape et si c'est fort")
    plt.show()


if __name__ == "__main__":
    main()
