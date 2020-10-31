import os
import platform
import shutil
import subprocess
import sys
import logging
from importlib import import_module, reload

import cuitools as subp

from cszp import colortest, cszp_plugin, cszp_setting, cszp_soccer, cszp_module
from cszp.cszp_module import error_dump


def menu(lang, module, Input):
    logger = logging.getLogger("menu")
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
            logger.warning(lang.lang("ERR:そのようなコマンドはありません。"))
            print("\033[38;5;9m" + lang.lang("ERR:そのようなコマンドはありません。"))
            Input.Input(lang.lang("Enterキーを押して続行..."), dot=False)
    if inp == "exit":
        pass
    elif inp == "colortest":
        logger.info("select colortest")
        colortest.colortest()
        logger.info("printed colortest")
        Input.Input(lang.lang("Enterキーを押して続行..."))
        menu(lang, module, Input)
    elif inp == "setting":
        logger.info("select setting")
        cszp_setting.setting(lang, module, Input)
        logger.info("exited setting")
        menu(lang, module, Input)
    elif inp == "reset":
        logger.info("select reset")
        os.remove("./config/*")
        shutil.rmtree("plugins")
        shutil.rmtree("teams")
        logger.info("reseted")
        Input.Input(lang.lang("\n\nリセットが完了しました。\nEnterキーを押して続行..."), dot=False, textcolor="#fdb100")
        logger.info("exited reset")
        menu(lang, module, Input)
    elif inp == "test":
        logger.info("select test")
        cszp_soccer.setting(lang, testmode=True, module=module, Input_=Input)
        logger.info("exited test")
        menu(lang, module, Input)
    elif inp == "start":
        logger.info("select start")
        cszp_soccer.setting(lang, module=module, Input_=Input)
        logger.info("exited start")
        menu(lang, module, Input)
    elif inp == "rrt":
        logger.info("select rrt")
        cszp_soccer.rrt(lang, module=module, Input_=Input)
        logger.info("exited rrt")
        menu(lang, module, Input)
    elif inp == "lang":
        terminal_size = shutil.get_terminal_size()
        printtext = ["Select Language"]
        select = 0
        logger.info("select lang")
        logger.info("list " + str(lang.lang_list))
        logger.info("length " + str(len(lang.lang_list)))
        logger.info("enable lang name " + lang.enable_lang_name)
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
        logger.info("reloaded")
        logger.info("select lang name " + lang.enable_lang_name)
        lang.autostart(lang)
        logger.info("autostart executed")
        logger.info("exited lang")
        menu(lang, module, Input)
    elif inp == "loop":
        logger.info("select loop")
        cszp_soccer.setting(lang, loopmode=True, module=module, Input_=Input)
        logger.info("exited loop")
        menu(lang, module, Input)
    elif inp == "server":
        logger.info("select server")
        print(lang.lang("Ctrl+Cで閲覧を終了します。"))
        try:
            logger.info("call", "cd html_logs/ && python3 -m http.server 20000")
            subprocess.check_call("cd html_logs/ && python3 -m http.server 20000", shell=True)
        except KeyboardInterrupt:
            pass
        except subprocess.CalledProcessError as e:
            logger.warning(e)
            Input(lang.lang("Enterキーを押して続行..."))
        logger.info("exited server")
        menu(lang, module, Input)
    elif inp == "plugin":
        logger.info("select plugin")
        tmp = cszp_plugin.plugin(module, lang)
        logger.info("exited plugin")
        if tmp is not None:
            menu(tmp, module, Input)
        else:
            menu(lang, module, Input)
    elif inp == "about":
        logger.info("select about")
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
        logger.info("exited about")
        menu(lang, module, Input)
    elif inp == "window":
        logger.info("select window")
        try:
            logger.info("call soccerwindow2")
            subprocess.check_call("soccerwindow2")
        except KeyboardInterrupt:
            pass
        except subprocess.CalledProcessError as e:
            logger.warning(e)
            Input(lang.lang("Enterキーを押して続行..."))
        logger.info("exited window")
        menu(lang, module, Input)
    else:
        logger.info("select other")
        sys.path.append(lang.functo("menu", inp)[0][0])
        plugin = import_module(lang.functo("menu", inp)[1][0])
        reload(plugin)
        logger.info("reload plugin module")
        try:
            logger.info("start plugin mode")
            plugin.plugin(lang, inp)
            logger.info("exited plugin mode")
        except Exception:
            error_dump(lang, "PLUGIN ERROR")
        logger.info("exited other")
        menu(lang, module, Input)
