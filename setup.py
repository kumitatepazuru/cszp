import sys,subprocess
try:
    argv2 = sys.argv[1]
except:
    argv2 = "/opt"

print("file downloading...")
print("During unzip the file...")
#passwd = (getpass.getpass() + '\n').encode()
subprocess.check_output("sudo mkdir -p "+argv2+"/cszp && sudo cp ./sources/* "+argv2+"/cszp", shell=True)
subprocess.check_output("sudo chmod a+rw "+argv2+"/cszp",shell=True)
subprocess.check_output("sudo bash -c 'echo cd "+argv2+"/cszp/ > "+argv2+"/cszp/cszp.sh && echo python3 "+argv2+"/cszp/main.py >> "+argv2+"/cszp/cszp.sh && chmod 777 "+argv2+"/cszp/cszp.sh && ln -sf "+argv2+"/cszp/cszp.sh /usr/bin/cszp'",shell=True)
print("completed!")
