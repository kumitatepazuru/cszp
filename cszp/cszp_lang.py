import json
import os


def isfile(path):
    if os.path.isfile(path):
        print("\033[38;5;10m\033[1m[OK]\033[0m\tReview", os.path.basename(path))
        return True
    else:
        print("\033[38;5;3m[WARNING]\033[0m\tThe plug-in is missing a required file:", os.path.basename(path))
        return False


class inname:
    def __init__(self, listd):
        self.list = listd

    def inname(self, name):
        if name in self.list:
            print("\033[38;5;10m\033[1m[OK]\033[0m\tVerify the", name, "tag is present")
            return True
        else:
            print("\033[38;5;3m[WARNING]\033[0m\tRequired information has not been written. Please confirm.", name)
            return False


class lang:
    def __init__(self, noenter=False):
        file = open("lang")
        ld = file.read()
        file.close()
        file = open("language/lang.json")
        self.lang_list = json.load(file)
        file.close()

        self.enable_lang = self.lang_list[ld]
        self.enable_lang_name = self.lang_list[ld].split(".")[0]
        path = "./plugins/"
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        self.files = ["./list.json"]
        self.pluginlist = []
        langs = ["./language/" + self.enable_lang]
        for i in files_dir:
            print("\033[38;5;4m[INFO]\033[0mThere was", i, "in the plugins folder. Checking for plug-ins.")
            if isfile("./plugins/" + i + "/list.json") and isfile("./plugins/" + i + "/setup.json") \
                    and isfile("./plugins/" + i + "/__init__.py"):
                setupf = open("./plugins/" + i + "/setup.json")
                setupd = json.load(setupf)
                print("\033[38;5;4m[INFO]\033[0m\tI checked that all the necessary files are present. "
                      "Verify that the required information has been written.")
                c = inname(setupd)
                if c.inname("name") and c.inname("version") and c.inname("author") and c.inname("author_email") and \
                        c.inname("description"):
                    self.files.append("./plugins/" + i + "/list.json")
                    self.pluginlist.append("./plugins/" + i)
                    langs.append("./plugins/" + i + "/language/" + self.enable_lang)
                else:
                    if not noenter:
                        input("\nPress enter key to run cszp")
            else:
                if not noenter:
                    input("\nPress enter key to run cszp")

        self.ld = ""
        for i in langs:
            if os.path.isfile(i):
                file = open(i)
                self.ld += file.read() + "\n\n"

    def lang(self, text):
        split = self.ld.split("\n")
        after = []
        for t in text.split("\n"):
            # print(t)
            # print(t,split)
            if t != "":
                if t in split:
                    after.append(split[split.index(t) + 1])
                else:
                    after.append(t)
            else:
                after.append("")
        return "\n".join(after)
