print("loading...")

import os
from cryptography.fernet import Fernet, InvalidToken
from random import randint
from sys import exit
import json
import subprocess

#imported files
from LOGS import logs_setup as logger
from STORAGE import pytojson
import file_moving


def menu(printdef: str, clear: bool): #PRINTDEF=NONE FOR NO PRINT
        if printdef: print(printdef)
        else: pass

        if clear: vars().clear() #clear all variables regardless of the parameter input
        else: pass

        while True:
        
            command: str = input("cmd->\t")

            if command == "/new":
                file: str = input("select file's relative path\tdont forget to place its extension at the end\n-->> ")
                file_checking = os.path.exists(file)
                if not file_checking:
                    print("file doesn't exist or you made a typo")
                    menu(None, False)
                    break
                else: pass

            elif command == "/genkey":
                #main global variables
                KEY = Fernet.generate_key()
                decoded_key = KEY.decode()

                id_num = randint(0, 1000)

                #check if already taken, if taken do again
                fileK_checking = os.path.exists(f"FERNETKEY{id_num}.txt")
                if fileK_checking: id_num = randint(0, 1000)
                
                else: pass

                with open(f"FERNETKEY{id_num}.txt", "wb") as f_key:
                    f_key.write(KEY)
                
                #check if the key has been generated or setted | true = generated; false = setted
                genkey_checkpoint = True

                print(f"\n->the key that just got generated is unique, use \"/sesion\" for more information\n")
                    
            elif command == "/encrypt":
                try:
                    #ENCRIPTION
                    fern = Fernet(key=KEY)
                    
                    with open(file, "rb") as raw_f:
                       origFile = raw_f.read()
                    
                    encrypt = fern.encrypt(origFile)
                    
                    with open(file, "wb") as f:
                       f.write(encrypt)
                    
                    print("\nsuccesfully encripted: ",file)
                except Exception: ValueError, print("invalid key")
        
            elif command == "/exit":
                exit("bai")
        
            elif command == "/decrypt":
                key_inp: str = input("input key:\n")
                try:
                    f = Fernet(key_inp) #THIS COULD CAUSE AN ERROR, WATCH!!
                    with open(file, "rb") as encrypted_f:
                        encrypted = encrypted_f.read()
                    
                    decrypted = f.decrypt(encrypted)
            
                    with open(f"decrypted_{file}", "wb") as decrypted_f:
                        decrypted_f.write(decrypted)
            
                    print(f"succesfully decripted {file}")
                except Exception: InvalidToken, print("invalid token")
                
            elif command == "/sesion":
                print("this sesion:\n")
                try: 
                    if genkey_checkpoint:
                        print(f"""
                         your key is: {decoded_key}
                         usable to decrypt: {file} only
                         stored in: FERNETKEY{id_num}.txt""")
                    elif not genkey_checkpoint:
                        print(f"""
                         your key is: {KEY}
                         usable to decrypt: {file} only
                         stored in: FERNETKEY{id_num}.txt""")

                except Exception: UnboundLocalError, print("no key generated during this sesion")
            
            elif command == "/save": #will only store the last change made into both "file" and "key" variables
                try:
                    #append key tuple
                    with open("STORAGE/storage_listKEY.py", "a") as f:
                        #check if it has the key in bytes or if the user just setted it, so it's not on bytes so it needs no decode
                        if genkey_checkpoint:
                            f.write(f", '{decoded_key}'")
                        elif not genkey_checkpoint:
                            f.write(f", '{KEY}'")               
                        
                    #append file tuple
                    with open("STORAGE/storage_listFILE.py", "a") as f:
                        f.write(f", '{file}'")
                except Exception: UnboundLocalError, print("no key specified")
                                 
            elif command == "/load":
                pytojson.start(True)

            elif command == "/destroydict":
                #running the bash script to clear x,y files
                subprocess.run(["STORAGE/rmdict_cmd.sh"], shell=True)
                #rewrite to place "N" on the lists to avoid errors while appending values & place the variable again
                with open("STORAGE/storage_listFILE.py", "w") as f:
                    f.write("filetuple = 'N'")

                with open("STORAGE/storage_listKEY.py", "w") as f:
                    f.write("keytuple = 'N'")

                print("successful")

            elif command == "/delvars":
                menu("deleting variable storage..",  True)
                #fix some errors

            elif command == "/changedir":
                file_moving.start()
        
            elif command == "/cwd": print(os.getcwd())

            elif command == "/logs":
                with open("LOGS/logs.log", "r") as f:
                    logs = f.read()
                print(logs)

            elif command == "/file":
                try: print(file)
                
                except Exception: UnboundLocalError, print("no file specified")
            
            elif command == "/setkey": #BE CAREFUL, IF YOU PLACE WRONG INFO. YOU'LL GET ERRORS LATER ON
                KEY = input("set the key if you've already got one:\n")
                #check if the key has been generated or setted | true = generated; false = setted
                genkey_checkpoint = False
            
            elif command == "/key":
                try:
                    if genkey_checkpoint:
                        print(decoded_key)
                    elif not genkey_checkpoint:
                        print(KEY)
                except Exception: UnboundLocalError, print("no key specified")

            elif command == "/tojson":
                #converts the dictionary stored in the storage directory to json file
                print("json file will get stored in: " + os.getcwd())

                #destroys last file and rewrites to avoid errors
                subprocess.run(["rm", "storage.json"])

                pytojson.start(False) #to update the new conent into the storage variable

                with open("storage.json", "x") as f:
                    json.dump(pytojson.storage, f, indent=2)

            elif command == "/jsonformat": menu("under construction", False)#change the json formatting

            else: print("unknown")

print("||fernet | p4tp5||\ntry \"/new\" command first to select a file")
    
menu(None, False) #PRINTDEF=NONE FOR NO PRINT