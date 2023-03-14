import json
import matplotlib.pyplot as plt


def load_Erae_data():
    with open("X.json", "r") as f:
        X = json.load(f)

    with open("Y.json", "r") as g:
        Y = json.load(g)

    return X, Y


def main():
    X, Y = load_Erae_data()

    plt.figure(num="Show Erae")
    plt.axvline(x=64, color="#888888", linestyle=":", alpha=.4)
    plt.axhline(y=64, color="#888888", linestyle=":", alpha=.4)
    plt.scatter(X, Y, color="#63AA29", alpha=0.5, edgecolors="none")
    plt.xlim(0, 128)
    plt.ylim(0, 128)
    plt.xticks([])
    plt.yticks([])
    plt.title("Représentation de là où on tape")
    plt.show()


if __name__ == "__main__":
    main()
