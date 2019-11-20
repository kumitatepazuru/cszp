# -*- coding: utf-8 -*-

import subprocess

import colortest
import cszp_setting
import cszp_soccer
import cszp_update
import subp


def menu_jp():
    inp = ""
    cszp_update.update()
    subprocess.check_output("reset", shell=True)
    while inp != "start" and inp != "test" and inp != "setting" and inp != "exit" and inp != "colortest" \
            and inp != "reset" and inp != "lang" and inp != "loop" and inp != "server":
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n")
        inp = subp.Input("""
cszp 簡単サッカー実行プログラム
   
start       試合をする
test        テスト試合をする
setting     設定をする
reset       リセットをかける
loop        試合を複数回する
lang        Change language/言語を変更
server      過去のloopログをサーバーで確認
exit        終了する
>>> """, dot=False)
        if inp != "start" and inp != "test" and inp != "setting" and inp != "exit" and inp != "colortest" \
                and inp != "reset" and inp != "lang" and inp != "loop" and inp != "server":
            print("\033[38;5;9mERR:そのようなコマンドはありません。")
            subp.Input("Enterキーを押して続行...", dot=False)
    if inp == "exit":
        pass
    elif inp == "colortest":
        colortest.colortest()
        subp.Input("press enter key")
        menu_jp()
    elif inp == "setting":
        cszp_setting.setting_jp()
        menu_jp()
    elif inp == "reset":
        data = open("./setting.conf", "w")
        data.write("name,command")
        data.close()
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output,/opt/cszp")
        data.close()
        subp.Input("\n\n\033[38;5;214mリセットが完了しました。\nEnterを押して続行...", dot=False)
        menu_jp()
    elif inp == "test":
        cszp_soccer.setting_jp(True)
        menu_jp()
    elif inp == "start":
        cszp_soccer.setting_jp(False)
        menu_jp()
    elif inp == "lang":
        try:
            data = open("lang", "r")
        except FileNotFoundError:
            data = open("lang", "w")
            data.write("1")
            data.close()
            data = open("lang", "r")
        datas = data.read()
        data.close()
        if datas == "1":
            datas = "0"
        else:
            datas = "1"
        data = open("lang", "w")
        data.write(datas)
        data.close()
        return 2
    elif inp == "loop":
        cszp_soccer.setting_jp_loop()
        menu_jp()
    elif inp == "server":
        print("Press Ctrl+C to Exit")
        try:
            subprocess.check_call("python3 -m http.server 6002",shell=True)
        except KeyboardInterrupt:
            menu_jp()
    return 1


def menu_en():
    inp = ""
    Return = cszp_update.update()
    if Return == 1:
        return 3
    subprocess.check_output("reset", shell=True)
    while inp != "start" and inp != "test" and inp != "setting" and inp != "exit" and inp != "colortest" \
            and inp != "reset" and inp != "lang" and inp != "loop" and inp != "server":
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n")
        inp = subp.Input("""
cszp Easy soccer execution program

start       Play a game
test        Play a test match
setting     Setting
loop        Multiple times in the match
reset       Apply a reset
lang        Change language/言語を変更
server      Check the previous loop log on the server
exit        Ends
>>> """, dot=False)
        if inp != "start" and inp != "test" and inp != "setting" and inp != "exit" and inp != "colortest" \
                and inp != "reset" and inp != "lang" and inp != "loop" and inp != "server":
            print("\033[38;5;9mERR:There is no such command.")
            subp.Input("Press Enter to continue...", dot=False)
    if inp == "exit":
        pass
    elif inp == "colortest":
        colortest.colortest()
        subp.Input("press enter key")
        menu_en()
    elif inp == "setting":
        cszp_setting.setting_en()
        menu_en()
    elif inp == "reset":
        data = open("./setting.conf", "w")
        data.write("name,command")
        data.close()
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output,/opt/cszp")
        data.close()
        subp.Input("\n\n\033[38;5;214mThe reset is complete.\nPress Enter to continue...", dot=False)
        menu_en()
    elif inp == "test":
        cszp_soccer.setting_en(True)
        menu_en()
    elif inp == "start":
        cszp_soccer.setting_en(False)
        menu_en()
    elif inp == "lang":
        try:
            data = open("lang", "r")
        except:
            data = open("lang", "w")
            data.write("1")
            data.close()
            data = open("lang", "r")
        datas = data.read()
        data.close()
        if datas == "1":
            datas = "0"
        else:
            datas = "1"
        data = open("lang", "w")
        data.write(datas)
        data.close()
        return 2
    elif inp == "loop":
        cszp_soccer.setting_en_loop()
        menu_en()
    elif inp == "server":
        print("Press Ctrl+C to Exit")
        try:
            subprocess.check_call("python3 -m http.server 6002",shell=True)
        except KeyboardInterrupt:
            menu_en()
    return 1
