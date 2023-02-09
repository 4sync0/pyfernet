#checks repo update
import requests as r
import subprocess
import os
from LOGS import logs_setup as logger

#I am aware there are easies ways of doing these type of stuff, but for the sake of "training" Im doing it this way

#get api
comms = r.get("https://api.github.com/repos/Party-Pie/pyfernet/commits") 

#the data
data = comms.json()

#the one I need for the commits
last_data = data[0]["sha"]


#the lastest commit of this clone
with open("repo/lastcheck.txt", "r") as f:
    last_onfile = f.read()

#check if same to newest
if last_onfile == last_data:
    pass

else:
    #get last update
    subprocess.run("git pull", shell=True)
    #then delete last save
    if os.name == "posix": #linux & macos
        subprocess.run("sudo rm repo/lastcheck.txt", shell=True)
    elif os.name == "nt":
        subprocess.run("del repo/lastcheck.txt", shell=True)
    
    #save in file
    with open("repo/lastcheck.txt", "w") as f:
        f.write(last_data)


#check if update
if last_data != last_onfile:
    import repo.backup_handler
    logger.logging.debug(f"updated pyfernet. {last_onfile} -> {last_data}")
else:
    print("your pyfernet is up to date")
    pass