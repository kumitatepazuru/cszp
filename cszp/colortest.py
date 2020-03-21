# -*- coding: utf-8 -*-


def colortest():
    for i in range(256):
        print("\033[38;5;" + str(i) + "mhello world! ・・・・" + str(i))
