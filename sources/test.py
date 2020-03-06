import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_socre(filename):
    data = pd.read_csv(filename, sep=',', header=None,
                       names=('date', 'team1', 'team2', 'team1_score', 'team2_score', 'toku1', "toku2"),
                       index_col=0)
    # print(data["team1_score"])
    x = np.array(range(len(data["team1_score"])))
    y = np.array(data["team1_score"])
    plt.bar(x - 0.15, y, align="center", alpha=0.7, color="g", width=0.3, label=data["team1"].values[0])

    x = np.array(range(len(data["team2_score"])))
    y = np.array(data["team2_score"])
    plt.bar(x + 0.15, y, align="center", alpha=0.7, color="b", width=0.3, label=data["team2"].values[0])

    plt.xlabel("point")
    plt.xlabel("number of times")
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


plot_socre("10_1.csv")
