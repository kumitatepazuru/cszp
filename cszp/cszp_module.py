import json
import os
import subprocess

from cszp import cszp_lang


def killsoccer():
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
    try:
        while True:
            serverpid = subprocess.check_output("ps o pid,cmd | grep -E 'python3.*http.*20000' | grep -v grep",
                                                shell=True).decode("utf-8").split("\n")[0].split(" ")[0]
            subprocess.check_output("kill " + serverpid, shell=True)
    except subprocess.CalledProcessError:
        pass


class Open:
    def __init__(self):
        self.writelist = {
            "config": "soccerwindow2start,on,automake,off,rcglog output,on,rcllog output,on,logfile output," +
                      os.path.expanduser("~") + "/csvdata",
            "setting": "name,command"
        }

    def Open(self, file):
        if os.path.isfile(file):
            data = open(file, "r")
        else:
            data = open(file, "w")
            data.write(self.writelist[os.path.splitext(os.path.basename(file))[0]])
            data.close()
            data = open(file, "r")
        return data


class terminal(cszp_lang.lang):
    def question(self, key, note="cszp 簡単サッカー実行プログラム"):
        title = []
        description = []
        for j in self.files:
            listf = open(j)
            listd = json.load(listf)
            listf.close()
            if key in listd:
                for i in listd[key]:
                    title.append(i["title"])
                for i in listd[key]:
                    description.append(self.lang(i["description"]))

        titlemax = len(max(title, key=lambda n: len(n)))
        title = list(map(lambda n: n.ljust(titlemax), title))
        temp = self.lang(note) + "\n\n"
        for i in range(len(title)):
            temp += title[i] + " " * 4 + description[i] + "\n"
        temp += ">>> "
        return temp

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
        func = None
        path = None
        for j in self.files:
            listf = open(j)
            listd = json.load(listf)
            listf.close()
            if key in listd:
                for i in listd[key]:
                    # print(i["cmd"], text, i["cmd"] == text)
                    if i["cmd"] == text:
                        path = os.path.dirname(j)
                        func = os.path.dirname(j).replace(".", "").replace("/", ".")[1:] + ".__init__"
        return path, func
