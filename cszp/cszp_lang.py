import json
import os


class lang:
    def __init__(self):
        file = open("lang")
        ld = file.read()
        file.close()
        file = open("lang.json")
        self.lang_list = json.load(file)
        file.close()

        self.enable_lang = self.lang_list[ld]
        path = "./plugins/"
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        self.files = ["./list.json"]
        self.pluginlist = []
        langs = ["./language/" + self.enable_lang]
        for i in files_dir:
            if os.path.isfile("./plugins/" + i + "/list.json") and os.path.isfile("./plugins/" + i + "/setup.json") \
                    and os.path.isfile("./plugins/" + i + "/__init__.py"):
                setupf = open("./plugins/" + i + "/setup.json")
                setupd = json.load(setupf)
                if "name" in setupd and "version" in setupd and "author" in setupd and "author_email" in setupd and \
                        "description" in setupd:
                    self.files.append("./plugins/" + i + "/list.json")
                    self.pluginlist.append("./plugins/" + i)
                    langs.append("./plugins/" + i + "/language/" + self.enable_lang)

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
