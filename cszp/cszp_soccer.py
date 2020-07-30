import csv
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
from prompt_toolkit import HTML
from prompt_toolkit.shortcuts import yes_no_dialog, radiolist_dialog, button_dialog, input_dialog, message_dialog
from texttable import Texttable

from cszp import cszp_log
from cszp import cszp_module

matplotlib.use('Agg')


class soccerHTTPServer_Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        print(self.path)
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

    def __init__(self, cmd, lang, loop, module, logs2, Input):
        global result
        result = ""
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
        if loop > 1:
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
                        Input.Input("Enterキーを押して続行...")
                        error = 1
                        break

                    print("\t\033[38;5;4m[INFO]\033[0mteam1 stop.")
                    stdout, stderr = logtemp3.communicate()
                    stderr = stderr.decode("utf-8")
                    stdout = stdout.decode("utf-8")
                    logt2 += stdout + stderr
                    logt2 += "\n"
                    print("\t\033[38;5;4m[INFO]\033[0mreturncode:" + str(logtemp3.returncode))
                    if logtemp3.returncode != 0:
                        logtemp1.kill()
                        print("\t\033[38;5;9m\033[1m[ERR]\033[0m" + lang.lang("コマンド実行中にエラーが発生しました。"))
                        error = 1
                        break

                    print("\t\033[38;5;4m[INFO]\033[0mteam2 stop.")
                    stdout, stderr = logtemp1.communicate()
                    stderr = stderr.decode("utf-8")
                    stdout = stdout.decode("utf-8")
                    logs += stdout + stderr
                    logs += "\n"
                    print("\t\033[38;5;4m[INFO]\033[0mreturncode:" + str(logtemp1.returncode))
                    if logtemp1.returncode != 0:
                        logtemp1.kill()
                        print("\t\033[38;5;9m\033[1m[ERR]\033[0m" + lang.lang("コマンド実行中にエラーが発生しました。"))
                        error = 1
                        break

                    print("\t\033[38;5;4m[INFO]\033[0mrcssserver stop.")
                except (subprocess.CalledProcessError, KeyboardInterrupt, EOFError, FileNotFoundError) as e:
                    print("\t\033[38;5;9m\033[1m[ERR]\033[0m" + lang.lang("コマンド実行中にエラーが発生しました。\n"), e)
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
                    temp = open(df.split(",")[7] + "/" + logs2[2], "a")
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
            Input.Input("Enterキーを押して続行...", dot=False)


def team(num, lang, module):
    q = button_dialog(
        title=HTML("<style fg='red'>" * (num - 1) + "<style fg='olive'>" * abs(num - 2) + lang.lang(
            "cszp 簡単サッカー実行プログラム") + "/" +
                   lang.lang("Team" + str(num) + "(黄色)" * abs(num - 2) + "(赤色)" * (
                           num - 1) + "チームのパスを選択") + "</style>"),
        text=lang.lang("簡単サッカー実行リストから選択しますか？"),
        buttons=[
            ("Yes", True),
            ("No", False),
            ("Cancel", None)
        ]
    ).run()
    if q:
        data = module.Open("./config/setting.conf")
        datas = data.read().splitlines()[0]
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(2, len(datas), 2):
            datal.append((datas[i + 1], datas[i]))
        if len(datal) != 0:
            result = radiolist_dialog(
                title=HTML("<style fg='red'>" * (num - 1) + "<style fg='olive'>" * abs(num - 2) + lang.lang(
                    "cszp 簡単サッカー実行プログラム") + "/" +
                           lang.lang("Team" + str(num) + "(黄色)" * abs(num - 2) + "(赤色)" * (
                                   num - 1) + "チームのパスを選択") + "</style>"),
                text=lang.lang("下のリストから選択してください。Spaceキーで選択できます。\nキャンセルを選択すると選択方法の変更・終了ができます。"),
                values=datal
            ).run()
            if result is not None:
                return result
            else:
                return team(num, lang, module)
        else:
            if button_dialog(
                    title=HTML("<style fg='red'>" * (num - 1) + "<style fg='olive'>" * abs(num - 2) + lang.lang(
                        "cszp 簡単サッカー実行プログラム") + "/" +
                               lang.lang("Team" + str(num) + "(黄色)" * abs(num - 2) + "(赤色)" * (
                                       num - 1) + "チームのパスを選択") + "</style>"),
                    text=lang.lang("簡単サッカー実行リストにチームが設定されていないのでこの機能は使用できません。\n"
                                   "settingコマンドでチームの追加ができます。詳しくはsettingコマンドを確認してください。\n"
                                   "Cancelを押すとメニュー画面にもどります。"),
                    buttons=[
                        ('Ok', True),
                        ('Cancel', False),
                    ]).run():
                inp = cuitools.Inputfilegui(
                    lang.lang("Team" + str(num) + "(黄色)" * abs(num - 2) + "(赤色)" * (num - 1) + "チームのパスを選択") + lang.lang(
                        "(選択方法の変更・終了はQキー)"))
                if inp == -1:
                    return team(num, lang, module)
                elif inp == -2:
                    raise KeyboardInterrupt
                else:
                    return inp
    elif not q and q is not None:
        inp = cuitools.Inputfilegui(
            lang.lang("Team" + str(num) + "(黄色)" * abs(num - 2) + "(赤色)" * (num - 1) + "チームのパスを選択") + lang.lang(
                "(選択方法の変更・終了はQキー)"))
        if inp == -1:
            return team(num, lang, module)
        elif inp == -2:
            raise KeyboardInterrupt
        else:
            return inp


def setting(lang, module, Input, testmode=False, loopmode=False):
    # noinspection PyBroadException
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

    if yes_no_dialog(
            title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("設定確認"),
            text=table.draw() + lang.lang("\nEnterキーを押して続行...")).run():
        cuitools.reset()
        ok = 0
        csv_q = False
        while ok != 7 + loopmode + (csv_q is not False):
            if ok == 0:
                path = team(1, lang, module)
            else:
                path = True
            if path is not None:
                if ok == 0:
                    team1 = path
                    ok += 1
                if ok == 1:
                    path = team(2, lang, module)
                else:
                    path = True
                if path is not None:
                    if ok == 1:
                        team2 = path
                        ok += 1

                    if team1 == team2:
                        inp = button_dialog(
                            title=HTML("<style fg='red'>" + lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang(
                                "Team2(赤色)チームのパスを選択") + "</style>"),
                            text=lang.lang("同じチームと対戦させることは、仕様上不可能です。違うチームに変更してください。\n"
                                           "変更するチームを選択してください。Cancelを押すとホーム画面に戻ります。"),
                            buttons=[
                                ('Team1', True),
                                ('Team2', False),
                                ("Cancel", None)
                            ]).run()
                        if inp:
                            path = team(1, lang, module)
                            if path is not None:
                                # print(ok)
                                team1 = path
                                continue
                            else:
                                break
                        elif not inp and inp is not None:
                            ok -= 1
                            continue
                        else:
                            break

                    if ok == 2:
                        inp = input_dialog(title=lang.lang(
                            "cszp 簡単サッカー実行プログラム") + "/" + lang.lang("サーバーの引数を入力"),
                                           text=lang.lang("サーバーの引数を入力（ない場合は空欄）")).run()
                    else:
                        inp = True
                    if inp is not None:
                        if ok == 2:
                            arg = inp
                            ok += 1
                        data = module.Open("./config/config.conf")
                        datas = data.read().splitlines()[0]
                        data.close()
                        if ok == 3:
                            inp = button_dialog(
                                title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("サーバーログの保存"),
                                text=lang.lang("サーバーログを保存しますか？\n保存先") + " " + datas.split(",")[7],
                                buttons=[
                                    ('Yes', True),
                                    ('No', False),
                                    ('Cancel', None)
                                ],
                            ).run()
                        else:
                            inp = True
                        if inp is not None:
                            if ok == 3:
                                server = inp
                                ok += 1
                            if ok == 4:
                                inp = button_dialog(
                                    title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("プレイヤーログの保存"),
                                    text=lang.lang("プレイヤーログを保存しますか？\n保存先") + " " + datas.split(",")[7],
                                    buttons=[
                                        ('Yes', True),
                                        ('No', False),
                                        ('Cancel', None)
                                    ],
                                ).run()
                            else:
                                inp = True
                            if inp is not None:
                                if ok == 4:
                                    player = inp
                                    ok += 1
                                if ok == 5:
                                    inp = button_dialog(
                                        title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("csvログの保存"),
                                        text=lang.lang("csvログを保存しますか？\n保存先") + " " + datas.split(",")[7],
                                        buttons=[
                                            ('Yes', True),
                                            ('No', False),
                                            ('Cancel', None)
                                        ],
                                    ).run()
                                else:
                                    inp = True
                                if inp is not None:
                                    if ok == 5:
                                        csv_q = inp
                                        ok += 1

                                    if ok == 6:
                                        inp = button_dialog(
                                            title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("synchモードでの実行"),
                                            text=lang.lang("synchモードで実行しますか？"),
                                            buttons=[
                                                ('Yes', True),
                                                ('No', False),
                                                ('Cancel', None)
                                            ],
                                        ).run()
                                    else:
                                        inp = True
                                    if inp is not None:
                                        if ok == 6:
                                            synch = inp
                                            ok += 1
                                        if csv_q and ok == 7:
                                            inp = input_dialog(title=lang.lang(
                                                "cszp 簡単サッカー実行プログラム") + "/" + lang.lang("csvのファイル名を指定"),
                                                               text="filename").run()
                                            if inp is not None:
                                                if inp != "":
                                                    csv_q = inp
                                                    ok += 1
                                                else:
                                                    message_dialog(title=lang.lang(
                                                        "cszp 簡単サッカー実行プログラム") + "/" + lang.lang("csvのファイル名を指定"),
                                                                   text=lang.lang("ファイル名を入力してください。")).run()
                                                    continue
                                            else:
                                                ok -= 1
                                                continue

                                        if loopmode:
                                            inp = input_dialog(title=lang.lang(
                                                "cszp 簡単サッカー実行プログラム") + "/" + lang.lang("ループ回数を指定"),
                                                               text=lang.lang("ループ回数を指定")).run()
                                            if inp is not None:
                                                try:
                                                    loop = int(inp)
                                                    ok += 1
                                                except ValueError:
                                                    message_dialog(title=lang.lang(
                                                        "cszp 簡単サッカー実行プログラム") + "/" + lang.lang("ループ回数を指定"),
                                                                   text=lang.lang("数値を半角で入力してください。")).run()
                                                    continue
                                            else:
                                                ok -= 1
                                                continue
                                        else:
                                            loop = 1
                                    else:
                                        ok -= 1
                                        continue
                                else:
                                    ok -= 1
                                    continue
                            else:
                                ok -= 1
                                continue
                        else:
                            ok -= 1
                            continue
                    else:
                        ok -= 1
                        continue
                else:
                    ok -= 1
                    continue
            else:
                break
        if ok == 7 + loopmode + (csv_q is not False):
            if yes_no_dialog(
                    title=lang.lang("cszp 簡単サッカー実行プログラム") + "/" + lang.lang("確認"),
                    text="team1 path:" + team1 + "\n" +
                         "team2 path:" + team2 + "\n" +
                         "server arg:" + arg + "\n" +
                         "server log:" + str(server) + "\n" +
                         "player log:" + str(player) + "\n" +
                         "csv log:" + str(csv_q) + "\n" +
                         "synch mode:" + str(synch) + "\n" +
                         lang.lang("\nEnterキーを押して続行...")).run():

                arg += "server::auto_mode=true server::kick_off_wait=20 server::game_over_wait=20 " \
                       "server::connect_wait=2000 " + "server::game_log_dir=" + \
                       datas.split(",")[7] + " server::text_log_dir=" + datas.split(",")[
                           7] + " server::game_logging=" + ("true" * (datas.split(",")[3] == "on") + "false" * (
                        datas.split(",")[3] == "off")) + " server::text_logging=" + (
                               "true" * (datas.split(",")[3] == "on") + "false" * (datas.split(",")[3] == "off"))

                if testmode:
                    arg += " server::nr_normal_halfs=1 server::nr_extra_halfs=0 server::penalty_shoot_outs=0 " \
                           "server::half_time=10"
                soccer([team2, team1, arg], lang, loop, module, [server, player, csv_q, synch], Input)
            else:
                setting(lang, module, testmode, loopmode)
