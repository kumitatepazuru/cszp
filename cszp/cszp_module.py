import json
import locale
import logging
import os
import shutil
import subprocess
import sys
from io import StringIO

import cuitools
import cuitools as subp
from pyfiglet import Figlet
from importlib import import_module

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.completion import WordCompleter

from cszp import cszp_lang
import requests
from tqdm import tqdm


def figlet(text, font="larry3d"):
    print(
        Figlet(
            font=font,
            justify="center",
            width=shutil.get_terminal_size()[0]
        ).renderText(text)
    )


class lexer(Lexer):
    def __init__(self, color):
        self.color = color

    def lex_document(self, document):
        def get_line(lineno):
            return list(map(lambda n: (self.color, n), document.lines[lineno]))

        return get_line


class Input:
    def __init__(self):
        self.session = PromptSession()

    def Input(self, text, normal=False, textcolor="#89e324", dotcolor="#ffffff", usercolor="#75a0d1", dot=True,
              word=None):
        if word is not None:
            word = WordCompleter(word)
        if dot:
            text = [
                (textcolor + " bold" * normal, text),
                (dotcolor, ":")
            ]
        else:
            text = [
                (textcolor + " bold" * normal, text),
            ]
        if word is None:
            inp = self.session.prompt(text, lexer=lexer(usercolor), auto_suggest=AutoSuggestFromHistory())
        else:
            inp = self.session.prompt(text, lexer=lexer(usercolor), completer=word,
                                      auto_suggest=AutoSuggestFromHistory())
        return inp


def killsoccer(rcss=True):
    if rcss:
        try:
            while len(subprocess.check_output("pidof rcssserver", shell=True).decode("utf-8").split()) != 0:
                subprocess.check_output("killall rcssserver", shell=True)
        except subprocess.CalledProcessError:
            pass
    try:
        while len(subprocess.check_output("pidof soccerwindow2-qt4", shell=True).decode("utf-8").split()) != 0:
            subprocess.check_output("killall soccerwindow2-qt4", shell=True)
    except subprocess.CalledProcessError:
        pass


class Open:
    def __init__(self):
        self.writelist = {
            "config": "soccerwindow2start,on,rcglog output,on,rcllog output,on,logfile output," +
                      os.path.expanduser("~") + "/csvdata",
            "setting": "name,command"
        }
        self.hogo = json.load(open("config/hogo.json"))
        with open("config/plus.txt") as f:
            self.plus = f.read()

    def Open(self, file, mode="r"):
        if os.path.isfile(file):
            data = open(file, mode)
        else:
            data = open(file, "w")
            data.write(self.writelist[os.path.splitext(os.path.basename(file))[0]])
            data.close()
            data = open(file, "r")
        if os.path.splitext(os.path.basename(file))[0] == "setting":
            data = StringIO(data.read() + self.plus)
        return data


class terminal(cszp_lang.lang):
    def question(self, key, note="cszp 簡単サッカー実行プログラム", inp=True):
        title = []
        description = []
        cmd = []
        for j in self.files:
            listf = open(j)
            listd = json.load(listf)
            listf.close()
            if key in listd:
                for i in listd[key]:
                    title.append(i["title"])
                for i in listd[key]:
                    description.append(self.lang(i["description"]))
                for i in listd[key]:
                    cmd.append(i["cmd"])

        titlemax = len(max(title, key=lambda n: len(n)))
        title = list(map(lambda n: n.ljust(titlemax), title))
        temp = self.lang(note) + "\n\n"
        for i in range(len(title)):
            temp += title[i] + " " * 4 + description[i] + "\n"
        if inp:
            temp += ">>> "
        return temp, cmd

    def searchcmd(self, key, text):
        hit = 0
        for j in self.files:

            listf = open(j)
            listd = json.load(listf)
            listf.close()
            if key in listd:
                for i in listd[key]:
                    if i["cmd"] == text.split(" ")[0]:
                        hit = 1
        return hit

    def functo(self, key, text):
        func = []
        path = []
        for j in self.files:
            listf = open(j)
            listd = json.load(listf)
            listf.close()
            if key in listd:
                for i in listd[key]:
                    # print(i["cmd"], text, i["cmd"] == text)
                    if i["cmd"] == text:
                        path.append(os.path.dirname(j))
                        func.append(os.path.dirname(j).replace(".", "").replace("/", ".")[1:] + ".__init__")
        return path, func

    def autostart(self, lang):
        plugin_list = self.functo("auto_start", "auto_start")
        for i in plugin_list[0]:
            sys.path.append(i)
        for i in plugin_list[1]:
            plugin = import_module(i)
            plugin.autostart(lang)


def download_files_progress(lang, file_urls):
    for url in file_urls:
        file_url = url
        try:
            res = requests.get(file_url, stream=True)
        except requests.exceptions.ConnectionError:
            cuitools.box("エラー", [lang.lang("この機能を使用するにはネットワーク接続が必要です。"),
                                 lang.lang("以下のサイトににアクセスできるかどうか確認してください。"), "https://raw.githubusercontent.com/",
                                 lang.lang("Enterキーを押して続行...")])
            k = ""
            while k != "\n":
                k = cuitools.Key()
            break
        file_size = int(res.headers.get('content-length', 0))
        pbar = tqdm(total=file_size, unit="B", unit_scale=True)
        with open("/tmp/" + url.split("/")[-1], 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()


def download_file_mem(lang, file_url):
    try:
        return requests.get(file_url).text
    except requests.exceptions.ConnectionError:
        cuitools.box("エラー", [lang.lang("この機能を使用するにはネットワーク接続が必要です。"),
                             lang.lang("以下のサイトににアクセスできるかどうか確認してください。"), "https://raw.githubusercontent.com/",
                             lang.lang("Enterキーを押して続行...")])
        k = ""
        while k != "\n":
            k = cuitools.Key()


def error_dump(lang, ERR_TYPE="CSZP PROGRAM ERROR",e=False):
    logger = logging.getLogger("error_dump")
    import traceback
    logger.error(ERR_TYPE)
    logger.error(traceback.format_exc())
    print("\033[0m")
    with open("logs/cszp_log.log") as f:
        print(f.read())
    print(lang.lang("ログを確認してください")+"\n"+os.getcwd() + "/logs/cszp_log.log\n"+"-"*50)
    if e:
        raise SystemError
    else:
        subp.Key()