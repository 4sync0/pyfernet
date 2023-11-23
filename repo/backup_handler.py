import shutil
import os
import subprocess

# files that gets saved regardless of there being an update
truetxt = False
storagejson = False
logslog = False

home = os.path.expanduser("~")


if os.path.isfile("true.txt"):
    truetxt = True
else:
    pass

if input("do you want to save the storage? (.../pyfernet/storage.json)\t y/n \n") == "y":
    storagejson = True
else:
    pass

if input("do you want to save the logs? (.../pyfernet/LOGS/logs.log)\t y/n \n") == "y":
    logslog = True
else:
    pass

# True = save ; False = No save

print(f"""will be saved:\n
 true.txt: {truetxt}
 storage.json: {storagejson}
 logs.log {logslog}\n""")

confirm = input("Do you want to proceed with the update?\t y/n \n")

if confirm == "y":
    try:
        # save everything on the content folder & put it in home directory
        if storagejson: shutil.move("storage.json", "repo/content")
        else: pass

        if truetxt: shutil.move("true.txt", "repo/content")
        else: pass

        if logslog: shutil.move("LOGS/logs.log", "repo/content")
        else: pass


        shutil.move("repo", home)

    finally:
        # get lastest
        subprocess.run(["git", "pull", "https://github.com/Party-Pie/pyfernet"])

        # delete the new ones (only the ones that are already on the repo) & put files back
        if storagejson:
            os.remove("true.txt")
            shutil.move(f"{home}/content/storage.json", {os.getcwd()})
        else: pass

        if truetxt:
            os.remove("LOGS/storage.json")
            shutil.move(f"{home}/content/storage.json", "STORAGE")
        else: pass

        if logslog:
            os.remove("LOGS/logs.log")
            shutil.move(f"{home}/content/logs.log", "LOGS")
        else: pass
else:
    print("update cancelled")

# THIS IS CURRENTLY UNDER TESTS