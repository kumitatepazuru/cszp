# -*- coding: utf-8 -*-

import subp
import subprocess

from texttable import *


def setting_jp():
    subprocess.check_output("reset", shell=True)
    inp = ""
    while inp.split(' ')[0] != "add" and inp.split(' ')[0] != "remove" and inp != "back" \
            and inp.split(' ')[0] != "soccerwindow2" and inp.split(' ')[0] != "automake" \
            and inp.split(' ')[0] != "rcg" and inp.split(' ')[0] != "rcl" and inp.split(' ')[0] != "fileout":
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
        print(table.draw() + "\n\n")

        print("\033[38;5;39m設定")
        # noinspection PyBroadException
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output,/opt/cszp")
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
        print(table.draw() + "\n\n")

        inp = subp.Input("""※  注 [文字列] は引数を表します。 文字列は引数名です。
add [NAME] [COMMAND]    簡単サッカー実行リストの登録
remove [NAME]           簡単サッカー実行リストの削除
soccerwindow2 [ON/OFF]  soccerwindow2を試合時に自動起動するかどうか
automake [ON/OFF]       試合前に最適化用makeをかけるかどうか
rcg [ON/OFF]            rcgログを出力するかどうか
rcl [ON/OFF]            rclログを出力するかどうか
fileout                 logファイルの保存先を指定
back                    全ページへ戻る(ホーム)
>>>""", dot=False)
        if inp.split(' ')[0] != "add" and inp.split(' ')[0] != "remove" and inp != "back" \
                and inp.split(' ')[0] != "soccerwindow2" and inp.split(' ')[0] != "automake" \
                and inp.split(' ')[0] != "rcg" and inp.split(' ')[0] != "rcl" and inp.split(' ')[0] != "fileout":
            print("\033[38;5;9mERR:そのようなコマンドはありません。")
            subp.Input("Enterキーを押して続行...", dot=False)

    try:
        if inp == "back":
            pass

        elif inp.split(' ')[0] == "add":
            data = open("./setting.conf", "r")
            datas = data.read()
            data.close()
            data = open("./setting.conf", "w")
            datas += "," + inp.split(' ')[1] + "," + inp.split(' ')[2]
            data.write(datas)
            data.close()
            setting_jp()

        elif inp.split(' ')[0] == "remove":
            data = open("./setting.conf", "r")
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
                data = open("./setting.conf", "w")
                data.write(datas)
                data.close()
            except:
                print("\033[38;5;9mERR:名前 " + inp.split(" ")[1] + " は簡単サッカー実行プログラムに登録されていません。"
                                                                  "\nタイプミスをを確認してください")
                subp.Input("Enterキーを押して続行...", dot=False)
            setting_jp()

        elif inp.split(' ')[0] == "soccerwindow2":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[1] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[1] = "off"
            else:
                print("\033[38;5;9mERR:使える引数はONまたはOFFです。\nタイプミスをを確認してください")
                subp.Input("Enterキーを押して続行...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_jp()

        elif inp.split(' ')[0] == "automake":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[3] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[3] = "off"
            else:
                print("\033[38;5;9mERR:使える引数はONまたはOFFです。\nタイプミスをを確認してください")
                subp.Input("Enterキーを押して続行...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_jp()

        elif inp.split(' ')[0] == "rcg":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[5] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[5] = "off"
            else:
                print("\033[38;5;9mERR:使える引数はONまたはOFFです。\nタイプミスをを確認してください")
                subp.Input("Enterキーを押して続行...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_jp()

        elif inp.split(' ')[0] == "rcl":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[7] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[7] = "off"
            else:
                print("\033[38;5;9mERR:使える引数はONまたはOFFです。\nタイプミスをを確認してください")
                subp.Input("Enterキーを押して続行...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_jp()

        elif inp.split(' ')[0] == "fileout":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            datas[9] = inp.split(" ")[1]
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_jp()
    except IndexError:
        print("\033[38;5;9mERR:引数がありません。タイプミスを確認してください")
        subp.Input("Enterキーを押して続行...", dot=False)
        setting_jp()

def setting_en():
    subprocess.check_output("reset", shell=True)
    inp = ""
    while inp.split(' ')[0] != "add" and inp.split(' ')[0] != "remove" and inp != "back" \
            and inp.split(' ')[0] != "soccerwindow2" and inp.split(' ')[0] != "automake" \
            and inp.split(' ')[0] != "rcg" and inp.split(' ')[0] != "rcl" and inp.split(' ')[0] != "fileout":
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
        print(table.draw() + "\n\n")

        print("\033[38;5;39mSetting")
        # noinspection PyBroadException
        try:
            data = open("./config.conf", "r")
        except:
            data = open("./config.conf", "w")
            data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output,/opt/cszp")
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
        print(table.draw() + "\n\n")

        inp = subp.Input("""Note [String] represents the argument. The string is the argument name.
add [NAME] [COMMAND]    Easy soccer run list registration
remove [NAME]           Easy soccer run list deletion
soccerwindow2 [ON/OFF]  Whether soccerwindow2 is automatically started during the match
automake [ON/OFF]       Whether to apply optimization make before the game
rcg [ON/OFF]            Whether to output rcg log
rcl [ON/OFF]            Whether to output rcl log
fileout                 Specify where to save the log file
back                    Return to pages (Home)
>>>""", dot=False)
        if inp.split(' ')[0] != "add" and inp.split(' ')[0] != "remove" and inp != "back" \
                and inp.split(' ')[0] != "soccerwindow2" and inp.split(' ')[0] != "automake" \
                and inp.split(' ')[0] != "rcg" and inp.split(' ')[0] != "rcl" and inp.split(" ")[0] != "fileout":
            print("\033[38;5;9mERR:There is no such command.")
            subp.Input("Press Enter to continue...", dot=False)

    try:
        if inp == "back":
            pass

        elif inp.split(' ')[0] == "add":
            data = open("./setting.conf", "r")
            datas = data.read()
            data.close()
            data = open("./setting.conf", "w")
            datas += "," + inp.split(' ')[1] + "," + inp.split(' ')[2]
            data.write(datas)
            data.close()
            setting_en()

        elif inp.split(' ')[0] == "remove":
            data = open("./setting.conf", "r")
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
                data = open("./setting.conf", "w")
                data.write(datas)
                data.close()
            except:
                print("\033[38;5;9mERR:The name " + inp.split(" ")[1] + " is not registered in the easy soccer "
                                                                        "execution program. Check for typos.")
                subp.Input("Press Enter to continue...", dot=False)
            setting_en()

        elif inp.split(' ')[0] == "soccerwindow2":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[1] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[1] = "off"
            else:
                print("\033[38;5;9mERR:Available arguments are ON or OFF.\nCheck for typos.")
                subp.Input("Press Enter to continue...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_en()

        elif inp.split(' ')[0] == "automake":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[3] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[3] = "off"
            else:
                print("\033[38;5;9mERR:Available arguments are ON or OFF.\nCheck for typos.")
                subp.Input("Press Enter to continue...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_en()

        elif inp.split(' ')[0] == "rcg":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[5] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[5] = "off"
            else:
                print("\033[38;5;9mERR:Available arguments are ON or OFF.\nCheck for typos.")
                subp.Input("Press Enter to continue...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_en()

        elif inp.split(' ')[0] == "rcl":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            if inp.split(' ')[1].lower() == "on":
                datas[7] = "on"
            elif inp.split(' ')[1].lower() == "off":
                datas[7] = "off"
            else:
                print("\033[38;5;9mERR:Available arguments are ON or OFF.\nCheck for typos.")
                subp.Input("Press Enter to continue...", dot=False)
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_en()

        elif inp.split(' ')[0] == "fileout":
            data = open("./config.conf", "r")
            datas = data.read()
            datas = datas.split(",")
            data.close()
            datas[9] = inp.split(" ")[1]
            datat = datas
            datas = ""
            for i in datat:
                datas += i + ","
            datas = datas[:len(datas) - 1]
            data = open("./config.conf", "w")
            data.write(datas)
            data.close()
            setting_jp()
    except IndexError:
        print("\033[38;5;9mERR:IndexError")
        subp.Input("Press Enter to continue...", dot=False)
        setting_en()