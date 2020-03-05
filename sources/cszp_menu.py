# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

import cuitools as subp

import colortest
import cszp_setting
import cszp_soccer
import cszp_update


def menu(lang):
    inp = ""
    Return = cszp_update.update()
    if Return == 1:
        return 3
    subp.reset()
    while inp != "start" and inp != "test" and inp != "setting" and inp != "exit" and inp != "colortest" \
            and inp != "reset" and inp != "lang" and inp != "loop" and inp != "server":
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n")
        inp = subp.Input(lang.lang("""
cszp 簡単サッカー実行プログラム

start       試合をする
test        テスト試合をする
setting     設定をする
reset       リセットをかける
loop        試合を複数回する
lang        Change language/言語を変更
server      過去のloopログをサーバーで確認
exit        終了する
>>>""") + " ", dot=False)
        if inp != "start" and inp != "test" and inp != "setting" and inp != "exit" and inp != "colortest" \
                and inp != "reset" and inp != "lang" and inp != "loop" and inp != "server":
            print("\033[38;5;9m" + lang.lang("ERR:そのようなコマンドはありません。"))
            subp.Input(lang.lang("Enterキーを押して続行..."), dot=False)
    if inp == "exit":
        return 1
    elif inp == "colortest":
        colortest.colortest()
        subp.Input(lang.lang("Enterキーを押して続行..."))
        r = menu(lang)
    elif inp == "setting":
        cszp_setting.setting(lang)
        r = menu(lang)
    elif inp == "reset":
        data = open("./setting.conf", "w")
        data.write("name,command")
        data.close()
        data = open("./config.conf", "w")
        data.write("soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," + os.getcwd())
        data.close()
        subp.Input("\n\n\033[38;5;214m" + lang.lang("リセットが完了しました。\nEnterキーを押して続行..."), dot=False)
        r = menu(lang)
    elif inp == "test":
        cszp_soccer.setting(lang, testmode=True)
        r = menu(lang)
    elif inp == "start":
        cszp_soccer.setting(lang)
        r = menu(lang)
    elif inp == "lang":
        terminal_size = shutil.get_terminal_size()
        printtext = ["Select Language"]
        for i in range(len(lang.lang_list)):
            if lang.lang_list[str(i)] == lang.enable_lang:
                select = i
                printtext.append(">> " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])
            else:
                printtext.append("   " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])
        printtext.append("")
        k = ""
        while k != "\n":
            lentext = max(map(len, printtext))
            for i in range(len(printtext)):
                if i == 0:
                    print("\033[" + str(int(terminal_size[1] / 2 + i)) + ";" + str(
                        int(terminal_size[0] / 2 - lentext / 2)) + "H┏" + printtext[i].center(lentext, '━') + "┓")
                elif i == len(printtext) - 1:
                    print("\033[" + str(int(terminal_size[1] / 2 + i)) + ";" + str(
                        int(terminal_size[0] / 2 - lentext / 2)) + "H┗" + printtext[i].center(lentext, '━') + "┛")
                else:
                    print("\033[" + str(int(terminal_size[1] / 2 + i)) + ";" + str(
                        int(terminal_size[0] / 2 - lentext / 2)) + "H┃" + printtext[i].center(lentext, ' ') + "┃")
            k = subp.Key()
            if k == "\x1b":
                subp.Key()
                k = subp.Key()
                if k == "B":
                    if select < len(lang.lang_list) - 1:
                        select += 1
                elif k == "A":
                    if select > 0:
                        select -= 1

            printtext = ["Select Language"]
            for i in range(len(lang.lang_list)):
                if i == select:
                    printtext.append(">> " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])
                else:
                    printtext.append("   " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])
            printtext.append("")

        langf = open("lang", "w")
        langf.write(str(select))
        langf.close()
        return 2
    elif inp == "loop":
        cszp_soccer.setting(lang, loopmode=True)
        r = menu(lang)
    elif inp == "server":
        print(lang.lang("Ctrl+Cで閲覧を終了します。"))
        try:
            subprocess.check_call("cd html_logs/ && python3 -m http.server 20000", shell=True)
        except KeyboardInterrupt:
            r = menu(lang)
    return r
