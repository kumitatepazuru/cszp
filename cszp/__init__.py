import os
import subprocess
import sys

sys.path.append(os.getcwd())
os.chdir(os.path.abspath(os.path.dirname(__file__)))
try:
    import cuitools as subp

    subp.reset()
    print("\033[1;1H\033[0m\033[38;5;172m")
    ver = open("./version")
    subprocess.check_call("figlet -ctk cszp " + ver.read(), shell=True)
    ver.close()
    print("\033[38;5;2mloading Now...")
except Exception:
    ver = open("./version")
    print("\033[2Jcszp " + ver.read())
    ver.close()
    print(
        "\033[1mERR:\033[0mfiglet package is not installed.\ncszp (easy soccer run program) requires figlet."
        "\nExecute the following command and try again.\n\033[38;5;11msudo apt install figlet "
    )
    sys.exit()

import json
import locale
import platform
import shutil

import cszp.cszp_module
from cszp.cszp_module import Open, terminal
from cszp.cszp_markdown import to256_window
from cszp import cszp_menu

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


module = Open()


def main():
    # noinspection PyBroadException
    print("")
    if int(sys.version_info[0]) == 3 and int(sys.version_info[1]) >= 6 and int(sys.version_info[2]) >= 1:
        sys.stdout.write("\033[38;5;10m\033[1m[OK] ")
        print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
    else:
        sys.stdout.write("\033[38;5;9m\033[1m[ERR] ")
        print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
        print("\033[38;5;9m\033[1mERR:\033[0mThis program requires python3.6.1 or higher version.")
        sys.exit()

    if not os.path.isdir("config"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: config")
        os.mkdir("config")
    data = module.Open("./config/config.conf")
    path = data.read().splitlines()[0].split(",")[7]
    data.close()
    if not os.path.isdir("html_logs"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: html_logs")
        os.mkdir("html_logs")
    if not os.path.isdir(path):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: csvdata")
        os.mkdir(path)
    if not os.path.isdir("plugins"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: plugins")
        os.mkdir("plugins")

    # main

    if not os.path.isfile("lang"):
        file = open("language/lang.json")
        lang_list = json.load(file)
        file.close()
        langf = open("lang", "w")
        langn = [k for k, n in lang_list.items() if n == locale.getlocale()[0].lower() + ".lang"]
        if len(langn) == 1:
            langf.write(langn[0])
        else:
            langf.write("1")
        langf.close()
    lang = terminal()
    lang.autostart(lang)
    Input = cszp.cszp_module.Input()
    if not os.path.isfile("start"):
        with open("start", "w") as f:
            f.write("1")
        with open("./docs/welcome_to_cszp_" + lang.enable_lang_name + ".md") as f:
            to256_window(lang.lang("cszpへようこそ！") + " / " + lang.lang("qキーで終了"), f.read())
    try:
        cszp_menu.menu(lang, module, Input)
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    except Exception:
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
        subp.box(lang.lang("エラー"),
                 [temp.splitlines()[0], lang.lang("ログを確認してください"), "", os.getcwd() + "/errorlog.log", "",
                  lang.lang("Enterキーを押して続行...")])
        k = ""
        while k != "\n":
            k = subp.Key()

    #  stop
    subp.reset()
    print("\033[38;5;10mgood bye!")


if __name__ == '__main__':
    main()
