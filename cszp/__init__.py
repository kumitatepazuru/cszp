# -*- coding: utf-8 -*-

import importlib
import json
import locale
import os
import platform
import shutil
import subprocess
import sys
import time

from cszp import cszp_lang

os.chdir(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
try:
    from texttable import *
except ModuleNotFoundError:
    v = open("./version")
    print("\033[2Jcszp " + v.read())
    v.close()
    print(
        "\033[1mERR:\033[0mtexttable package is not installed.\ncszp (easy soccer run program) requires texttable.\n"
        "Execute the following command and try again.\n\033[38;5;11mpip3 install texttable"
    )
    sys.exit()

try:
    import cuitools as subp
except ModuleNotFoundError:
    v = open("./version")
    print("\033[2Jcszp " + v.read())
    v.close()
    print(
        "\033[1mERR:\033[0mcuitools package is not installed.\ncszp (easy soccer run program) requires cuitools.\n"
        "Execute the following command and try again.\n\033[38;5;11mpip3 install cuitools"
    )
    sys.exit()

try:
    import tqdm
except ModuleNotFoundError:
    v = open("./version")
    print("\033[2Jcszp " + v.read())
    v.close()
    print(
        "\033[1mERR:\033[0mtqdm package is not installed.\ncszp (easy soccer run program) requires tqdm.\n"
        "Execute the following command and try again.\n\033[38;5;11mpip3 install tqdm"
    )
    sys.exit()

try:
    import matplotlib
except ModuleNotFoundError:
    v = open("./version")
    print("\033[2Jcszp " + v.read())
    v.close()
    print(
        "\033[1mERR:\033[0mmatplotlib package is not installed.\ncszp (easy soccer run program) requires matplotlib.\n"
        "Execute the following command and try again.\n\033[38;5;11mpip3 install matplotlib"
    )
    sys.exit()

try:
    import pandas
except ModuleNotFoundError:
    v = open("./version")
    print("\033[2Jcszp " + v.read())
    v.close()
    print(
        "\033[1mERR:\033[0mpandas package is not installed.\ncszp (easy soccer run program) requires pandas.\n"
        "Execute the following command and try again.\n\033[38;5;11mpip3 install pandas"
    )
    sys.exit()


def main():
    # noinspection PyBroadException
    try:
        subp.reset()
        print("\033[0m\033[38;5;172m")
        ver = open("./version")
        subprocess.check_call("figlet -ctk cszp " + ver.read(), shell=True)
        ver.close()
    except Exception:
        ver = open("./version")
        print("\033[2Jcszp " + ver.read())
        ver.close()
        print(
            "\033[1mERR:\033[0mfiglet package is not installed.\ncszp (easy soccer run program) requires figlet."
            "\nExecute the following command and try again.\n\033[38;5;11msudo apt install figlet "
        )
        sys.exit()
    time.sleep(1)

    print("")
    if int(sys.version_info[0]) == 3 and int(sys.version_info[1]) > 2:
        sys.stdout.write("\033[38;5;10m\033[1m[OK] ")
        print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
        time.sleep(0.2)
        print("\033[38;5;2mloading Now...")
        time.sleep(0.5)
    else:
        sys.stdout.write("\033[38;5;9m\033[1m[FAILD] ")
        print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
        print("\033[38;5;9m\033[1mERR:\033[0mThis program requires python3.2 or higher version.")
        sys.exit()

    if not os.path.isdir("config"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: config")
        os.mkdir("config")
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
    path = data.read().split(",")[9]
    if not os.path.isdir("html_logs"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: html_logs")
        os.mkdir("html_logs")
    if not os.path.isdir(path):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: csvdata")
        os.mkdir(path)
    if not os.path.isfile(path + "/data.csv"):
        print("\033[38;5;4m[INFO]\033[0mCreate file: data.csv")
        temp = open(path + "/data.csv", "w")
        temp.close()
    if not os.path.isdir("plugins"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: plugins")
        os.mkdir("plugins")

    # main
    from cszp import cszp_menu

    if not os.path.isfile("lang"):
        file = open("lang.json")
        lang_list = json.load(file)
        file.close()
        langf = open("lang", "w")
        langn = [k for k, n in lang_list.items() if n == locale.getlocale()[0].lower() + ".lang"]
        if len(langn) == 1:
            langf.write(langn[0])
        else:
            langf.write("1")
        langf.close()
    lang = cszp_lang.lang()
    try:
        r = cszp_menu.menu(lang)
    except KeyboardInterrupt:
        r = 0
    except EOFError:
        r = 0
    except Exception:
        r = 0
        import traceback
        temp = "CSZP PROGRAM ERROR\ncszp=" + open("version").read() + "\n"
        file = open("./errorlog.log", "w")
        temp += "---------- error log ----------\n" + traceback.format_exc() + "\n"
        temp += "---------- computer information ----------\nwhich python3 : " + shutil.which(
            'python3') + "\n" + "\n".join(map(lambda n: "=".join(n), list(os.environ.items())))
        temp += "\n\n---------- file list ----------\n" + subprocess.check_output("ls -al", shell=True).decode("utf-8")
        file.write(temp)
        file.close()
        print("\033[0m")
        subp.box(lang.lang("エラー"), [temp.splitlines()[0], lang.lang("ログを確認してください"), "", "errorlog.log", "",
                                    lang.lang("Enterキーを押して続行...")])
        k = ""
        while k != "\n":
            k = subp.Key()

    #  stop
    subp.reset()
    print("\033[0m\033[38;5;172m")
    ver = open("./version")
    subprocess.check_call("figlet -ctk cszp " + ver.read(), shell=True)
    ver.close()
    sys.stdout.write("\033[38;5;10m\033[1m[OK] ")
    print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
    print("\033[38;5;2mloading Now...")
    print("\n\n\033[38;5;2mloading Now...")
    time.sleep(0.5)
    print("stoped.")
    time.sleep(0.25)
    subp.reset()
    if r == 2 or r == 3:
        importlib.reload(cszp_menu)
        main()


if __name__ == '__main__':
    main()
