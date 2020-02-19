import os
import subprocess
import time
from datetime import datetime

import cszp_html
import cszp_log
import subp
import tqdm
from texttable import *


def loop(cmd, loops):
    subp.reset()
    inp = ""
    while inp.lower() != "y" and inp.lower() != "n":
        inp = subp.Input("Do you want to save the program log? Y/n")
        if inp.lower() != "y" and inp.lower() != "n":
            print("\033[1m\033[38;5;9mERR:\033[0mPlease answer with y or n")
    i1 = inp.lower()
    inp = ""
    while inp.lower() != "y" and inp.lower() != "n":
        inp = subp.Input("Do you want to save the server log? Y/n")
        if inp.lower() != "y" and inp.lower() != "n":
            print("\033[1m\033[38;5;9mERR:\033[0mPlease answer with y or n")
    i2 = inp.lower()
    inp = ""
    while inp.lower() != "y" and inp.lower() != "n":
        inp = subp.Input("Would you like to collect the results of the battle in a csv file? Y/n")
        if inp.lower() != "y" and inp.lower() != "n":
            print("\033[1m\033[38;5;9mERR:\033[0mPlease answer with y or n")
    i3 = inp.lower()
    if i3 == "y":
        file = subp.Input("FileName?")
        subprocess.Popen("python3 -m http.server 20000".split(" "))
        time.sleep(1)
        serverpid = \
            subprocess.check_output("ps o pid,cmd | grep -E 'python3.*http.*20000' | grep -v grep", shell=True).decode(
                "utf-8").split(" ")
        i = 0
        while serverpid[i] == "":
            i += 1
        serverpid = serverpid[i]
        temp = open("html.csv", "w")
        temp.write("ただいま、情報を収集中です。しばらくお待ちください。")
        temp.close()
        subprocess.check_call("cp ./nofile.png ./file1.png", shell=True)
    subp.reset()
    print("\033[1m\033[38;5;172m---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------")
    print("\033[38;5;2mTeam1-CMD : bash " + cmd[0])
    print("Team2-CMD : bash " + cmd[1])
    sc = "rcssserver " + cmd[2]
    wc = "soccerwindow2 > /dev/null 2>&1"
    print("\033[38;5;2mSERVER-CMD : " + sc)
    print("WINDOW-CMD : " + wc + "\033[0m")
    tqdmd = tqdm.tqdm(range(loops))

    for i in tqdmd:
        logs = ""
        logt1 = ""
        logt2 = ""
        logs += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
        logt1 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
        logt2 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"

        try:
            while len(subprocess.check_output("pidof rcssserver", shell=True).decode("utf-8").split()) != 0:
                subprocess.check_output("killall rcssserver", shell=True)
        except:
            pass
        try:
            while len(subprocess.check_output("pidof soccerwindow2-qt4", shell=True).decode("utf-8").split()) != 0:
                subprocess.check_output("killall soccerwindow2-qt4", shell=True)
        except:
            pass
        logs += "SERVER-CMD : " + sc + "\n"

        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")

        if datas[1] == "on":
            try:
                subprocess.Popen(wc, shell=True)
            except:
                print("\033[38;5;9m\033[1mERR:SOCCERWINDOW2_ERROR")

        try:
            logtemp1 = subprocess.Popen(sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logtemp2 = subprocess.Popen("bash " + cmd[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            logtemp3 = subprocess.Popen("bash " + cmd[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = logtemp1.communicate()
            stderr = stderr.decode("utf-8")
            stdout = stdout.decode("utf-8")
            logs += stdout + stderr
            logs += "\n"
            stdout, stderr = logtemp2.communicate()
            stderr = stderr.decode("utf-8")
            stdout = stdout.decode("utf-8")
            logt1 += stdout + stderr
            logt1 += "\n"
            stdout, stderr = logtemp3.communicate()
            stderr = stderr.decode("utf-8")
            stdout = stdout.decode("utf-8")
            logt2 += stdout + stderr
            logt2 += "\n"
        except:
            print("\033[38;5;9m\033[1mERR:RCSSSERVER_ERROR")
            import traceback
            traceback.print_exc()
            subp.Input("press Enter Key")
            return "error"

        logs += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
        logt1 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
        logt2 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
        exittime = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            while len(subprocess.check_output("pidof soccerwindow2-qt4", shell=True).decode("utf-8").split()) != 0:
                subprocess.check_output("killall soccerwindow2-qt4", shell=True)
        except:
            pass
        soccer = cszp_log.log(logs)
        if i1 == "y":
            try:
                data = open("./config.conf", "r")
            except:
                data = open("./config.conf", "w")
                data.write(
                    "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd()
                )
                data.close()
                data = open("./config.conf", "r")
            df = data.read()
            # print(df.split("'"))
            temp = open(df.split(",")[9] + "/" + exittime + "_team1.log", "w")
            temp.write(logt1)
            temp.close()
            temp = open(df.split(",")[9] + "/" + exittime + "_team2.log", "w")
            temp.write(logt2)
            temp.close()
        if i2 == "y":
            try:
                data = open("./config.conf", "r")
            except:
                data = open("./config.conf", "w")
                data.write(
                    "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd()
                )
                data.close()
                data = open("./config.conf", "r")
            df = data.read()
            # print(df)
            temp = open(df.split(",")[9] + "/" + exittime + "_server.log", "w")
            temp.write(logs)
            temp.close()
        if i3 == "y":
            try:
                data = open("./config.conf", "r")
            except:
                data = open("./config.conf", "w")
                data.write(
                    "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd()
                )
                data.close()
                data = open("./config.conf", "r")
            df = data.read()
            print(df.split(",")[9] + "/" + file)
            temp = open(df.split(",")[9] + "/" + file, "a")
            soccer = cszp_log.log(logs)
            temp.write(
                "\n" + exittime + "," + soccer[0] + "," + soccer[1] + "," + soccer[2] + "," + soccer[3] + "," + soccer[4])
            temp.close()
            cszp_html.plot_socre(file)

    print("\033[1m\033[38;5;172m---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------")
    # print(serverpid)
    subprocess.check_output("kill " + serverpid, shell=True)
    # time.sleep(2)
    cszp_html.logs(exittime)
    subp.Input("Press Enter Key")

def start(cmd, lang):
    subp.reset()
    logs = ""
    logt1 = ""
    logt2 = ""
    logs += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
    logt1 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
    logt2 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
    print("\033[1m\033[38;5;172m---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------")
    print("\033[38;5;2mTeam1-CMD : bash " + cmd[0])
    print("Team2-CMD : bash " + cmd[1])
    sc = "rcssserver " + cmd[2]
    wc = "soccerwindow2"

    try:
        while len(subprocess.check_output("pidof rcssserver", shell=True).decode("utf-8").split()) != 0:
            subprocess.check_output("killall rcssserver", shell=True)
    except:
        pass
    try:
        while len(subprocess.check_output("pidof soccerwindow2-qt4", shell=True).decode("utf-8").split()) != 0:
            subprocess.check_output("killall soccerwindow2-qt4", shell=True)
    except:
        pass
    logs += "SERVER-CMD : " + sc + "\n"
    print("\033[38;5;2mSERVER-CMD : " + sc)
    print("WINDOW-CMD : " + wc + "\033[0m")

    try:
        data = open("./config.conf", "r")
    except:
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
        data.close()
        data = open("./config.conf", "r")
    datas = data.read()
    data.close()
    datas = datas.split(",")
    if datas[3] == "on":
        makelog = "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
        makelog += "TEAM1-CONFIGURE-CMD : " + "cd " + os.path.dirname(cmd[0]) + " && ./configure\n"
        makelog += "TEAM1-MAKE-CMD : " + "cd " + os.path.dirname(cmd[0]) + " && make\n"
        makelog += "TEAM2-CONFIGURE-CMD : " + "cd " + os.path.dirname(cmd[1]) + " && ./configure\n"
        makelog += "TEAM2-MAKE-CMD : " + "cd " + os.path.dirname(cmd[1]) + " && make\033[0m\n"
        print("\033[1m\033[38;5;2mTEAM1-CONFIGURE-CMD : " + "cd " + os.path.dirname(cmd[0]) + " && ./configure\n")
        print("TEAM1-MAKE-CMD : " + "cd " + os.path.dirname(cmd[0]) + " && make\n")
        print("TEAM2-CONFIGURE-CMD : " + "cd " + os.path.dirname(cmd[1]) + " && ./configure\n")
        print("TEAM2-MAKE-CMD : " + "cd " + os.path.dirname(cmd[1]) + " && make\033[0m")
        with tqdm.tqdm(total=100) as pbar:
            pbar.set_description("team1-configure")
            logtemp = subprocess.Popen("cd " + os.path.dirname(cmd[0]) + " && ./configure", shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = logtemp.communicate()
            stderr = stderr.decode("utf-8")
            stdout = stdout.decode("utf-8")
            makelog += stdout + stderr
            makelog += "\n\n"
            pbar.update(25)

            pbar.set_description("team1-make")
            logtemp = subprocess.Popen("cd " + os.path.dirname(cmd[0]) + " && make", shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = logtemp.communicate()
            stderr = stderr.decode("utf-8")
            stdout = stdout.decode("utf-8")
            makelog += stdout + stderr
            makelog += "\n\n"
            pbar.update(25)

            pbar.set_description("team2-configure")
            logtemp = subprocess.Popen("cd " + os.path.dirname(cmd[1]) + " && ./configure", shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = logtemp.communicate()
            stderr = stderr.decode("utf-8")
            stdout = stdout.decode("utf-8")
            makelog += stdout + stderr
            makelog += "\n\n"
            pbar.update(25)

            pbar.set_description("team2-make")
            logtemp = subprocess.Popen("cd " + os.path.dirname(cmd[1]) + " && make", shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = logtemp.communicate()
            stderr = stderr.decode("utf-8")
            stdout = stdout.decode("utf-8")
            makelog += stdout + stderr
            makelog += "\n\n"
            pbar.update(25)
            makelog += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"

    if datas[1] == "on":
        try:
            subprocess.Popen(wc, shell=True)
        except:
            print("\033[38;5;9m\033[1mERR:SOCCERWINDOW2_ERROR")

    try:
        logtemp1 = subprocess.Popen(sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logtemp2 = subprocess.Popen("bash " + cmd[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        logtemp3 = subprocess.Popen("bash " + cmd[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = logtemp1.communicate()
        stderr = stderr.decode("utf-8")
        stdout = stdout.decode("utf-8")
        logs += stdout + stderr
        logs += "\n"
        stdout, stderr = logtemp2.communicate()
        stderr = stderr.decode("utf-8")
        stdout = stdout.decode("utf-8")
        logt1 += stdout + stderr
        logt1 += "\n"
        stdout, stderr = logtemp3.communicate()
        stderr = stderr.decode("utf-8")
        stdout = stdout.decode("utf-8")
        logt2 += stdout + stderr
        logt2 += "\n"
    except:
        print("\033[38;5;9m\033[1mERR:RCSSSERVER_ERROR")
        return "error"

    logs += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
    logt1 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
    logt2 += "---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------\n"
    exittime = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("\033[1m\033[38;5;172m---------- " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " -----------")
    try:
        while len(subprocess.check_output("pidof soccerwindow2-qt4", shell=True).decode("utf-8").split()) != 0:
            subprocess.check_output("killall soccerwindow2-qt4", shell=True)
    except:
        pass
    soccer = cszp_log.log(logs)
    if lang == 1:
        print(soccer[0] + " " + soccer[2] + " - " + soccer[3] + " " + soccer[1] + "で" + cszp_log.kekka(logs, 1))
    else:
        print(soccer[0] + " " + soccer[2] + " - " + soccer[3] + " " + soccer[1] + " " + cszp_log.kekka(logs, 0))
    inp = ""
    while inp.lower() != "y" and inp.lower() != "n":
        inp = subp.Input("Do you want to save the program log? Y/n")
        if inp.lower() != "y" and inp.lower() != "n":
            print("\033[1m\033[38;5;9mERR:\033[0mPlease answer with y or n")
    if inp.lower() == "y":
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        df = data.read()
        temp = open(df.split(",")[9] + "/" + exittime + "_team1.log", "w")
        temp.write(logt1)
        temp.close()
        temp = open(df.split(",")[9] + "/" + exittime + "_team2.log", "w")
        temp.write(logt2)
        temp.close()
    inp = ""
    while inp.lower() != "y" and inp.lower() != "n":
        inp = subp.Input("Do you want to save the server log? Y/n")
        if inp.lower() != "y" and inp.lower() != "n":
            print("\033[1m\033[38;5;9mERR:\033[0mPlease answer with y or n")
    if inp.lower() == "y":
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        df = data.read()
        temp = open(df.split(",")[9] + "/" + exittime + "_server.log", "w")
        temp.write(logs)
        temp.close()
    inp = ""
    while inp.lower() != "y" and inp.lower() != "n":

        inp = subp.Input("Would you like to collect the results of the battle in a csv file? Y/n")
        if inp.lower() != "y" and inp.lower() != "n":
            print("\033[1m\033[38;5;9mERR:\033[0mPlease answer with y or n")
    if inp.lower() == "y":
        inp = subp.Input("FileName?")
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        df = data.read()
        data.close()
        temp = open(df.split(",")[9] + "/" + inp, "a")
        soccer = cszp_log.log(logs)
        temp.write(
            "\n" + exittime + "," + soccer[0] + "," + soccer[1] + "," + soccer[2] + "," + soccer[3] + "," + soccer[4])
        temp.close()

    temp = open("data.csv", "a")
    soccer = cszp_log.log(logs)
    temp.write("\n" + exittime + "," + soccer[0] + "," + soccer[1] + "," + soccer[2] + "," + soccer[3] + "," + soccer[4])
    temp.close()

    inp = ""
    if datas[3] == "on":
        while inp.lower() != "y" and inp.lower() != "n":
            inp = subp.Input("Do you want to save the make log? Y/n")
            if inp.lower() != "y" and inp.lower() != "n":
                print("\033[1m\033[38;5;9mERR:\033[0mPlease answer with y or n")
        if inp.lower() == "y":
            try:
                data = open("./config.conf", "r")
            except:
                data = open("./config.conf", "w")
                data.write(
                    "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd()
                )
                data.close()
                data = open("./config.conf", "r")
            df = data.read()
            data.close()
            temp = open(df.split(",")[9] + "/" + exittime + "_makelog.log", "w")
            temp.write(makelog)
            temp.close()


def setting_jp(testmode=False):
    ok = 0
    cmd = []

    subp.reset()
    print("\033[0m\033[38;5;172m")
    v = open("./version")
    subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
    v.close()
    print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
    print("\033[38;5;39m設定確認")
    # noinspection PyBroadException
    try:
        data = open("./config.conf", "r")
    except:
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
        data.close()
        data = open("./config.conf", "r")
    datas = data.read()
    data.close()
    datas = datas.split(",")
    datal = []
    for i in range(0, len(datas), 2):
        datat = []
        datat += datas[i:i + 2]
        datal.append(datat)
    table = Texttable()
    table.add_rows(datal)
    print(table.draw())
    subp.Input("Press Enter Key")

    subp.reset()
    while ok == 0:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
        print("\n\033[38;5;39m簡単サッカー実行リスト")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\n前画面に戻る場合はbackと入力\n")
        inp = subp.Inputfile("\nTeam1(黄色)チームのパスまたはリストの名前を入力", textcolor="\033[38;5;11m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                # print(inp)
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:名前 " + inp + " は簡単サッカー実行プログラムに登録されていません。\n"
                                                        "また、そのようなファイルも存在しません。\nタイプミスをを確認してください")
                    subp.Input("Enterキーを押して続行...", dot=False)
        else:
            ok = 2

    cmd.append(inp)
    # print(type(inp))
    # subp.Input("")
    if ok != 2:
        ok = 0
    subp.reset()
    while ok == 0 and ok != 2:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
        print("\n\033[38;5;39m簡単サッカー実行リスト")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\n前画面に戻る場合はbackと入力\n\033[38;5;11mTeam1(黄色)チームのパス:" + cmd[0])
        inp = subp.Inputfile("\nTeam2(赤色)チームのパスまたはリストの名前を入力", textcolor="\033[38;5;9m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:名前 " + inp + " は簡単サッカー実行プログラムに登録されていません。\n"
                                                        "また、そのようなファイルも存在しません。\nタイプミスをを確認してください")
                    subp.Input("Enterキーを押して続行...", dot=False)
        else:
            ok = 2

    if ok != 2:
        cmd.append(inp)
        subp.reset()
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
        print("\n\033[38;5;11mTeam1(黄色)チームのパス:" + cmd[0])
        print("\033[38;5;9mTeam2(赤色)チームのパス:" + cmd[1])
        inp = subp.Input("\nサーバーの引数を入力（ない場合は空欄）", textcolor="\033[38;5;9m")
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        df = data.read()
        data.close()
        inp += " server::auto_mode=true server::kick_off_wait=10 server::game_over_wait=10 server::connect_wait=1500 server::game_log_dir=" + \
               df.split(",")[9] + " server::text_log_dir=" + df.split(",")[9]
        if testmode:
            inp += " server::nr_normal_halfs=1 server::nr_extra_halfs=0 server::penalty_shoot_outs=0 " \
                   "server::half_time=10"

        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        datas = data.read()
        datas = datas.split(",")
        data.close()
        if datas[5] == "off":
            inp += " server::game_logging=false"
        if datas[7] == "off":
            inp += " server::text_logging=false"
        cmd.append(inp)
        print("\n\033[38;5;14mloading now...")
        time.sleep(0.5)
        start(cmd, 1)


def setting_en(testmode=False):
    ok = 0
    cmd = []

    subp.reset()
    print("\033[0m\033[38;5;172m")
    v = open("./version")
    subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
    v.close()
    print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
    print("\033[38;5;39mSetting confirmation")
    # noinspection PyBroadException
    try:
        data = open("./config.conf", "r")
    except:
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
        data.close()
        data = open("./config.conf", "r")
    datas = data.read()
    data.close()
    datas = datas.split(",")
    datal = []
    for i in range(0, len(datas), 2):
        datat = []
        datat += datas[i:i + 2]
        datal.append(datat)
    table = Texttable()
    table.add_rows(datal)
    print(table.draw())
    subp.Input("Press Enter Key")

    subp.reset()
    while ok == 0:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
        print("\n\033[38;5;39mEasy soccer run list")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\nEnter back to return to the previous screen\n")
        inp = subp.Inputfile("\nTeam1 (yellow) Enter the team path or list name", textcolor="\033[38;5;11m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                # print(inp)
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:The name " + inp + " is not registered in the easy soccer "
                                                              "execution program. Check for typos.")
                    subp.Input("Press Enter to continue...", dot=False)
        else:
            ok = 2

    cmd.append(inp)
    # print(type(inp))
    # subp.Input("")
    if ok != 2:
        ok = 0
    subp.reset()
    while ok == 0 and ok != 2:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
        print("\n\033[38;5;39mEasy soccer run list")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\nEnter back to return to the previous screen\n\033[38;5;11mTeam1 "
                             "(yellow) Team of the path:" + cmd[0])
        inp = subp.Inputfile("\nEnter Team2 (red) team path or list name", textcolor="\033[38;5;9m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:The name " + inp + " is not registered in the easy soccer "
                                                              "execution program. Check for typos.")
                    subp.Input("Press Enter to continue...", dot=False)
        else:
            ok = 2

    if ok != 2:
        cmd.append(inp)
        subp.reset()
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
        print("\n\033[38;5;11mTeam1 (yellow) Team of the path:" + cmd[0])
        print("\033[38;5;9mTeam2 (red) Team of the path:" + cmd[1])
        inp = subp.Input("\nEnter the server argument (blank if none)", textcolor="\033[38;5;9m")
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        df = data.read()
        data.close()
        inp += " server::auto_mode=true server::kick_off_wait=10 server::game_over_wait=10 server::connect_wait=1500 server::game_log_dir=" + \
               df.split(",")[9] + " server::text_log_dir=" + df.split(",")[9]
        if testmode:
            inp += " server::nr_normal_halfs=1 server::nr_extra_halfs=0 server::penalty_shoot_outs=0 " \
                   "server::half_time=10"

        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        datas = data.read()
        datas = datas.split(",")
        data.close()
        if datas[5] == "off":
            inp += " server::game_logging=false"
        if datas[7] == "off":
            inp += " server::text_logging=false"
        cmd.append(inp)
        print("\n\033[38;5;14mloading now...")
        time.sleep(0.5)
        start(cmd, 0)


def setting_en_loop():
    ok = 0
    cmd = []

    subp.reset()
    print("\033[0m\033[38;5;172m")
    v = open("./version")
    subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
    v.close()
    print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
    print("\033[38;5;39mSetting confirmation")
    # noinspection PyBroadException
    try:
        data = open("./config.conf", "r")
    except:
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
        data.close()
        data = open("./config.conf", "r")
    datas = data.read()
    data.close()
    datas = datas.split(",")
    datal = []
    for i in range(0, len(datas), 2):
        datat = []
        datat += datas[i:i + 2]
        datal.append(datat)
    table = Texttable()
    table.add_rows(datal)
    print(table.draw())
    subp.Input("Press Enter Key")

    subp.reset()
    while ok == 0:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
        print("\n\033[38;5;39mEasy soccer run list")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\nEnter back to return to the previous screen\n")
        inp = subp.Inputfile("\nTeam1 (yellow) Enter the team path or list name", textcolor="\033[38;5;11m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                # print(inp)
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:The name " + inp + " is not registered in the easy soccer "
                                                              "execution program. Check for typos.")
                    subp.Input("Press Enter to continue...", dot=False)
        else:
            ok = 2

    cmd.append(inp)
    # print(type(inp))
    # subp.Input("")
    if ok != 2:
        ok = 0
    subp.reset()
    while ok == 0 and ok != 2:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
        print("\n\033[38;5;39mEasy soccer run list")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\nEnter back to return to the previous screen\n\033[38;5;11mTeam1 "
                             "(yellow) Team of the path:" + cmd[0])
        inp = subp.Inputfile("\nEnter Team2 (red) team path or list name", textcolor="\033[38;5;9m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:The name " + inp + " is not registered in the easy soccer "
                                                              "execution program. Check for typos.")
                    subp.Input("Press Enter to continue...", dot=False)
        else:
            ok = 2

    if ok != 2:
        cmd.append(inp)
        subp.reset()
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp Easy soccer execution program")
        print("\n\033[38;5;11mTeam1 (yellow) Team of the path:" + cmd[0])
        print("\033[38;5;9mTeam2 (red) Team of the path:" + cmd[1])
        inp = subp.Input("\nEnter the server argument (blank if none)", textcolor="\033[38;5;9m")
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        df = data.read()
        data.close()
        inp += " server::auto_mode=true server::kick_off_wait=10 server::game_over_wait=10 server::connect_wait=1500 server::game_log_dir=" + \
               df.split(",")[9] + " server::text_log_dir=" + df.split(",")[9]
        loops = int(subp.Input("Specify the number of loops", textcolor="\033[38;5;9m"))
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        datas = data.read()
        datas = datas.split(",")
        data.close()
        if datas[5] == "off":
            inp += " server::game_logging=false"
        if datas[7] == "off":
            inp += " server::text_logging=false"
        cmd.append(inp)
        print("\n\033[38;5;14mloading now...")
        time.sleep(0.5)
        loop(cmd, loops)


def setting_jp_loop():
    ok = 0
    cmd = []

    subp.reset()
    print("\033[0m\033[38;5;172m")
    v = open("./version")
    subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
    v.close()
    print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
    print("\033[38;5;39m設定確認")
    # noinspection PyBroadException
    try:
        data = open("./config.conf", "r")
    except:
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
        data.close()
        data = open("./config.conf", "r")
    datas = data.read()
    data.close()
    datas = datas.split(",")
    datal = []
    for i in range(0, len(datas), 2):
        datat = []
        datat += datas[i:i + 2]
        datal.append(datat)
    table = Texttable()
    table.add_rows(datal)
    print(table.draw())
    subp.Input("Press Enter Key")

    subp.reset()
    while ok == 0:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
        print("\n\033[38;5;39m簡単サッカー実行リスト")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\n前画面に戻る場合はbackと入力\n")
        inp = subp.Inputfile("\nTeam1(黄色)チームのパスまたはリストの名前を入力", textcolor="\033[38;5;11m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                # print(inp)
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:名前 " + inp + " は簡単サッカー実行プログラムに登録されていません。\n"
                                                        "また、そのようなファイルも存在しません。\nタイプミスをを確認してください")
                    subp.Input("Enterキーを押して続行...", dot=False)
        else:
            ok = 2

    cmd.append(inp)
    # print(type(inp))
    # subp.Input("")
    if ok != 2:
        ok = 0
    subp.reset()
    while ok == 0 and ok != 2:
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
        print("\n\033[38;5;39m簡単サッカー実行リスト")
        # noinspection PyBroadException
        try:
            data = open("./setting.conf", "r")
        except:
            data = open("./setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./setting.conf", "r")
        datas = data.read()
        data.close()
        datas = datas.split(",")
        datal = []
        for i in range(0, len(datas), 2):
            datat = []
            datat += datas[i:i + 2]
            datal.append(datat)
        table = Texttable()
        table.add_rows(datal)
        print(table.draw() + "\n前画面に戻る場合はbackと入力\n\033[38;5;11mTeam1(黄色)チームのパス:" + cmd[0])
        inp = subp.Inputfile("\nTeam2(赤色)チームのパスまたはリストの名前を入力", textcolor="\033[38;5;9m")

        if inp != "back":
            i = 0
            try:
                while datas[i] != inp:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                i += 1
                inp = datas[i]
                ok = 1
            except:
                if os.path.isfile(inp):
                    ok = 1
                else:
                    print("\033[38;5;9mERR:名前 " + inp + " は簡単サッカー実行プログラムに登録されていません。\n"
                                                        "また、そのようなファイルも存在しません。\nタイプミスをを確認してください")
                    subp.Input("Enterキーを押して続行...", dot=False)
        else:
            ok = 2

    if ok != 2:
        cmd.append(inp)
        subp.reset()
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10mcszp 簡単サッカー実行プログラム")
        print("\n\033[38;5;11mTeam1(黄色)チームのパス:" + cmd[0])
        print("\033[38;5;9mTeam2(赤色)チームのパス:" + cmd[1])
        inp = subp.Input("\nサーバーの引数を入力（ない場合は空欄）", textcolor="\033[38;5;9m")
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        df = data.read()
        data.close()
        inp += " server::auto_mode=true server::kick_off_wait=10 server::game_over_wait=10 server::connect_wait=1500 server::game_log_dir=" + \
               df.split(",")[9] + " server::text_log_dir=" + df.split(",")[9]
        loops = int(subp.Input("\nやる回数を指定", textcolor="\033[38;5;9m"))
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
            data.close()
            data = open("./config.conf", "r")
        datas = data.read()
        datas = datas.split(",")
        data.close()
        if datas[5] == "off":
            inp += " server::game_logging=false"
        if datas[7] == "off":
            inp += " server::text_logging=false"
        cmd.append(inp)
        print("\n\033[38;5;14mloading now...")
        time.sleep(0.5)
        loop(cmd, loops)
