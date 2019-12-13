# -*- coding: utf-8 -*-

import subprocess, sys, platform, time, importlib, subp

try:
    from texttable import *
except:
    v = open("./version")
    print("\033[2Jcszp " + v.read())
    v.close()
    print(
        "\033[1mERR:\033[0mtexttable package is not installed.\ncszp (easy soccer run program) requires texttable.\n"
        "Execute the following command and try again.\n\033[38;5;11msudo apt install python3-pip && pip3 install texttable"
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
        "Execute the following command and try again.\n\033[38;5;11msudo apt install python3-pip && pip3 install tqdm"
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
        "Execute the following command and try again.\n\033[38;5;11msudo apt install python3-pip && pip3 install matplotlib"
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
        "Execute the following command and try again.\n\033[38;5;11msudo apt install python3-pip && pip3 install pandas"
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
        table = Texttable()
        table.add_rows([["box1", "box2", "box3"],
                        ["test", 1234567890, 3.1415926535],
                        ["test2", 123454321, 54e+2]])
        print("\n" + table.draw())
    else:
        sys.stdout.write("\033[38;5;9m\033[1m[FAILD] ")
        print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
        print("\033[38;5;9m\033[1mERR:\033[0mThis program requires python3.2 or higher version.")
        sys.exit()

    # main
    import cszp_menu

    try:
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
            r = cszp_menu.menu_jp()
        else:
            r = cszp_menu.menu_en()
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
    table = Texttable()
    table.add_rows([["box1", "box2", "box3"],
                    ["test", 1234567890, 3.1415926535],
                    ["test2", 123454321, 54e+2]])
    print("\n" + table.draw())
    print("\n\n\033[38;5;2mloading Now...")
    time.sleep(0.75)
    print("stoped.")
    time.sleep(0.25)
    subp.reset()
    if r == 2:
        main()
    elif r == 3:
        importlib.reload(cszp_menu)
        main()


if __name__ == '__main__':
    main()
