import requests as r
import subprocess
import os
from LOGS import logs_setup as logger

# I am aware there are easies ways of doing these type of stuff, but for the sake of "training" Im doing it this way

# get api, data and specific commit
comms = r.get("https://api.github.com/repos/4sync0/pyfernet/commits") 

data = comms.json()

last_data = data[0]["sha"]


# the lastest commit of this clone
with open("repo/lastcheck.txt", "r") as f:
    last_onfile = f.read()

if last_onfile == last_data:
    pass

else:
    # get last update and  delete old
    subprocess.run(["git", "pull"])

    if os.name == "posix":
        subprocess.run(["sudo", "rm", "repo/lastcheck.txt"])
    elif os.name == "nt":
        subprocess.run(["del", "repo/lastcheck.txt"])
    
    with open("repo/lastcheck.txt", "w") as f:
        f.write(last_data)


# check if update
if last_data != last_onfile:
    import repo.backup_handler
    logger.logging.info(f"updated pyfernet. {last_onfile} -> {last_data}")
else:
    print("your pyfernet is up to date")
    pass