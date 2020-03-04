import json


class lang:
    def __init__(self):
        file = open("lang")
        ld = file.read()
        file.close()
        file = open("lang.json")
        self.lang_list = json.load(file)
        file.close()

        self.enable_lang = self.lang_list[ld]
        file = open("./language/" + self.enable_lang)
        self.ld = file.read()

    def lang(self, text):
        split = self.ld.split("\n")
        after = []
        for t in text.split("\n"):
            # print(t)
            if t != "":
                if t in split:
                    after.append(split[split.index(t) + 1])
                else:
                    raise SyntaxError("そのような文字列はLangファイル内に見つかりませんでした:" + t)
            else:
                after.append("")
        return "\n".join(after)
