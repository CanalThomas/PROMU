import matplotlib.pyplot as plt
import numpy as np


def main_akai(ax: plt.Axes, first_time_stroke: float):
    from show_Akai import sub_main_Akai
    sub_main_Akai(ax, first_time_stroke)


def main_loss(ax: plt.Axes):
    from show_Loss import sub_main_Loss
    time, loss = sub_main_Loss()
    first_time_stroke = time[0]
    time_shifted = time - first_time_stroke * np.ones_like(time)

    ax.step(time_shifted, loss, label="Loss", color="grey", where="post")
    for t, l in zip(time_shifted, loss):
        if l == 0:
            ax.scatter(t, 0, marker='x', color="green")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Loss value")
    ax.legend(loc="center left")
    
    return first_time_stroke


if __name__ == "__main__":
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    plt.get_current_fig_manager().set_window_title("Show Akai and Loss")
    first_time_stroke = main_loss(ax2)
    print(first_time_stroke)
    main_akai(ax1, first_time_stroke)
    fig.tight_layout()
    plt.show()
