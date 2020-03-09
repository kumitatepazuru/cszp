# -*- coding: utf-8 -*-

import importlib
import json
import locale
import os
import platform
import subprocess
import sys
import time

import cszp_lang

try:
    from texttable import *
except:
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
except:
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
except:
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
except:
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
except:
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
        v = open("./version")
        subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
        v.close()
    except:
        v = open("./version")
        print("\033[2Jcszp " + v.read())
        v.close()
        print(
            "\033[1mERR:\033[0mfiglet package is not installed.\ncszp (easy soccer run program) requires figlet.\nExecute "
            "the following command and try again.\n\033[38;5;11msudo apt install figlet "
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

    if not os.path.isdir("html_logs"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: html_logs")
        os.mkdir("html_logs")
    if not os.path.isdir("csvdata"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: csvdata")
        os.mkdir("csvdata")
    if not os.path.isdir("config"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: config")
        os.mkdir("config")
    if not os.path.isdir("plugins"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: plugins")
        os.mkdir("plugins")
    # main
    import cszp_menu

    try:
        if not os.path.isfile("lang"):
            file = open("lang.json")
            lang_list = json.load(file)
            file.close()
            langf = open("lang", "w")
            langn = [k for k, v in lang_list.items() if v == locale.getlocale()[0].lower() + ".lang"]
            if len(langn) == 1:
                langf.write(langn[0])
            else:
                langf.write("1")
            langf.close()
        lang = cszp_lang.lang()
        r = cszp_menu.menu(lang)
    except KeyboardInterrupt:
        print("INFO:PROGRAM IS STOP!")
        r = 0

    #  stop
    subp.reset()
    print("\033[0m\033[38;5;172m")
    v = open("./version")
    subprocess.check_call("figlet -ctk cszp " + v.read(), shell=True)
    v.close()
    sys.stdout.write("\033[38;5;10m\033[1m[OK] ")
    print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
    print("\033[38;5;2mloading Now...")
    print("\n\n\033[38;5;2mloading Now...")
    time.sleep(0.75)
    print("stoped.")
    time.sleep(0.25)
    subp.reset()
    if r == 2 or r == 3:
        importlib.reload(cszp_menu)
        main()


if __name__ == '__main__':
    main()
