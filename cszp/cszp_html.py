import subprocess

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_socre(filename):
    data = pd.read_csv("./csvdata/" + filename, sep=',', header=None,
                       names=('date', 'team1', 'team2', 'team1_score', 'team2_score', 'toku1', "toku2"),
                       index_col=0)
    heikin = data.mean()
    x = np.array(range(max(max(data["team1_score"]), max(data["team2_score"])) + 1))
    y = np.array([0] * (max(max(data["team1_score"]), max(data["team2_score"])) + 1))
    for i in data["team1_score"]:
        y[i] += 1
    plt.bar(x - 0.15, y, color="y", width=0.3,
            label=data["team1"].values[0] + "\nAverage:" + str(np.round(heikin["team1_score"], decimals=2)))

    x = np.array(range(max(max(data["team1_score"]), max(data["team2_score"])) + 1))
    y = np.array([0] * (max(max(data["team1_score"]), max(data["team2_score"])) + 1))
    for i in data["team2_score"]:
        y[i] += 1
    plt.bar(x + 0.15, y, color="r", width=0.3,
            label=data["team2"].values[0] + "\nAverage:" + str(np.round(heikin["team2_score"], decimals=2)))
    plt.ylabel("number of times")
    plt.xlabel("point")
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig("file1.png", dpi=300)
    plt.clf()

    csv = open("./csvdata/" + filename)
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
