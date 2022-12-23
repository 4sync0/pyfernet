#this file is to add necessary code that needs to be runned before everything else

from os import chdir,  access, X_OK
import sys
import subprocess
import os.path

if __name__ == "__main__":
    #sets the working directory to wherever this file is
    chdir(os.path.dirname(__file__))

    #makes alias only if first time

    try: open("true.txt") #exists, not first time
    except Exception: #doesn't exist, first time, runs alias script
        FileNotFoundError
        subprocess.run(["/home/partypie/encryption/alias_setup.sh"], shell=True)
        with open("true.txt", "w") as f:
            f.write("This file exists to check if the script runs for the first time or not, to run alias_setup.sh or only once")

    #give every shell script executable perms only if they dont have it

    #alias_setup.sh
    if access("alias_setup.sh", X_OK):
        pass
    else:
        subprocess.run(["sudo -v chmod +x alias_setup.sh"])
    
    #rmdict_cmd.sh
    if access("STORAGE/rmdict_cmd.sh", X_OK):
        pass
    else:
        subprocess.run(["sudo -v chmod +x rmdict_cmd.sh"])


    #finally gets to fernet.py
    import fernet



    #PUT HERE BASH SCRIPT
    #error handling
    #compatibility issues