import os
import shutil
import subprocess
from importlib import import_module, reload

import cuitools as subp
from texttable import *


def setting(lang):
    subp.reset()
    inp = ""
    while not lang.searchcmd("setting", inp):
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n\n\033[1m\033[38;5;10m" + lang.lang("cszp 簡単サッカー実行プログラム"))
        print("\n\033[38;5;39m" + lang.lang("簡単サッカー実行リスト"))
        # noinspection PyBroadException
        try:
            data = open("./config/setting.conf", "r")
        except FileNotFoundError:
            data = open("./config/setting.conf", "w")
            data.write("name,command")
            data.close()
            data = open("./config/setting.conf", "r")
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
        print(table.draw() + "\n\n")

        print("\033[38;5;39m" + lang.lang("設定"))
        # noinspection PyBroadException
        try:
            data = open("./config/config.conf", "r")
        except FileNotFoundError:
            data = open("./config/config.conf", "w")
            data.write(
                "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.path.expanduser(
                    "~") +
                "/csvdata")
            data.close()
            data = open("./config/config.conf", "r")
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
        print(table.draw() + "\n\n")

        inp = subp.Input(lang.question("setting", "※  注 [文字列] は引数を表します。 文字列は引数名です。"), dot=False)
        if not lang.searchcmd("setting", inp):
            print("\033[38;5;9m" + lang.lang("ERR:そのようなコマンドはありません。"))
            subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)

    try:
        if inp == "back":
            pass

        elif inp.split(' ')[0] == "add":
            data = open("./config/setting.conf", "r")
            datas = data.read()
            data.close()
            datas += "," + inp.split(' ')[1] + "," + inp.split(' ')[2]
            data = open("./config/setting.conf", "w")
            data.write(datas)
            data.close()
            setting(lang)

        elif inp.split(' ')[0] == "remove":
            data = open("./config/setting.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            i = 0
            try:
                while datas[i] != inp.split(" ")[1]:
                    i += 2
                if i < 2:
                    raise TypeError("data_ERROR")
                del datas[i:i + 2]
                datat = datas
                datas = ""
                for i in datat:
                    datas += i + ","
                datas = datas[:len(datas) - 1]
                data = open("./config/setting.conf", "w")
                data.write(datas)
                data.close()
            except TypeError:
                print("\033[38;5;9m" + lang.lang("ERR:名前"), inp.split(" ")[1], lang.lang(
                    "は簡単サッカー実行リストに登録されていません。\nタイプミスを確認してください"))
                subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)
            setting(lang)

        elif inp.split(' ')[0] == "soccerwindow2":
            data = open("./config/config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[1] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[1] = "off"
            else:
                print("\033[38;5;9m" + lang.lang("ERR:使える引数はONまたはOFFです。\nタイプミスを確認してください"))
                subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config/config.conf", "w")
            data.write(datas)
            data.close()
            setting(lang)

        elif inp.split(' ')[0] == "automake":
            data = open("./config/config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[3] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[3] = "off"
            else:
                print("\033[38;5;9m" + lang.lang("ERR:使える引数はONまたはOFFです。\nタイプミスを確認してください"))
                subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config/config.conf", "w")
            data.write(datas)
            data.close()
            setting(lang)

        elif inp.split(' ')[0] == "rcg":
            data = open("./config/config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[5] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[5] = "off"
            else:
                print("\033[38;5;9mERR:使える引数はONまたはOFFです。\nタイプミスを確認してください")
                subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config/config.conf", "w")
            data.write(datas)
            data.close()
            setting(lang)

        elif inp.split(' ')[0] == "rcl":
            data = open("./config/config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[7] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[7] = "off"
            else:
                print("\033[38;5;9mERR:使える引数はONまたはOFFです。\nタイプミスを確認してください")
                subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config/config.conf", "w")
            data.write(datas)
            data.close()
            setting(lang)

        elif inp.split(' ')[0] == "fileout":
            data = open("./config/config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            datas[9] = inp.split(" ")[1]
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config/config.conf", "w")
            data.write(datas)
            data.close()
            setting(lang)
        else:

            plugin = import_module(lang.functo("setting", inp)[1])
            reload(plugin)
            try:
                plugin.plugin(lang)
            except Exception:
                import traceback
                temp = "PLUGIN ERROR\ncszp=" + open("version").read() + "\n"
                file = open("./errorlog.log", "w")
                temp += "---------- error log ----------\n" + traceback.format_exc() + "\n"
                temp += "---------- computer information ----------\nwhich python3 : " + shutil.which(
                    'python3') + "\n" + "\n".join(map(lambda n: "=".join(n), list(os.environ.items())))
                temp += "\n\n---------- file list ----------\n" + subprocess.check_output("ls -al", shell=True).decode(
                    "utf-8")
                file.write(temp)
                file.close()
                print("\033[0m")
                subp.box(lang.lang("エラー"), [temp.splitlines()[0], lang.lang("ログを確認してください"), "", "errorlog.log", "",
                                            lang.lang("Enterキーを押して続行...")])
                k = ""
                while k != "\n":
                    k = subp.Key()
            setting(lang)
    except IndexError:
        print("\033[38;5;9m" + lang.lang("ERR:引数がありません。タイプミスを確認してください"))
        subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)
        setting(lang)
