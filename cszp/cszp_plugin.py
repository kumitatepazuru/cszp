import json
import zipfile

import cuitools
from cszp.cszp_module import terminal


def plugin_text(lang, text):
    return list(map(lambda n: json.load(open(n + "/setup.json"))[text], lang.pluginlist))


def plugin(lang):
    print("\033[0m")
    select = cuitools.printlist(lang.lang("プラグインを選択"), plugin_text(lang, "name") + [lang.lang("プラグインを追加"),
                                                                                    lang.lang("前ページへ戻る(ホーム)")])
    if select != -1 and select < len(plugin_text(lang, "name")):
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
    elif select == len(plugin_text(lang, "name")):
        k = ""
        while k != "\n":
            cuitools.box(lang.lang("プラグインを追加"), [
                lang.lang("プラグインの追加を行います。"),
                lang.lang("プラグインの入ったzipファイルを選択してください。"),
                lang.lang("終了したい場合は次の画面に行ってからqキーを押してください。"),
                lang.lang("Enterキーを押して続行...")
            ])
            k = cuitools.Key()
        ok = None
        while ok is None:
            path = cuitools.Inputfilegui(lang.lang("プラグインの入ったzipファイルを選択（終了したい場合はQキー）"))
            if path == -1:
                plugin(lang)
                break
            elif path == -2:
                raise KeyboardInterrupt()
            else:
                cuitools.reset()
                try:
                    with zipfile.ZipFile(path) as existing_zip:
                        existing_zip.extractall('./plugins/')
                except zipfile.BadZipFile:
                    k = ""
                    while k != "\n":
                        cuitools.box(lang.lang("エラー"), [
                            lang.lang("zipファイルではありません。"),
                            lang.lang("Enterキーを押して続行...")
                        ], reset_=True)
                        k = cuitools.Key()
                else:
                    k = ""
                    lang = terminal(noenter=True)
                    lang.autostart(lang)
                    while k != "\n":
                        cuitools.box("完了", [
                            lang.lang("正常にプラグインが追加されました。"),
                            lang.lang("正常にプラグインが動作するか確認してください。"),
                            lang.lang("Enterキーを押して続行...")
                        ])
                        k = cuitools.Key()
                    ok = lang
        return ok

    elif select == len(plugin_text(lang, "name")) + 1:
        pass
