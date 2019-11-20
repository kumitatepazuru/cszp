import matplotlib.pyplot as plt
import pandas as pd
import subprocess


def plot_hist(d):
    if max(d) - min(d) != 0:
        d.hist(bins=max(d) - min(d), alpha=0.5)
    else:
        d.hist(alpha=0.5)


def plot_socre(filename):
    data = pd.read_csv(filename, sep=',', header=None, names=('date', 'team1', 'team2', 'team1_score', 'team2_score'),
                       index_col=0)
    # print(data)
    plot_hist(data['team1_score'])
    plot_hist(data['team2_score'])
    # plt.show()
    plt.savefig("file.png")

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
    csv2.write("プレイヤー1,プレイヤー２,プレイヤー1の得点,プレイヤー2の得点\n" + csvd)
    csv.close()
    csv2.close()
    # print(filename)
    return filename


def logs(time):
    subprocess.check_call("mkdir ./html_logs/" + time, shell=True)
    subprocess.check_call("mv ./html.csv ./html_logs/" + time + "/", shell=True)
    subprocess.check_call("mv ./file.png ./html_logs/" + time + "/", shell=True)
    subprocess.check_call("cp ./index.html ./html_logs/" + time + "/", shell=True)
