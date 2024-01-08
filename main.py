# add necessary code that needs to be runned before everything else
import sys
import subprocess
from os import path, walk, chdir, getcwd, chdir, access, X_OK, name
import requests

last_dir = getcwd()

# THIS IS ALL TO FIX FILE IMPORTING
# sets the working directory to wherever this file is
def search_directory(target_directory):
    current_dir = path.dirname(path.realpath(__file__))
    for root, dirs, files in walk(current_dir):
        if target_directory in dirs:
            return path.abspath(path.join(root, target_directory))

    return path.abspath(path.join(current_dir))

chdir(search_directory("pyfernet"))

import LOGS.logs_setup as logger

if __name__ == "__main__":

    # makes alias only if first time
    try: open("true.txt")
    except Exception: # doesn't exist, first time; runs alias script & store commit
        # give every shell script executable perms only if they dont have it
        if name == "nt":
            pass
        else:
            subprocess.run(["sudo", "chmod", "+x", "./alias_setup_win.sh"], shell=True)
        # add alias_setup depending on OS
        if name == "posix":
            subprocess.run(["./alias_setup_unix.sh"], shell=True)
        elif name == "nt":
            subprocess.run(["./alias_setup_win.sh"], shell=True)

        logger.logging.info("setting alias")

        # repo info
        try: open("true.txt")
        except Exception:
            comms = requests.get("https://api.github.com/repos/4sync0/pyfernet/commits") 

            data = comms.json()

            in_commit = data[0]["sha"]

            with open("repo/lastcheck.txt", "w") as f:
                f.write(in_commit)
        
        
            with open("true.txt", "w") as f:
                f.write("This file exists to check if the script runs for the first time or not, to run alias_setup.sh or only once")


    import fernet

    chdir(last_dir)