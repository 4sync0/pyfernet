#checks repo update
import requests as r
import subprocess

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
    subprocess.run("sudo rm repo/lastcheck.txt", shell=True)
    
    #save in file
    with open("repo/lastcheck.txt", "w") as f:
        f.write(last_data)



#NOTE: make file compatibility for windows
#NOTE: make an automatic backup for some stuff like the storage.json file