import csv
import os
import shutil
import socketserver
import subprocess
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from io import StringIO, BytesIO

import cuitools
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from prompt_toolkit.shortcuts import yes_no_dialog
from texttable import Texttable

from cszp import cszp_log
from cszp import cszp_module
from cszp.cszp_module import figlet, Input

matplotlib.use('Agg')


class soccerHTTPServer_Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            try:
                with open("./html/index.html") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            except FileNotFoundError as e:
                print("\t\033[38;5;3m[WARNING]", e)
                self.wfile.write("404 Not Found!".encode("utf-8"))

        elif self.path == "/html.csv":
            if result != "":
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.end_headers()
                bs = StringIO(result)
                data = pd.DataFrame(list(csv.reader(bs))[1:],
                                    columns=('date', 'team1', 'team2', 'team1_score', 'team2_score', 'toku1', "toku2"))
                data = data.set_index('date')
                # print(data)
                csvd = result.splitlines()[1:]
                csvtd = []
                for i in csvd:
                    csvtd.append(i.split(","))
                csvd = ""
                for i in csvtd:
                    for j in range(len(i)):
                        if j != 0:
                            if j != len(i) - 1:
                                csvd += i[j] + ","
                            else:
                                csvd += i[j] + "\n"
                self.wfile.write(
                    ("プレイヤー1,プレイヤー２," + data["team1"][0] + "の得点," + data["team2"][0] + "の得点," + data["team1"][
                        0] + "の得失点差," +
                     data["team2"][0] + "の得失点差\n" + csvd).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        elif self.path == "/file1.png":
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
            if result != "":
                bs = StringIO(result)
                data = pd.DataFrame(list(csv.reader(bs))[1:],
                                    columns=('date', 'team1', 'team2', 'team1_score', 'team2_score', 'toku1', "toku2"))
                data["team1_score"] = data["team1_score"].astype(int)
                data["team2_score"] = data["team2_score"].astype(int)
                # print(result)
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
                img = BytesIO()
                plt.savefig(img, dpi=300, format="png")
                plt.clf()
                self.wfile.write(img.getvalue())
            else:
                self.wfile.write(open("./html/nofile.png", "rb").read())
        elif self.path == "/load.gif":
            self.send_response(200)
            self.send_header("Content-Type", "image/gif")
            self.end_headers()
            self.wfile.write(open("./html/load.gif", "rb").read())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write("404 Not Found!".encode("utf-8"))


def totime(sec):
    return "{0.days}d {0.hours}h {0.minutes}m {0.seconds}s".format(relativedelta(seconds=sec))


class soccer:
    def server(self):
        PORT = 20000
        Handler = soccerHTTPServer_Handler
        try:
            socketserver.TCPServer.allow_reuse_address = True
            self.httpd = socketserver.ThreadingTCPServer(("", PORT), Handler)
            print("\t\033[38;5;10m\033[1m[OK]\033[0mThe web server has been started. Port:", PORT)
            self.httpd.serve_forever()
        except OSError as e:
            print("\t\033[38;5;3m[WARNING]\033[0mCould not start web server port", PORT, ":" + str(e))
            time.sleep(5)
            self.server()

    def __init__(self, cmd, lang, loop, module, logs2, Input, s_start, reset=True, exit=True):
        global result
        result = ""
        self.result_list = []
        if reset:
            cuitools.reset()

        sc = "rcssserver " + cmd[2]
        wc = "soccerwindow2 > /dev/null 2>&1"
        if logs2[3]:
            sc += " server::synch_mode=true"
        print("\t\033[1m\033[38;5;172m" + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        print("\033[38;5;2mTeam1-CMD : " + cmd[0])
        print("Team2-CMD : " + cmd[1])
        print("\033[38;5;2mSERVER-CMD : " + sc)
        print("WINDOW-CMD : " + wc + "\033[0m")
        error = 0
        list_time = []
        if loop > 1 and s_start:
            server = threading.Thread(target=self.server)
            server.setDaemon(True)
            server.start()

        try:
            for i in range(loop):
                print("\t\033[38;5;4m[INFO]\033[0mLOOP:", i + 1, "/", loop)
                tmp_time = time.time()
                logs = "\t" + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\n" + "SERVER-CMD : " + sc + "\n"
                logt1 = "\t" + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\n"
                logt2 = "\t" + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\n"
                cszp_module.killsoccer()

                data = module.Open("./config/config.conf")
                datas = data.read().splitlines()[0]
                data.close()
                datas = datas.split(",")

                if datas[1] == "on":
                    try:
                        subprocess.Popen(wc, shell=True)
                    except subprocess.CalledProcessError as e:
                        print("\033[38;5;3m[WARNING]\033[0m" + "SOCCERWINDOW2_ERROR" + str(e))

                try:
                    logtemp1 = subprocess.Popen(sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print("\t\033[38;5;4m[INFO]\033[0mrcssserver start.")
                    logtemp2 = subprocess.Popen(cmd[0], shell=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                    print("\t\033[38;5;4m[INFO]\033[0mteam1 start.")
                    time.sleep(1)
                    logtemp3 = subprocess.Popen(cmd[1], shell=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                    print("\t\033[38;5;4m[INFO]\033[0mteam2 start.")
                    stdout, stderr = logtemp2.communicate()
                    try:
                        stderr = stderr.decode("utf-8")
                        stdout = stdout.decode("utf-8")
                    except UnicodeDecodeError as e:
                        print("\033[38;5;3m[WARNING]\033[0m\t" + str(e))
                        stderr = stderr.decode("utf-8", "replace")
                        stdout = stdout.decode("utf-8", "replace")
                    logt1 += stdout + stderr
                    logt1 += "\n"
                    print("\t\033[38;5;4m[INFO]\033[0mreturncode:" + str(logtemp2.returncode))
                    if logtemp2.returncode != 0:
                        logtemp3.kill()
                        logtemp1.kill()
                        print("\t\033[38;5;9m\033[1m[ERR]\033[0m" + lang.lang("コマンド実行中にエラーが発生しました。"))
                        error = 1
                        continue

                    print("\t\033[38;5;4m[INFO]\033[0mteam1 stop.")
                    stdout, stderr = logtemp3.communicate()
                    try:
                        stderr = stderr.decode("utf-8")
                        stdout = stdout.decode("utf-8")
                    except UnicodeDecodeError as e:
                        print("\033[38;5;3m[WARNING]\033[0m\t" + str(e))
                        stderr = stderr.decode("utf-8", "replace")
                        stdout = stdout.decode("utf-8", "replace")
                    logt2 += stdout + stderr
                    logt2 += "\n"
                    print("\t\033[38;5;4m[INFO]\033[0mreturncode:" + str(logtemp3.returncode))
                    if logtemp3.returncode != 0:
                        logtemp1.kill()
                        print("\t\033[38;5;9m\033[1m[ERR]\033[0m" + lang.lang("コマンド実行中にエラーが発生しました。"))
                        error = 1
                        continue

                    print("\t\033[38;5;4m[INFO]\033[0mteam2 stop.")
                    stdout, stderr = logtemp1.communicate()
                    try:
                        stderr = stderr.decode("utf-8")
                        stdout = stdout.decode("utf-8")
                    except UnicodeDecodeError as e:
                        print("\033[38;5;3m[WARNING]\033[0m\t" + str(e))
                        stderr = stderr.decode("utf-8", "replace")
                        stdout = stdout.decode("utf-8", "replace")
                    logs += stdout + stderr
                    logs += "\n"
                    print("\t\033[38;5;4m[INFO]\033[0mreturncode:" + str(logtemp1.returncode))
                    if logtemp1.returncode != 0:
                        logtemp1.kill()
                        print("\t\033[38;5;9m\033[1m[ERR]\033[0m" + lang.lang("コマンド実行中にエラーが発生しました。"))
                        error = 1
                        continue

                    print("\t\033[38;5;4m[INFO]\033[0mrcssserver stop.")
                except (subprocess.CalledProcessError, EOFError, FileNotFoundError) as e:
                    print("\t\033[38;5;9m\033[1m[ERR]\033[0m" + lang.lang("コマンド実行中にエラーが発生しました。\n"), e)
                    cszp_module.killsoccer(False)
                    error = 1
                    continue
                except KeyboardInterrupt:
                    cszp_module.killsoccer(False)
                    error = 1
                    break

                logs += "\t" + datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                logt1 += "\t" + datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                logt2 += "\t" + datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                exittime = datetime.now().strftime("%Y%m%d_%H%M%S")
                cszp_module.killsoccer(False)
                soccer = cszp_log.log(logs)
                result += "\n" + exittime + "," + soccer[0] + "," + soccer[1] + "," + soccer[2] + "," + soccer[
                    3] + "," + \
                          str(int(soccer[2]) - int(soccer[3])) + "," + str(int(soccer[3]) - int(soccer[2]))
                self.result_list.append(
                    [exittime, soccer[0], soccer[1], int(soccer[2]), int(soccer[3]), int(soccer[2]) - int(soccer[3]),
                     int(soccer[3]) - int(soccer[2])])

                if logs2[0]:
                    data = module.Open("./config/config.conf")
                    df = data.read()
                    # print(df)
                    temp = open(df.split(",")[7] + "/" + exittime + "_server.log", "w")
                    temp.write(logs)
                    temp.close()

                if logs2[1]:
                    data = module.Open("./config/config.conf")
                    df = data.read()
                    # print(df.split("'"))
                    temp = open(df.split(",")[7] + "/" + exittime + "_team1.log", "w")
                    temp.write(logt1)
                    temp.close()
                    temp = open(df.split(",")[7] + "/" + exittime + "_team2.log", "w")
                    temp.write(logt2)
                    temp.close()

                if logs2[2] is not False:
                    data = module.Open("./config/config.conf")
                    df = data.read()
                    # print(df.split(",")[9] + "/" + file)
                    temp = open(df.split(",")[7] + "/" + logs2[2], "w")
                    soccer = cszp_log.log(logs)
                    temp.write(
                        "\n" + exittime + "," + soccer[0] + "," + soccer[1] + "," + soccer[2] + "," + soccer[
                            3] + "," + str(
                            int(soccer[2]) - int(soccer[3])) + "," + str(int(soccer[3]) - int(soccer[2])))
                    temp.close()

                list_time.append(time.time() - tmp_time)
                print("━" * 50 + "\n\033[38;5;4m[INFO]\033[0mRun Time:", totime(int(list_time[-1])), " Total",
                      totime(int(sum(list_time))), " ETA",
                      totime(int((loop - len(list_time)) * (sum(list_time) / len(list_time)))), "\n" + "━" * 50)

            if error == 0:
                exittime = datetime.now().strftime("%Y%m%d_%H%M%S")
                subprocess.check_call("mkdir ./html_logs/" + exittime, shell=True)
                subprocess.check_call("cp ./html/index.html ./html_logs/" + exittime + "/", shell=True)
                print("\033[38;5;10m\033[1m[OK]\033[0mDone! time:" + totime(
                    int(sum(list_time))) + "\n" + "━" * 50 + "\nresult")
                bs = StringIO(result)
                data = pd.DataFrame(list(csv.reader(bs))[1:],
                                    columns=(
                                        'date', 'team1', 'team2', 'team1_score', 'team2_score', 'team1 goal difference',
                                        "team2 goal difference"))
                data = data.set_index('date')
                # print(data)
                csvd = result.splitlines()[1:]
                csvtd = []
                for i in csvd:
                    csvtd.append(i.split(","))
                csvd = ""
                for i in csvtd:
                    for j in range(len(i)):
                        if j != 0:
                            if j != len(i) - 1:
                                csvd += i[j] + ","
                            else:
                                csvd += i[j] + "\n"
                with open("./html_logs/" + exittime + "/" + "html.csv", "w") as f:
                    f.write("プレイヤー1,プレイヤー２," + data["team1"][0] + "の得点," + data["team2"][0] + "の得点," + data["team1"][
                        0] + "の得失点差," +
                            data["team2"][0] + "の得失点差\n" + csvd)
                data["team1_score"] = data["team1_score"].astype(int)
                data["team2_score"] = data["team2_score"].astype(int)
                print(data)
                print("━" * 50)
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
                plt.savefig("./html_logs/" + exittime + "/" + "file1.png", dpi=300)
                plt.clf()

        finally:
            try:
                self.httpd.shutdown()
            except AttributeError:
                pass
            if exit:
                Input.Input(lang.lang("Enterキーを押して続行..."), dot=False)

    def get_result(self):
        return self.result_list


def check_path(text):
    if not os.path.isfile(text[1][1]):
        text[1][2] = 0
    else:
        text[1][2] = 1
    if not os.path.isfile(text[2][1]):
        text[2][2] = 0
    else:
        text[2][2] = 1
    if text[1][1] == text[2][1]:
        text[1][2] = 0
        text[2][2] = 0
    return text


def yesno(title, text):
    tmp = 0
    k = ""
    while k != "\n":
        if tmp == 0:
            cuitools.box(title,
                         text + ["\033[7mYes\033[0m  No"])
        else:
            cuitools.box(title,
                         text + ["Yes  \033[7mNo\033[0m"])
        k = cuitools.Key()
        if k == "\x1b":
            k = cuitools.Key()
            if k == "[":
                k = cuitools.Key()
                if k == "C":
                    if tmp == 0:
                        tmp = 1
                elif k == "D":
                    if tmp == 1:
                        tmp = 0
    return tmp


def kakunin(module):
    data = module.Open("./config/config.conf")
    datas = data.read().splitlines()
    data.close()
    datas = datas[0].split(",")
    datal = []
    for i in range(0, len(datas), 2):
        datat = []
        datat += datas[i:i + 2]
        datal.append(datat)
    table = Texttable()
    table.add_rows(datal)
    return table


def setting(lang, module, Input_, testmode=False, loopmode=False):
    data = module.Open("./config/config.conf")
    datas = data.read().splitlines()
    data.close()
    datas = datas[0].split(",")
    table = kakunin(module)

    if yes_no_dialog(
            title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("設定確認"),
            text=table.draw() + lang.lang("\nEnterキーを押して続行...")).run():
        k = ""
        ok = False
        select = 0
        text = [
            ["\033[38;5;10m" + lang.lang("前ページへ戻る(ホーム)"), False],
            ["\033[38;5;11m" + lang.lang("Team1(黄色)チームのパスを選択"), "None", 0],
            ["\033[38;5;9m" + lang.lang("Team2(赤色)チームのパスを選択"), "None", 0],
            ["\033[38;5;10m" + "─" * shutil.get_terminal_size()[0], None],
            ["\033[38;5;12m" + lang.lang("サーバーの引数を入力（ない場合は空欄）"), "", None],
            ["\033[38;5;10m" + "─" * shutil.get_terminal_size()[0], None],
            ["\033[38;5;9m" + lang.lang("保存先") + " " + datas[7], None],
            ["\033[38;5;11m" + lang.lang("サーバーログの保存"), "No", None],
            ["\033[38;5;11m" + lang.lang("プレイヤーログの保存"), "No", None],
            ["\033[38;5;11m" + lang.lang("csvログの保存"), "No", None],
            ["\033[38;5;10m" + "─" * shutil.get_terminal_size()[0], None],
            ["\033[38;5;14m" + lang.lang("synchモードでの実行"), "No", None],
            ["\033[38;5;14m" + lang.lang("サーバーの起動"), "Yes", None],
        ]
        if loopmode:
            text += [
                ["\033[38;5;10m" + "─" * shutil.get_terminal_size()[0], None],
                ["\033[38;5;15m" + lang.lang("ループ回数を指定"), 3, 1]
            ]
        if testmode:
            text += [
                ["", None],
                ["\033[38;5;11m" + lang.lang("*テストモードで実行しています"), None]
            ]
        else:
            text += [["", None]]
        text += [
            ["\033[38;5;10m" + lang.lang("サッカーを実行"), False]
        ]
        ver = open("./version")
        v = ver.read()
        ver.close()
        while k != "\n" or ok is False:
            cuitools.reset()
            print("\033[1;1H\033[0m\033[38;5;172m")
            figlet("cszp " + v)
            for i, j in enumerate(text):
                if j[1] is False:
                    if i == select:
                        print("\033[1m\033[38;5;9m> " + j[0] + "\033[0m")
                    else:
                        print("  " + j[0] + "\033[0m")
                elif j[1] is not None:
                    if j[2] is None:
                        if i == select:
                            print(
                                "\033[1m\033[38;5;9m> " + j[0] + ":\033[0m\033[4m\033[38;5;14m" + str(j[1]) + "\033[0m")
                        else:
                            print("  " + j[0] + ":\033[0m\033[4m\033[38;5;14m" + str(j[1]) + "\033[0m")
                    else:
                        if i == select:
                            print(
                                "\033[1m\033[38;5;9m> " + j[0] + ":\033[0m\033[4m\033[38;5;14m" + str(
                                    j[1]) + "\033[0m " + (
                                        "\033[38;5;9m✖" * ((j[2] - 1) * -1) + "\033[38;5;10m✔" * j[2]) + "\033[0m ")
                        else:
                            print("  " + j[0] + ":\033[0m\033[4m\033[38;5;14m" + str(j[1]) + "\033[0m " + (
                                    "\033[38;5;9m✖" * ((j[2] - 1) * -1) + "\033[38;5;10m✔" * j[2]) + "\033[0m ")
                else:
                    print(j[0])
            print("\n")

            k = cuitools.Key()
            if k == "\n":
                if select == 0:
                    break
                elif select == 1 or select == 2:
                    tmp = yesno(lang.lang("選択"), [lang.lang("簡単サッカー実行リストから選択しますか？")])
                    if tmp == 0:
                        data = module.Open("./config/setting.conf")
                        datas = data.read().splitlines()[0]
                        data.close()
                        datas = datas.split(",")
                        datal = []
                        for i in range(2, len(datas), 2):
                            datal.append((datas[i + 1], datas[i]))
                        if len(datal) == 0:
                            k = ""
                            while k != "\n":
                                cuitools.box(lang.lang("エラー"), [
                                    lang.lang("簡単サッカー実行リストにチームが設定されていないのでこの機能は使用できません。"),
                                    lang.lang("settingコマンドでチームの追加ができます。詳しくはsettingコマンドを確認してください。"),
                                    lang.lang("Enterキーを押して続行...")
                                ])
                                k = cuitools.Key()
                        else:
                            tmp = Input()
                            tmp = tmp.Input(lang.lang("簡単サッカー実行リストで設定した名前を指定（Tabで一覧が確認できます）"),
                                            word=list(map(lambda n: n[1], datal)))
                            text[select][1] = "None"
                            text = check_path(text)
                            for i in datal:
                                if i[1] == tmp:
                                    text[select][1] = i[0]
                                    text = check_path(text)
                                    break
                    else:
                        if select == 1:
                            tmp = cuitools.Inputfilegui(lang.lang("Team1(黄色)チームのパスを選択") + lang.lang("(選択方法の変更・終了はQキー)"))
                        else:
                            tmp = cuitools.Inputfilegui(lang.lang("Team2(赤色)チームのパスを選択") + lang.lang("(選択方法の変更・終了はQキー)"))
                        if tmp == -1:
                            pass
                        elif tmp == -2:
                            raise KeyboardInterrupt
                        else:
                            text[select][1] = tmp
                            text = check_path(text)
                elif select == 4:
                    tmp = Input()
                    text[select][1] = tmp.Input(lang.lang("サーバーの引数を入力（ない場合は空欄）"))

                elif select == 7:
                    tmp = yesno(lang.lang("選択"), [lang.lang("サーバーログを保存しますか？")])
                    if tmp == 0:
                        text[select][1] = "Yes"
                    else:
                        text[select][1] = "No"
                elif select == 8:
                    tmp = yesno(lang.lang("選択"), [lang.lang("プレイヤーログを保存しますか？")])
                    if tmp == 0:
                        text[select][1] = "Yes"
                    else:
                        text[select][1] = "No"
                elif select == 9:
                    tmp = yesno(lang.lang("選択"), [lang.lang("csvログを保存しますか？")])
                    if tmp == 0:
                        tmp = Input()
                        tmp = tmp.Input("filename")
                        if len(tmp.split(".")) == 1:
                            tmp += ".csv"
                        text[select][1] = tmp
                    else:
                        text[select][1] = "No"
                elif select == 11:
                    tmp = yesno(lang.lang("選択"), [lang.lang("synchモードで実行しますか？")])
                    if tmp == 0:
                        text[select][1] = "Yes"
                    else:
                        text[select][1] = "No"
                elif select == 12:
                    tmp = yesno(lang.lang("選択"), [lang.lang("サーバーを起動させますか？")])
                    if tmp == 0:
                        text[select][1] = "Yes"
                    else:
                        text[select][1] = "No"
                elif select == 14 and loopmode:
                    tmp = Input()
                    tmp = tmp.Input(lang.lang("ループ回数を指定"))
                    try:
                        text[select][1] = int(tmp)
                    except ValueError:
                        text[select][1] = 0
                    if text[select][1] == 0:
                        text[select][2] = 0
                    else:
                        text[select][2] = 1
                elif select == len(text) - 1:
                    ok = True
                    for i in text:
                        if len(i) == 3:
                            if i[2] == 0:
                                k = ""
                                ok = False
                                while k != "\n":
                                    cuitools.box(lang.lang("エラー"), [lang.lang("問題箇所があります。確認してください。"),
                                                                    lang.lang("Enterキーを押して続行...")])
                                    k = cuitools.Key()
                                break

            if k == "\x1b":
                k = cuitools.Key()
                if k == "[":
                    k = cuitools.Key()
                    if k == "B":
                        if len(text) - 1 > select:
                            select += 1
                            while text[select][1] is None:
                                select += 1
                    elif k == "A":
                        if 0 < select:
                            select -= 1
                            while text[select][1] is None:
                                select -= 1

        if ok:
            data = module.Open("./config/config.conf")
            datas = data.read().splitlines()
            data.close()
            datas = datas[0].split(",")
            arg = text[4][1]
            arg += "server::auto_mode=true server::kick_off_wait=20 server::game_over_wait=20 " \
                   "server::connect_wait=2000 server::game_log_dir=" + datas[7] + " server::text_log_dir=" + datas[
                       7] + " server::game_logging=" + (
                           "true" * (datas[3] == "on") + "false" * (datas[3] == "off")) + " server::text_logging=" + (
                           "true" * (datas[3] == "on") + "false" * (datas[3] == "off"))

            if testmode:
                arg += " server::nr_normal_halfs=1 server::nr_extra_halfs=0 server::penalty_shoot_outs=0 " \
                       "server::half_time=10"
            if loopmode:
                loop = text[14][1]
            else:
                loop = 1
            if text[12][1] == "Yes":
                s = True
            else:
                s = False
            if text[11][1] == "Yes":
                synch = True
            else:
                synch = False
            if text[9][1] == "Yes":
                tmp1 = True
            else:
                tmp1 = False
            if text[8][1] == "Yes":
                tmp2 = True
            else:
                tmp2 = False
            if text[7][1] == "Yes":
                tmp3 = True
            else:
                tmp3 = False
            soccer([text[2][1], text[1][1], arg], lang, loop, module, [tmp3, tmp2, tmp1, synch],
                   Input_, s)


def rrt(lang, module, Input_):
    table = kakunin(module)

    data = module.Open("./config/setting.conf")
    datas = data.read().splitlines()[0]
    data.close()
    datas = datas.split(",")
    datal = []
    for i in range(2, len(datas), 2):
        datal.append((datas[i + 1], datas[i]))
    if len(datal) == 0:
        k = ""
        while k != "\n":
            cuitools.box(lang.lang("エラー"), [
                lang.lang("簡単サッカー実行リストにチームが設定されていないのでこの機能は使用できません。"),
                lang.lang("settingコマンドでチームの追加ができます。詳しくはsettingコマンドを確認してください。"),
                lang.lang("Enterキーを押して続行...")
            ])
            k = cuitools.Key()
    elif yes_no_dialog(
            title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("設定確認"),
            text=table.draw() + lang.lang("\nEnterキーを押して続行...")).run():
        k = ""
        csv_save = False
        ok = False
        ver = open("./version")
        v = ver.read()
        ver.close()
        kantan_list = list(map(lambda n: n[1], datal))
        kantan_cmd = list(map(lambda n: n[0], datal))
        select = 0
        selector = []
        synch = False
        while k != "\n" or not ok:
            cuitools.reset()
            print("\033[1;1H\033[0m\033[38;5;172m")
            figlet("cszp " + v)
            if select == -1:
                print("\033[1m\033[38;5;9m>  \033[38;5;10m" + lang.lang("前ページへ戻る(ホーム)") + "\033[0m\n")
            else:
                print("   \033[38;5;10m" + lang.lang("前ページへ戻る(ホーム)") + "\033[0m\n")
            print("\033[38;5;12m" + lang.lang("総当たり戦をさせるチームを選択してください。"))
            for i, j in enumerate(kantan_list):
                if i in selector:
                    if select == i:
                        print("\033[1m\033[38;5;9m>\033[38;5;11m* \033[38;5;10m" + j + "\033[0m")
                    else:
                        print("\033[38;5;11m * \033[38;5;10m" + j + "\033[0m")
                elif select == i:
                    print("\033[1m\033[38;5;9m>  \033[38;5;10m" + j + "\033[0m")
                else:
                    print("   \033[38;5;10m" + j + "\033[0m")
            print("")
            if select == len(kantan_list):
                print("\033[1m\033[38;5;9m>  \033[38;5;14m" + lang.lang(
                    "synchモードでの実行") + ":\033[0m\033[4m\033[38;5;14m" + "No" * (
                              (synch - 1) * -1) + "Yes" * synch + "\033[0m")
            else:
                print("   \033[38;5;14m" + lang.lang("synchモードでの実行") + ":\033[0m\033[4m\033[38;5;14m" + "No" * (
                        (synch - 1) * -1) + "Yes" * synch + "\033[0m")
            if select == len(kantan_list) + 1:
                if csv_save is False:
                    print("\033[1m\033[38;5;9m>  \033[38;5;11m" + lang.lang("csvログの保存") + ":\033[0m\033[4m\033["
                                                                                          "38;5;14mNo\033[0m")
                else:
                    print("\033[1m\033[38;5;9m>  \033[38;5;11m" + lang.lang(
                        "csvログの保存") + ":\033[0m\033[4m\033[38;5;14m" + csv_save + "\033[0m")
            else:
                if csv_save is False:
                    print(
                        "   \033[38;5;11m" + lang.lang("csvログの保存") + ":\033[0m\033[4m\033[38;5;14mNo\033[0m")
                else:
                    print(
                        "   \033[38;5;11m" + lang.lang(
                            "csvログの保存") + ":\033[0m\033[4m\033[38;5;14m" + csv_save + "\033[0m")
            if select == len(kantan_list) + 2 and len(selector) > 1:
                print("\033[1m\033[38;5;9m>  \033[38;5;10m" + lang.lang("サッカーを実行") + "\033[0m")
            elif len(selector) < 2:
                print("   \033[38;5;243m" + lang.lang("サッカーを実行") + "\033[0m")
            else:
                print("   \033[38;5;10m" + lang.lang("サッカーを実行") + "\033[0m")

            table = []
            tmp = [""]
            for i in selector:
                tmp.append(kantan_list[i])
            table.append(tmp)
            for i in selector:
                table.append([kantan_list[i]] + [""] * len(selector))
            print(Texttable().add_rows(table).draw())
            k = cuitools.Key()
            if k == "\x1b":
                k = cuitools.Key()
                if k == "[":
                    k = cuitools.Key()
                    if k == "B":
                        if len(kantan_list) + 2 > select:
                            select += 1
                            if len(kantan_list) + 2 == select and len(selector) < 2:
                                select -= 1
                    elif k == "A":
                        if -1 < select:
                            select -= 1
            if (k == " " or k == "\n") and select == -1:
                break
            elif (k == " " or k == "\n") and select == len(kantan_list) + 2:
                ok = True
                break
            elif (k == " " or k == "\n") and select == len(kantan_list) + 1:
                tmp = yesno(lang.lang("選択"), [lang.lang("csvログを保存しますか？")])
                if tmp == 0:
                    tmp = Input()
                    tmp = tmp.Input("filename")
                    if len(tmp.split(".")) == 1:
                        tmp += ".csv"
                    csv_save = tmp
                else:
                    csv_save = False
            elif (k == " " or k == "\n") and select == len(kantan_list):
                tmp = yesno(lang.lang("選択"), [lang.lang("synchモードで実行しますか？")])
                if tmp == 0:
                    synch = True
                else:
                    synch = False
            elif (k == " " or k == "\n") and select > -1:
                if select in selector:
                    for i, j in enumerate(selector):
                        if j == select:
                            del selector[i]
                            break
                else:
                    selector.append(select)
        if ok:
            print("\033[1;1H\033[0m\033[38;5;172m")
            figlet("cszp " + v)
            print("\033[0m")
            table = []
            tmp = [""]
            for i in selector:
                tmp.append(kantan_list[i])
            table.append(tmp)
            for i in selector:
                table.append([kantan_list[i]] + [""] * len(selector))
            for i in range(len(table)):
                if i != 0:
                    table[i][i] = "N/A"
            tmp = []
            for i in selector:
                for j in selector:
                    if kantan_cmd[i] != kantan_cmd[j] and not [kantan_cmd[j], kantan_cmd[i]] in tmp:
                        tmp.append([kantan_cmd[i], kantan_cmd[j]])
            tmp2 = []
            for i in selector:
                for j in selector:
                    if kantan_cmd[i] != kantan_cmd[j] and not [kantan_list[j], kantan_list[i]] in tmp2:
                        tmp2.append([kantan_list[i], kantan_list[j]])
            # print(tmp)
            data = module.Open("./config/config.conf")
            datas = data.read().splitlines()
            data.close()
            datas = datas[0].split(",")
            arg = "server::auto_mode=true server::kick_off_wait=20 server::game_over_wait=20 " \
                  "server::connect_wait=2000 server::game_log_dir=" + datas[7] + " server::text_log_dir=" + datas[
                      7] + " server::game_logging=" + (
                          "true" * (datas[3] == "on") + "false" * (datas[3] == "off")) + " server::text_logging=" + (
                          "true" * (datas[3] == "on") + "false" * (datas[3] == "off"))
            # arg += " server::nr_normal_halfs=1 server::nr_extra_halfs=0 server::penalty_shoot_outs=0 " \
            #        "server::half_time=10"
            s = [0, 1]
            results = []
            for i, j in zip(tmp, tmp2):
                cuitools.reset()
                print(Texttable().add_rows(table).draw() + "\n" + "━" * 50)
                _ = soccer([i[0], i[1], arg], lang, 1, module, [False, False, False, synch],
                           Input_, False, False, False)
                result = _.get_result()
                if len(result) == 0:
                    table[s[0] + 1][s[1] + 1] = "Error"
                else:
                    tmp3 = result[0]
                    tmp3[1] = table[s[0] + 1][0]
                    tmp3[2] = table[0][s[1] + 1]
                    results.append(tmp3)
                    table[s[0] + 1][s[1] + 1] = str(result[0][3]) + "-" + str(result[0][4])
                s[1] += 1
                if s[1] > len(selector) - 1:
                    s[0] += 1
                    s[1] = 0
                tmp3 = list(map(lambda n: n + 1, s))
                while [j[1], j[0]] != [table[tmp3[0]][0], table[0][tmp3[1]]]:
                    print([table[tmp3[0]][0], table[0][tmp3[1]]], [j[1], j[0]])
                    tmp3[1] += 1
                    if tmp3[1] > len(selector):
                        tmp3[0] += 1
                        tmp3[1] = 0
                if len(result) == 0:
                    table[tmp3[0]][tmp3[1]] = "Error"
                else:
                    table[tmp3[0]][tmp3[1]] = str(result[0][4]) + "-" + str(result[0][3])

                while s[1] <= s[0]:
                    s[1] += 1
                    if s[1] > len(selector):
                        s[0] += 1
                        s[1] = 0
            if csv_save is not False:
                with open(datas[7] + "/" + csv_save, "w") as f:
                    f.write("\n".join(list(map(lambda n: ",".join(map(str, n)), results))))
            cuitools.reset()
            print("\033[1m\033[38;5;11m"+lang.lang("集計結果")+"\033[0m\n"+"━"*50+"\n"+Texttable().add_rows(table).draw())
            tmp = []
            for i in results:
                if not i[1] in list(map(lambda n: n[0], tmp)):
                    tmp.append([i[1], [0, 0, 0]])
                for j, k in enumerate(tmp):
                    if k[0] == i[1]:
                        break
                if i[3] > i[4]:
                    tmp[j][1][0] += 1
                elif i[3] < i[4]:
                    tmp[j][1][1] += 1
                else:
                    tmp[j][1][2] += 1

                if not i[2] in list(map(lambda n: n[0], tmp)):
                    tmp.append([i[2], [0, 0, 0]])
                for j, k in enumerate(tmp):
                    if k[0] == i[2]:
                        break
                if i[4] > i[3]:
                    tmp[j][1][0] += 1
                elif i[4] < i[3]:
                    tmp[j][1][1] += 1
                else:
                    tmp[j][1][2] += 1
            table = [["", "W", "D", "L", "Total"]]
            for i in tmp:
                table.append([i[0], i[1][0], i[1][1], i[1][2], i[1][0] - i[1][1]])
            print("\n"+"━"*50+"\n"+Texttable().add_rows(table).draw())
            Input_.Input(lang.lang("Enterキーを押して続行..."), dot=False)
