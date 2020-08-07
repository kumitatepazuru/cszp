import cuitools
from cszp import to256_window



def Help(lang):
    help_file_name = ""
    while help_file_name != "***":
        help_list = {
            "cszpへようこそ！": "welcome_to_cszp",
            "基本的な使い方": "basic_usage",
            "start・test・loopコマンドの使い方": "basic_usage_2",
            "前ページへ戻る(ホーム)":"***"
        }
        keys = list(map(lang.lang,list(help_list.keys())))
        index = cuitools.printlist(lang.lang("cszpのヘルプの参照"),keys)
        help_file_name = list(help_list.values())[index]
        if help_file_name != "***":
            with open("./docs/" + help_file_name + "_" + lang.enable_lang_name + ".md") as f:
                to256_window(keys[index] + " / " + lang.lang("qキーで終了"), f.read(),
                             background_file="./docs/background.png")
