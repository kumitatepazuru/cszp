import os
import platform
import shutil
import subprocess
import sys
from importlib import import_module, reload

import cuitools as subp

from cszp import colortest, cszp_plugin, cszp_setting, cszp_soccer


def menu(lang):
    inp = ""
    subp.reset()
    while not lang.searchcmd("menu", inp):
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
        print("\n")
        inp = subp.Input(lang.question("menu"), dot=False)
        if not lang.searchcmd("menu", inp):
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
        data = open("./config/setting.conf", "w")
        data.write("name,command")
        data.close()
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
        temp = open(data.read().split(",")[9] + "/data.csv", "w")
        temp.close()
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
        select = 0
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
            pass
        r = menu(lang)
    elif inp == "plugin":
        cszp_plugin.plugin(lang)
        r = menu(lang)
    elif inp == "about":
        print("\033[0m")
        v = open("./version")
        vd = v.read().splitlines()[0]
        v.close()
        printtext = [
            "CSZP VER " + vd,
            "VERSION:" + vd,
            "",
            sys.version.splitlines()[0],
            sys.version.splitlines()[1],
            "Install Location:" + os.getcwd(),
            "",
            "SYSTEM:" + platform.system() + " " + platform.machine(),
            "PLATFORM:" + platform.platform(),
            "PC-NAME:" + platform.node(),
            "PYTHON-IMPLEMENTATION:" + platform.python_implementation()
        ]
        subp.printlist("about cszp", printtext)
        r = menu(lang)
    else:

        plugin = import_module(lang.functo("menu", inp)[1])
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
        r = menu(lang)

    return r
