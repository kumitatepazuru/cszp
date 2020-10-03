import glob
import json
import os
import shutil
import subprocess
import zipfile

import cuitools
from prompt_toolkit.shortcuts import button_dialog
from tqdm import tqdm

from cszp import cszp_module
from cszp.cszp_module import terminal


def plugin_text(lang, text):
    return list(map(lambda n: json.load(open(n + "/setup.json"))[text], lang.pluginlist))


def gen_rand_str_hex(length):
    import os
    import hashlib
    buf = ''
    while len(buf) < length:
        buf += hashlib.md5(os.urandom(100)).hexdigest()
    return buf[0:length]


def plugin(module, lang):
    print("\033[0m")
    select = cuitools.printlist(lang.lang("プラグインを選択"), plugin_text(lang, "name") + [
        lang.lang("バイナリファイルデータの追加・変更"), lang.lang("プラグインを追加"), lang.lang("前ページへ戻る(ホーム)")])
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
        while True:
            cuitools.reset()
            print(lang.lang("必要なデータをダウンロード中..."))
            data_list = cszp_module.download_file_mem(lang,
                                                      "https://raw.githubusercontent.com/kumitatepazuru/Soccer-binary"
                                                      "-files-for-cszp "
                                                      "/master/data.json")
            if data_list is not None:
                data_list = json.loads(data_list)
                text_list = list(map(lambda n: n["text"], data_list))
                folder_list = list(map(lambda n: n["folder"], data_list))
                url_list = list(map(lambda n: n["url"], data_list))
                team_data_list = list(map(lambda n: n["data"], data_list))
                num = cuitools.printlist(lang.lang("バイナリファイルデータの追加・変更"), text_list + [lang.lang("前ページへ戻る")])
                if num == len(data_list):
                    break
                else:
                    while True:
                        if os.path.isfile("config/" + folder_list[num]):
                            result = button_dialog(
                                title=lang.lang("詳細情報") + "/" + text_list[num],
                                text="download URL:" + url_list[num] + "\n" + lang.lang("インストール済み"),
                                buttons=[
                                    (lang.lang('前ページへ戻る'), True),
                                    (lang.lang("選手一覧"), None)
                                ]
                            ).run()
                            if result:
                                break
                            elif result is None:
                                cuitools.reset()
                                print("\n".join(json.loads(cszp_module.download_file_mem(lang, team_data_list[num]))))
                                input(lang.lang("Enterキーを押して続行..."))
                        else:
                            result = button_dialog(
                                title=lang.lang("詳細情報") + "/" + text_list[num],
                                text="download URL:" + url_list[num] + "\n" + lang.lang("未インストール"),
                                buttons=[
                                    (lang.lang('前ページへ戻る'), True),
                                    (lang.lang("インストールする"), False),
                                    (lang.lang("選手一覧"), None)
                                ]
                            ).run()
                            if result:
                                break
                            elif result is False:
                                cuitools.reset()
                                print(lang.lang("必要なデータをダウンロード中...") + lang.lang("これには数分~数十分かかることがあります。") + "\n")
                                print(url_list[num])
                                cszp_module.download_files_progress(lang, [url_list[num]])
                                print("\n" + lang.lang("データを解凍中...") + lang.lang("これには数分~数十分かかることがあります。"))
                                h = ""
                                while h == "" or os.path.isdir("teams/" + h):
                                    h = gen_rand_str_hex(8)
                                with zipfile.ZipFile("/tmp/" + folder_list[num] + ".zip") as existing_zip:
                                    existing_zip.extractall("/tmp")
                                try:
                                    cmd = ["unzip", "-od", "/tmp", "/tmp/" + folder_list[num] + ".zip"]
                                    print(" ".join(cmd))
                                    subprocess.check_call(cmd)
                                except FileNotFoundError:
                                    while True:
                                        cuitools.box(lang.lang("エラー"), [lang.lang("この機能を使用するにはunzipをインストールする必要があります。"),
                                                                        lang.lang("Enterキーを押して続行...")])
                                        if cuitools.Key() == "\n":
                                            break
                                    continue
                                with open(
                                        "/tmp/Soccer-binary-files-for-cszp-" + folder_list[num] + "/hogo.json") as f:
                                    with open("config/hogo.json") as F:
                                        data = json.load(F)
                                        tmp = json.load(f)
                                        tmp = list(map(lambda n: "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./teams/" + h +
                                                                 "/libs ./teams/" + h + "/" + n, tmp))
                                        data += tmp
                                    with open("config/hogo.json", "w") as F:
                                        json.dump(data, F)
                                    with open(
                                            "/tmp/Soccer-binary-files-for-cszp-" + folder_list[
                                                num] + "/team.json") as F:
                                        tmp2 = json.load(F)
                                        data = ""
                                        for i, j in zip(tmp2, tmp):
                                            data += "," + i + "," + j
                                        F = module.Open("./config/plus.txt", "a")
                                        F.write(data)
                                os.mkdir("teams/" + h)
                                print("\n" + lang.lang("データをコピー中..."))
                                for i in tqdm(glob.glob(
                                        "/tmp/Soccer-binary-files-for-cszp-" + folder_list[num] + "/teams/*")):
                                    shutil.copytree(i, "teams/" + h + "/" + i.split("/")[-1])
                                os.mkdir("teams/" + h + "/libs")
                                for i in tqdm(
                                        glob.glob("/tmp/Soccer-binary-files-for-cszp-" + folder_list[num] + "/libs/*")):
                                    shutil.copy(i, "teams/" + h + "/libs")
                                with open("config/" + folder_list[num], "w") as f:
                                    f.write(h)
                                # module = cszp_module.Open()
                                input("\n" + lang.lang("Enterキーを押して続行..."))

                            elif result is None:
                                cuitools.reset()
                                print("\n".join(json.loads(cszp_module.download_file_mem(lang, team_data_list[num]))))
                                input("\n" + lang.lang("Enterキーを押して続行..."))
                cuitools.reset()
                print("")
            else:
                break

        plugin(module, lang)
    elif select == len(plugin_text(lang, "name")) + 1:
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
                plugin(module, lang)
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

    elif select == len(plugin_text(lang, "name")) + 2:
        pass
