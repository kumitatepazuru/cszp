import pygments.util
import cuitools
import shutil
import numpy as np
import mistune
from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter


class md_code:
    def __init__(self, text, lang=None):
        self.text = text
        if lang == "":
            self.lang = None
        else:
            self.lang = lang

    def tohtml(self):
        _max = max(list(map(cuitools.subp.width_kana, self.text.split("\n")))) + 7
        if self.lang is None:
            return "━" * _max + "\n⣿ " + "\n⣿ ".join(self.text.split("\n")) + "\n" + "━" * _max
        else:
            try:
                lexer = get_lexer_by_name(self.lang, stripall=True)
            except pygments.util.ClassNotFound:
                return "━" * _max + "\n⣿ " + "\n⣿ ".join(self.text.split("\n")) + "\n" + "━" * _max
            formatter = Terminal256Formatter(encoding='utf-8')
            return "━" * _max + "\n⣿ " + "\n⣿ ".join(
                highlight(self.text, lexer, formatter).decode("utf-8").split("\n")) + "\n" + "━" * _max


class to256_renderer(mistune.HTMLRenderer):
    def text(self, text):
        return text

    def link(self, link, text=None, title=None):
        if text is None:
            return link
        else:
            return "\033[38;5;2m" + text + ":" + link + "\033[0m"

    def image(self, src, alt="", title=None):
        if alt == "":
            return "\n\033[38;5;3m" + src + "\033[0m\n"
        else:
            return "\n\033[38;5;3m" + alt + ":" + src + "\033[0m\n"

    def emphasis(self, text):
        return "\033[3m" + text + "\033[0m"

    def strong(self, text):
        return "\033[1m" + text + "\033[0m"

    def codespan(self, text):
        return "\033[48;5;16m\033[38;5;1m" + text + "\033[0m"

    def linebreak(self):
        return "\n"

    def newline(self):
        return ""

    def inline_html(self, html):
        return html

    def paragraph(self, text):
        return text + "\n"

    def heading(self, text, level):
        if level == 1:
            return "\033[1m\033[38;5;9m" + text + "  " + "\033[0m\n\033[38;5;9m" + "━" * cuitools.subp.width_kana(
                text) + "\033[0m\n"
        elif level == 2:
            return "  \033[38;5;6m" + text + "  " + "\033[0m\n\033[38;5;6m  " + "─" * cuitools.subp.width_kana(
                text) + "\033[0m\n"
        elif level == 3:
            return "    \033[4m\033[1m\033[38;5;14m" + text + "\033[0m\n"
        elif level == 4:
            return "      \033[1m\033[38;5;2m" + text + "\033[0m\n"
        elif level == 5:
            return "        \033[38;5;11m" + text + "\033[0m\n"
        else:
            return "          \033[38;5;3m" + text + "\033[0m\n"

    def thematic_break(self):
        return "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    def block_text(self, text):
        return text

    def block_code(self, code, lang=None):
        code = md_code(code, lang)
        return code.tohtml() + "\n"

    def block_quote(self, text):
        return "⣿ " + "\n⣿ ".join(text.split("\n")) + "\n"

    def block_html(self, html):
        return html + "\n"

    def block_error(self, html):
        return "\033[38;5;1m" + html + "\033[0m\n"

    def list(self, text, ordered, level, start=None):
        return text + '\n'

    def list_item(self, text, level):
        return "\033[1m\033[38;5;4m# \033[0m " + text + '\n'

    def strikethrough(self, text):
        return "\033[9m" + text + "\033[0m"


def to256(text):
    markdown = mistune.create_markdown(renderer=to256_renderer(), plugins=['strikethrough'])
    return markdown(text)


def reload(text, to256_ok=True):
    terminal_size = shutil.get_terminal_size()
    tmp = []
    for i in to256(text).split("\n"):
        j = 1
        while len(i) > j:
            length = 0
            old_j = j
            while length < terminal_size[0] - 18 and len(i) > j:
                length = cuitools.subp.width_kana(i[old_j - 1:j])
                j += 1
            if len(i) > j:
                tmp.append(i[old_j - 1:j - 1])
            else:
                tmp.append(i[old_j - 1:j])
    return tmp


def scale_to_height(img, height):
    width = round(img.width * height / img.height)
    return img.resize((width, height))


def background(file):
    img = Image.open(file)
    terminal_size = list(shutil.get_terminal_size())
    terminal_size[0] /= 2
    img.thumbnail(terminal_size)
    img = np.array(img)
    for no, i in enumerate(img):
        print("")
        if no == 0:
            print("\033[1;1H", end="")
        for j in i:
            print("\033[48;2;" + str(j[0]) + ";" + str(j[1]) + ";" + str(j[2]) + "m  ", end="")
        print("\033[0m", end="")


def to256_window(title, text, reset=True, background_file=None, place="c"):
    terminal_size = shutil.get_terminal_size()
    if terminal_size[0] < 15:
        cuitools.reset()
        print("\033[1;1HThe screen is too small. Please make it bigger.")
        while terminal_size[0] < 15:
            terminal_size = shutil.get_terminal_size()

    tmp = reload(text)

    if reset:
        cuitools.reset()
    if background_file is not None:
        background(background_file)
    k = ""
    scroll = 0
    while k != "q":
        terminal_size = shutil.get_terminal_size()
        printtext = tmp[0 + scroll:terminal_size[1] - 4 + scroll]
        printtext.insert(0, title)
        printtext.append("")
        lentext = terminal_size[0] - 15
        if place == "c":
            y = int(terminal_size[1] / 2 - len(printtext) / 2)
            x = int(terminal_size[0] / 2 - lentext / 2)
        elif place == "n":
            y = 1
            x = int(terminal_size[0] / 2 - lentext / 2)
        elif place == "nw":
            y = 1
            x = 1
        elif place == "ne":
            y = 1
            x = terminal_size[0] - lentext - 1
        elif place == "e":
            y = int(terminal_size[1] / 2 - len(printtext) / 2)
            x = terminal_size[0] - lentext - 1
        elif place == "w":
            y = int(terminal_size[1] / 2 - len(printtext) / 2)
            x = 1
        elif place == "s":
            y = terminal_size[1] - len(printtext)
            x = int(terminal_size[0] / 2 - lentext / 2)
        elif place == "sw":
            y = terminal_size[1] - len(printtext)
            x = 1
        elif place == "se":
            y = terminal_size[1] - len(printtext)
            x = terminal_size[0] - lentext - 1
        else:
            raise IndexError("placeはc,n,nw,ne,e,w,s,sw,seのみ対応しています")
        for i in range(len(printtext)):
            if i == 0:
                print(
                    "\033[" + str(y + i) + ";" + str(x) + "H\033[0m┏" + cuitools.subp.ljust_kana(printtext[i], lentext,
                                                                                                 "━") + "┓")
            elif i == len(printtext) - 1:
                print("\033[" + str(y + i) + ";" + str(x) + "H┗" + cuitools.subp.ljust_kana(printtext[i], lentext,
                                                                                            "━") + "┛")
            else:
                print("\033[" + str(y + i) + ";" + str(x) + "H┃" + cuitools.subp.ljust_kana(printtext[i], lentext,
                                                                                            " ") + "┃")

        k = cuitools.Key()
        old_terminal_size = terminal_size
        terminal_size = shutil.get_terminal_size()
        if old_terminal_size != terminal_size:
            if scroll > len(tmp) - terminal_size[1] + 4:
                scroll = len(tmp) - terminal_size[1] + 1
            cuitools.reset()
            tmp = reload(text)
            if background_file is not None:
                background(background_file)
        if k == "\x1b":
            k = cuitools.Key()
            if k == "[":
                k = cuitools.Key()
                if k == "A":
                    if scroll != 0:
                        scroll -= 1
                if k == "B":
                    if scroll < len(tmp) - terminal_size[1] + 4:
                        scroll += 1
