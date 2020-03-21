import json

import cuitools


def plugin_text(lang, text):
    return list(map(lambda n: json.load(open(n + "/setup.json"))[text], lang.pluginlist))


def plugin(lang):
    print("\033[0m")
    select = cuitools.printlist("select plugin", plugin_text(lang, "name"))
    if select != -1:
        sselect = 0
        while True:

            printtext = [
                lang.lang("名前:") + plugin_text(lang, "name")[select],
                lang.lang("バージョン:") + plugin_text(lang, "version")[select],
                lang.lang("管理者:") + plugin_text(lang, "author")[select],
                lang.lang("管理者のメールアドレス:") + plugin_text(lang, "author_email")[select],
                ""
            ]
            if sselect == 0:
                printtext.append(">> " + lang.lang("前ページへ戻る(ホーム)"))
                printtext.append("   " + lang.lang("説明を読む"))
            else:
                printtext.append("   " + lang.lang("前ページへ戻る(ホーム)"))
                printtext.append(">> " + lang.lang("説明を読む"))
            # print(printtext)
            cuitools.box(lang.lang("詳細情報") + " " + plugin_text(lang, "name")[select], printtext)
            k = cuitools.Key()
            if k == "\x1b":
                cuitools.Key()
                k = cuitools.Key()
                if k == "B":
                    if sselect < 1:
                        sselect += 1
                elif k == "A":
                    if sselect > 0:
                        sselect -= 1
            elif k == "\n":
                if sselect == 0:
                    break
                else:
                    cuitools.printlist(lang.lang("説明を読む"), plugin_text(lang, "description")[select].splitlines(), False)
