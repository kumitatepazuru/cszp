import json
import locale
import os
import shutil
import subprocess
import sys
import threading
import time

import cuitools as subp

from sources import cszp_lang


def run(cmd):
    subp.reset()
    out = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True)
    terminal_size = shutil.get_terminal_size()

    while out.poll() is None:
        if len(cmd) < terminal_size[0] - 7:
            print("\033[" + str(
                terminal_size[1]) + ";1H\033[2KCMD\t" + cmd,
                  end="")
        else:
            print("\033[" + str(
                terminal_size[1]) + ";1H\033[2KCMD\t" + cmd[:terminal_size[0] - 11] + "...",
                  end="")
        time.sleep(0.15)
    return out.communicate()[1].decode("utf-8")


def error(error_log):
    global error_
    error_ = 1
    log = open("../install.log", "w")
    log.write(error_log)
    log.close()
    errtext = [lang.lang("エラー"), lang.lang("インストール実行中にエラーが発生しました。"),
               lang.lang("このプログラムにroot権限を与えてください"),
               "install.log",
               ""]
    box(errtext)
    sys.exit()


def install():
    out = run("apt update")
    if out == '\nWARNING: apt does not have a stable CLI interface. Use with caution in scripts.\n\ndebconf: delaying package configuration, since apt-utils is not installed\n' \
            or out == '\nWARNING: apt does not have a stable CLI interface. Use with caution in scripts.\n\n' \
            or out == "":
        out = run("apt install -y figlet python3-tk")
        if out == '\nWARNING: apt does not have a stable CLI interface. Use with caution in scripts.\n\ndebconf: delaying package configuration, since apt-utils is not installed\n' \
                or out == '\nWARNING: apt does not have a stable CLI interface. Use with caution in scripts.\n\n' \
                or out == "":
            out = run("pip3 install -U pip && pip3 install -r ../requirements.txt")
            if out.split("\n")[0][:7] != "WARNING" and out.split("\n")[0][:7] != "":
                error(out)
            else:
                global ok
                ok = 1
        else:
            error(out)
    else:
        error(out)


def box(printtext):
    terminal_size = shutil.get_terminal_size()
    lentext = max(map(subp.width_kana, printtext))
    for i in range(len(printtext)):
        if i == 0:
            print("\033[" + str(int(terminal_size[1] / 2 - len(printtext) / 2 + i)) + ";" + str(
                int(terminal_size[0] / 2 - lentext / 2)) + "H┏" + subp.center_kana(printtext[i], lentext, "━") + "┓")
        elif i == len(printtext) - 1:
            print("\033[" + str(int(terminal_size[1] / 2 - len(printtext) / 2 + i)) + ";" + str(
                int(terminal_size[0] / 2 - lentext / 2)) + "H┗" + subp.center_kana(printtext[i], lentext, "━") + "┛")
        else:
            print("\033[" + str(int(terminal_size[1] / 2 - len(printtext) / 2 + i)) + ";" + str(
                int(terminal_size[0] / 2 - lentext / 2)) + "H┃" + subp.center_kana(printtext[i], lentext, " ") + "┃")


os.chdir("./sources/")

subp.reset()
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

printtext = ["Step2/1 Select Language", lang.lang("cszp 簡単サッカー実行プログラム セットアップウィザードへようこそ"),
             lang.lang("いくつかのステップでcszpをインストールしましょう")]
for i in range(len(lang.lang_list)):
    if lang.lang_list[str(i)] == lang.enable_lang:
        select = i
        printtext.append(">> " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])
    else:
        printtext.append("   " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])
printtext.append("")
k = ""
while k != "\n":
    box(printtext)
    k = subp.Key()
    if k == "\x1b":
        subp.Key()
        k = subp.Key()
        if k == "B":
            if select < len(lang.lang_list) - 1:
                select += 1
                langf = open("lang", "w")
                langf.write(str(select))
                langf.close()
                lang = cszp_lang.lang()
        elif k == "A":
            if select > 0:
                select -= 1
                langf = open("lang", "w")
                langf.write(str(select))
                langf.close()
                lang = cszp_lang.lang()

    printtext = ["Step3/1 Select Language", lang.lang("cszp 簡単サッカー実行プログラム セットアップウィザードへようこそ"),
                 lang.lang("いくつかのステップでcszpをインストールしましょう")]
    for i in range(len(lang.lang_list)):
        if i == select:
            printtext.append(">> " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])
        else:
            printtext.append("   " + os.path.splitext(os.path.basename(lang.lang_list[str(i)]))[0])

    printtext.append("")
    subp.reset()

k = ""
select = 0
while k != "\n":
    printtext = ["Step3/2 " + lang.lang("確認"), lang.lang("cszp の実行に必要なプログラムがあるか確認し"),
                 lang.lang("可能ならばインストールすることができます。"),
                 lang.lang("この操作をスキップすることもできます。"),
                 lang.lang("ただし、手動で必要なプログラムをインストールする必要があります。"),
                 lang.lang("cszp の実行に必要なプログラムがあるか確認しインストールしますか？")]
    if select == 0:
        printtext.append(">> " + lang.lang("はい"))
        printtext.append("   " + lang.lang("いいえ"))
    else:
        printtext.append("   " + lang.lang("はい"))
        printtext.append(">> " + lang.lang("いいえ"))
    printtext.append("")

    box(printtext)
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

    subp.reset()

if select == 0:
    k = ""
    while k != "\n":
        printtext = ["Step 3/2.5 " + lang.lang("確認"),
                     lang.lang("下記のソフトをインストールします。"),
                     lang.lang("インストール済みのものも表示されます"), "",
                     "figlet" + lang.lang("とその依存"),
                     "texttable matplotlib tqdm pandas urllib3 cuitools" + lang.lang("とその依存"), "",
                     lang.lang("インストールしますか？")]
        if select == 0:
            printtext.append(">> " + lang.lang("はい"))
            printtext.append("   " + lang.lang("いいえ"))
        else:
            printtext.append("   " + lang.lang("はい"))
            printtext.append(">> " + lang.lang("いいえ"))
        printtext.append("")
        box(printtext)
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
        subp.reset()

ok = 0
if select == 0:
    ok = 0
    th = threading.Thread(target=install)
    th.start()

error_ = 0
k = ""
text = "/opt/"
while k != "\n" and error_ == 0:
    subp.reset()
    printtext = ["Step 3/3 ", lang.lang("インストールするパスを選択"), text, ""]
    box(printtext)
    k = subp.Key()
    if k == "\x7f":
        if len(text) > 1:
            text = text[:len(text) - 1]
    elif k == "\n":
        pass
    else:
        text += k

if error_ == 1:
    sys.exit()
subp.reset()
if select == 0:
    while ok == 0 and error_ == 0:
        box(["Loading...", "Welcome to cszp!", ""])
        time.sleep(0.2)
    if error_ == 1:
        sys.exit()

subp.reset()
box([lang.lang("インストール中..."), "Welcome to cszp!", ""])
os.chdir("../")
subprocess.check_output("mkdir -p " + text + "/cszp && cp -r ./sources/* " + text + "/cszp", shell=True)
subprocess.check_output("chmod a+rw " + text + "/cszp", shell=True)
subprocess.check_output(
    "bash -c 'echo cd " + text + "/cszp/ > " + text + "/cszp/cszp.sh && echo LANG=C.UTF-8 python3 " + text + "/cszp/main.py >> " + text + "/cszp/cszp.sh && chmod 755 " + text + "/cszp/cszp.sh && ln -sf " + text + "/cszp/cszp.sh /usr/bin/cszp'",
    shell=True)
k = ""
while k != "\n":
    subp.reset()
    box([lang.lang("インストール成功"), "Welcome to cszp!", ">> OK", ""])
    k = subp.Key()
os.remove(text + "/cszp/lang")
