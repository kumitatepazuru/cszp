import subprocess

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_hist(d, c):
    if max(d) - min(d) != 0:
        d.hist(alpha=0.4, bins=max(d), color=c)
    else:
        d.hist(alpha=0.4, color=c)


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
    plt.savefig("file1.png", dpi=600)

    csv = open(filename)
    csv2 = open("html.csv", "w")
    csvd = csv.read().splitlines()[1:]
    csvtd = []
    for i in csvd:
        csvtd.append(i.split(","))
    csvd = ""
    for i in csvtd:
        for j in range(len(i)):
            if j != 0:
                if j != len(i)-1:
                    csvd += i[j]+","
                else:
                    csvd += i[j] + "\n"
    csv2.write("プレイヤー1,プレイヤー２," + data["team1"][0] + "の得点," + data["team2"][0] + "の得点," + data["team1"][0] + "の得失点差," +
               data["team2"][0] + "の得失点差\n" + csvd)
    csv.close()
    csv2.close()
    # print(filename)
    return filename


def logs(time):
    subprocess.check_call("mkdir ./html_logs/" + time, shell=True)
    subprocess.check_call("mv ./html.csv ./html_logs/" + time + "/", shell=True)
    subprocess.check_call("mv ./file1.png ./html_logs/" + time + "/", shell=True)
    subprocess.check_call("cp ./index.html ./html_logs/" + time + "/", shell=True)
