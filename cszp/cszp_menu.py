import os
import platform
import shutil
import subprocess
import sys
from importlib import import_module, reload

import cuitools as subp

from cszp import colortest, cszp_plugin, cszp_setting, cszp_soccer, cszp_module, cszp_help


def menu(lang, module, Input):
    cszp_module.killsoccer()
    inp = ""
    subp.reset()
    while not lang.searchcmd("menu", inp):
        subprocess.check_call("clear", shell=True)
        print("\033[0m\033[38;5;172m")
        v = open("./version")
        cszp_module.figlet("cszp " + v.read())
        v.close()
        print("\n")
        q = lang.question("menu")
        inp = Input.Input(q[0], dot=False, normal=False, word=q[1])
        if not lang.searchcmd("menu", inp):
            print("\033[38;5;9m" + lang.lang("ERR:そのようなコマンドはありません。"))
            Input.Input(lang.lang("Enterキーを押して続行..."), dot=False)
    if inp == "exit":
        pass
    elif inp == "colortest":
        colortest.colortest()
        Input.Input(lang.lang("Enterキーを押して続行..."))
        menu(lang, module, Input)
    elif inp == "setting":
        cszp_setting.setting(lang, module,Input)
        menu(lang, module, Input)
    elif inp == "reset":
        data = open("./config/setting.conf", "w")
        data.write("name,command")
        data.close()
        Input.Input(lang.lang("\n\nリセットが完了しました。\nEnterキーを押して続行..."), dot=False, textcolor="#fdb100")
        menu(lang, module, Input)
    elif inp == "test":
        cszp_soccer.setting(lang,testmode=True, module=module, Input_=Input)
        menu(lang, module, Input)
    elif inp == "start":
        cszp_soccer.setting(lang, module=module,Input_=Input)
        menu(lang, module, Input)
    elif inp == "rrt":
        cszp_soccer.rrt(lang, module=module, Input_=Input)
        menu(lang, module, Input)
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
        lang = cszp_module.terminal(noenter=True)
        lang.autostart(lang)
        menu(lang, module, Input)
    elif inp == "loop":
        cszp_soccer.setting(lang, loopmode=True, module=module, Input_=Input)
        menu(lang, module, Input)
    elif inp == "server":
        print(lang.lang("Ctrl+Cで閲覧を終了します。"))
        try:
            subprocess.check_call("cd html_logs/ && python3 -m http.server 20000", shell=True)
        except KeyboardInterrupt:
            pass
        except subprocess.CalledProcessError:
            Input(lang.lang("Enterキーを押して続行..."))
        menu(lang, module, Input)
    elif inp == "plugin":
        tmp = cszp_plugin.plugin(lang)
        if tmp is not None:
            menu(tmp, module, Input)
        else:
            menu(lang, module, Input)
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
        menu(lang, module, Input)
    elif inp == "help":
        cszp_help.Help(lang)
        menu(lang, module, Input)
    elif inp == "window":
        try:
            subprocess.check_call("soccerwindow2")
        except KeyboardInterrupt:
            pass
        except subprocess.CalledProcessError:
            Input(lang.lang("Enterキーを押して続行..."))
        menu(lang, module, Input)
    else:
        sys.path.append(lang.functo("menu", inp)[0][0])
        plugin = import_module(lang.functo("menu", inp)[1][0])
        reload(plugin)
        try:
            plugin.plugin(lang, inp)
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
            subp.box(lang.lang("エラー"),
                     [temp.splitlines()[0], lang.lang("ログを確認してください"), "", os.getcwd() + "/errorlog.log", "",
                      lang.lang("Enterキーを押して続行...")])
            k = ""
            while k != "\n":
                k = subp.Key()
        menu(lang, module, Input)
