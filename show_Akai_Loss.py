import matplotlib.pyplot as plt


def main_akai(ax: plt.Axes):
    from show_Akai import sub_main_Akai
    sub_main_Akai(ax)


def main_loss(ax: plt.Axes):
    from show_Loss import sub_main_Loss
    time, loss = sub_main_Loss()
    ax.step(time, loss, label="Loss", color="grey")
    ax.legend(loc="center left")


if __name__ == "__main__":
    fig, ax1 = plt.subplots()
    plt.get_current_fig_manager().set_window_title("Show Akai and Loss")
    main_akai(ax1)
    ax2 = ax1.twinx()
    main_loss(ax2)
    fig.tight_layout()
    plt.show()
