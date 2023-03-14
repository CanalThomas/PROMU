import json
import matplotlib.pyplot as plt
import numpy as np


def load_Erae_data():
    with open("records/XYa.json", "r") as f:
        XYa = json.load(f)
        np_XYa = np.array(XYa)

    X, Y, alpha = np_XYa[:, 0], np_XYa[:, 1], np_XYa[:, 2]

    return X, Y, alpha


def main():
    X, Y, alpha = load_Erae_data()

    plt.figure(num="Show Erae")
    plt.axvline(x=64, color="#888888", linestyle=":", alpha=.4)
    plt.axhline(y=64, color="#888888", linestyle=":", alpha=.4)
    plt.scatter(X, Y, color="#63AA29", alpha=alpha, edgecolors="none")
    plt.xlim(0, 128)
    plt.ylim(0, 128)
    plt.xticks([])
    plt.yticks([])
    plt.title("Représentation de là où on tape")
    plt.show()


if __name__ == "__main__":
    main()
