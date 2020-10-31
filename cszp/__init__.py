import logging
import os
import sys

sys.path.append(os.getcwd())
os.chdir(os.path.abspath(os.path.dirname(__file__)))

try:
    os.mkdir("logs")
except FileExistsError:
    pass

logging.basicConfig(format='[%(asctime)s] - %(filename)s > %(name)s > %(lineno)d [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG, filename="logs/cszp_log.log", filemode="w")

logging.info("level: DEBUG")
logging.debug("Running in module mode.")


def main():
    logger = logging.getLogger("main")
    print("\033[38;5;2mloading Now...")
    logger.info("loading Now...")
    print("1/7")
    logger.debug("set python path:" + os.getcwd())
    import json
    logger.debug("imported json module")
    print("\033[1A2/7")
    import locale
    logger.debug("imported locale module")
    print("\033[1A3/7")
    import platform
    logger.debug("imported platform module")
    print("\033[1A4/7")
    from cszp.cszp_module import Open, terminal, figlet, error_dump, Input
    logger.debug("imported Open, terminal, figlet, error_dump, Input at cszp.cszp_module")
    print("\033[1A5/7")
    from cszp import cszp_menu
    logger.debug("imported cszp_menu at cszp")
    print("\033[1A6/7")
    import cuitools as subp
    logger.debug("imported cuitools module")
    print("\033[1A7/7")
    subp.reset()
    logger.debug("imported subp module")
    print("\033[1;1H\033[0m\033[38;5;172m")
    logger.info("cszp version " + open("./version").read())
    ver = open("./version")
    figlet("cszp " + ver.read())
    # noinspection PyBroadException
    print("")
    logger.info("python ver:" + platform.python_version())
    logger.info("PYTHON-IMPLEMENTATION:" + platform.python_implementation())
    logger.info("PLATFORM:" + platform.platform())
    logger.info("SYSTEM:" + platform.system() + " " + platform.machine())
    if int(sys.version_info[0]) == 3 and int(sys.version_info[1]) >= 6 and int(sys.version_info[2]) >= 1:
        sys.stdout.write("\033[38;5;10m\033[1m[OK] ")
        print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
    else:
        print("\033[0m\033[38;5;2mpythonVersion\033[38;5;7m:\033[38;5;6m" + platform.python_version())
        print("\033[38;5;9m\033[1m[ERR] \033[0mThis program requires python3.6.1 or higher version.")
        logger.error("This program requires python3.6.1 or higher version.")
        logger.critical("cszp exited.")
        sys.exit()

    if not os.path.isdir("config"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: config")
        logger.info("Create directory: config")
        os.mkdir("config")
    if not os.path.isfile("config/hogo.json"):
        print("\033[38;5;4m[INFO]\033[0mCreate file: config/hogo.json")
        logger.info("Create file: config/hogo.json")
        tmp = open("config/hogo.json","w")
        tmp.write("[]")
        tmp.close()
    if not os.path.isfile("config/plus.txt"):
        print("\033[38;5;4m[INFO]\033[0mCreate file: config/plus.txt")
        logger.info("Create file: config/plus.txt")
        open("config/plus.txt","w").close()
    module = Open()
    if not os.path.isdir("html_logs"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: html_logs")
        logger.info("Create directory: html_logs")
        os.mkdir("html_logs")
    data = module.Open("./config/config.conf")
    path = data.read().splitlines()[0].split(",")[7]
    data.close()
    if not os.path.isdir(path):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: csvdata")
        logger.info("Create directory: csvdata")
        os.mkdir(path)
    if not os.path.isdir("plugins"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: plugins")
        logger.info("Create directory: plugins")
        os.mkdir("plugins")
    if not os.path.isdir("teams"):
        print("\033[38;5;4m[INFO]\033[0mCreate directory: teams")
        logger.info("Create directory: teams")
        os.mkdir("teams")

    # main

    if not os.path.isfile("lang"):
        file = open("language/lang.json")
        lang_list = json.load(file)
        file.close()
        langf = open("lang", "w")
        langn = [k for k, n in lang_list.items() if n == locale.getlocale()[0].lower() + ".lang"]
        if len(langn) == 1:
            logger.info("setlang:", langn[0])
            langf.write(langn[0])
        else:
            logger.info("setlang:1")
            langf.write("1")
        langf.close()
    lang = terminal()
    logger.info("inited")
    lang.autostart(lang)
    logger.info("autostart executed")
    Input = Input()
    try:
        logger.info("start menu")
        cszp_menu.menu(lang, module, Input)
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    except Exception:
        error_dump(lang, "CSZP PROGRAM ERROR",True)

    #  stop
    subp.reset()
    logger.info("cszp exited.")
    print("\033[38;5;10mgood bye!")


if __name__ == '__main__':
    main()
else:
    print("\033[38;5;4m[OK]\tThank you for using cszp.")
    print("\033[38;5;2m[NOTE]\tRunning in module mode.\n")
