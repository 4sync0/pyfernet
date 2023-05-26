#this file is to add necessary code that needs to be runned before everything else
import sys
import subprocess
from os import path, walk, chdir, getcwd, chdir, access, X_OK
import requests

last_dir = getcwd()

#THIS IS ALL TO FIX FILE IMPORTING
#sets the working directory to wherever this file is
def search_directory(target_directory):
    current_dir = path.dirname(path.realpath(__file__))
    for root, dirs, files in walk(current_dir):
        if target_directory in dirs:
            return path.abspath(path.join(root, target_directory))

    return path.abspath(path.join(current_dir))

chdir(search_directory("pyfernet"))

import LOGS.logs_setup as logger

if __name__ == "__main__":
    #makes alias only if first time

    try: open("true.txt") #exists, not first time
    except Exception: #doesn't exist, first time; runs alias script & store commit
        FileNotFoundError
        logger.logging.info("setting alias")
        subprocess.run(["./alias_setup.sh"])

        #get api
        comms = requests.get("https://api.github.com/repos/Party-Pie/pyfernet/commits") 
        
        #the data
        data = comms.json()
        
        #version
        in_commit = data[0]["sha"]

        with open("repo/lastcheck.txt", "w") as f:
            f.write(in_commit)
        

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

    #once done return back to last directory
    chdir(last_dir)

    #PUT HERE BASH SCRIPT
    #error handling
    #compatibility issues