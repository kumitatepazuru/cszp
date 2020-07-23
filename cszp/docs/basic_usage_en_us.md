## Usage.
cszp has introduced the same interactive system as the command line. As shown in the following images, the program can be executed only by making selections and so on.
![photo](https://cdn-ak.f.st-hatena.com/images/fotolife/k/kumitatepazuru/20200621/20200621185025.png)

## Explanation of commands on the menu screen.

### start command.
Execute the rcssserver. The arguments are auto-populated by a question which we will explain later.

### test command.
Similar to the start command, but this checks if the program can or will run It is made to be able to do so. The game time is set to 200tick. We'll talk about it later.

### setting command
Configure cszp. We will explain the details later.

### reset command.
If the configuration file is corrupted or does not start, use this command to initialize the settings and then use It is not possible to restore it. Cannot restore.

### loop command.
If you run rcssserver a specified number of times and set the result, you can save it to a csv file and save it to If you set up the synch mode, you can run it. I'll explain later.

### lang command.
Change the language. Current languages supported are Japanese and English. 

### server commands.
You can check the data of past matches. We will explain later.

### plugin command.
You can view and install plugin information. I'll explain about it later.

### about command.
Information and installation of cszp and PC can be checked. It will be explained later.

### help command.
You can check the usage of cszp and other information.

### exit command
Quit the program by pressing Ctrl+C (if you do this while it's running, it will cause a problem) (Possibly)
 
## I can't start it.

 * If the program stops with a warning similar to the one in the image below, press the Enter key to stop the program. It can run. This is caused by extra or non-existent plugins in the plugins folder. This is displayed when the user makes a request for a new item.
![photo](https://cdn-ak.f.st-hatena.com/images/fotolife/k/kumitatepazuru/20200621/20200621185709.png)