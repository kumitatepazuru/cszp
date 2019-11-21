import shutil
import subprocess
import urllib.request

import subp


def update():
    subprocess.check_call("clear",shell=True)
    versionlog = urllib.request.urlopen("https://raw.githubusercontent.com/kumitatepazuru/cszp/master/versionlog")
    vlog = versionlog.read().decode("utf-8")
    vlog = vlog.split("\n")[0]
    v = open("./version")
    if vlog != v.read().split("\n")[0]:
        k = ""
        b = 0
        while k != "\n":
            terminal_size = shutil.get_terminal_size()
            x = terminal_size[0]
            y = terminal_size[1]
            text1 = "Software Update!"
            text2 = "NEW version " + vlog + "!"
            text3 = "Update_Now Read_changelog do_nothing"
            tmp = text3.split(" ")
            text3 = ""
            for i in tmp:
                if tmp[b] == i:
                    text3 += "\033[7m" + i + "\033[0m "
                else:
                    text3 += i + " "
            text3 = text3[:len(text3) - 1]
            x1 = int(x / 2 - len(text1) / 2)
            y1 = int(y / 2 - 1)
            x2 = int(x / 2 - len(text2) / 2)
            y2 = y1 + 1
            x3 = int(x / 2 - len("Update_Now Read_changelog do_nothing") / 2)
            y3 = y1 + 2
            print("\033[" + str(y1) + ";" + str(x1) + "H" + text1)
            print("\033[" + str(y2) + ";" + str(x2) + "H" + text2)
            print("\033[" + str(y3) + ";" + str(x3) + "H" + text3 + "\033[0m")
            k = subp.Key()
            if k == "\x1b":
                subp.Key()
                k = subp.Key()
                if k == "C":
                    b += 1
                    if b > 2:
                        b = 2
                if k == "D":
                    b -= 1
                    if b < 0:
                        b = 0
        v.close()
        versionlog.close()

        if b == 0:
            subprocess.check_output("reset", shell=True)
            print("file downloading...")
            urllib.request.urlretrieve("https://github.com/kumitatepazuru/cszp/archive/master.zip",
                                       "/tmp/cszp.zip")
            print("During unzip the file...")
            subprocess.check_output("unzip /tmp/cszp.zip && sudo mv sources/* ./", shell=True)
            print("completed!")
            return 1
        elif b == 1:
            subprocess.check_output("reset", shell=True)
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/kumitatepazuru/cszp/master/changelog-cszp.txt",
                "/tmp/changelog.txt")
            changelog = open("/tmp/changelog.txt")
            print(changelog.read())
            changelog.close()
            subp.Input("\nPress Enter Key")
            subprocess.check_call("reset",shell=True)
            update()
