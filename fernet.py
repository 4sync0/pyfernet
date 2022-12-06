print("loading...")

from cryptography.fernet import Fernet, InvalidToken
from random import randint
import os
from sys import exit
import json
from LOGS import logs_setup as logger

#encryption api
if "__main__" == __name__:
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

                id_num = randint(0, 100)
                
                print("\nkey & it's id generated..\n")
                   
                with open(f"FERNETKEY{id_num}.txt", "wb") as f_key:
                    f_key.write(KEY)
                
                #check if the key has been generated or setted | true = generated; false = setted
                genkey_checkpoint = True
                    
                fileK_checking = os.path.exists(f"FERNETKEY{id_num}.txt")
                if not fileK_checking: os.path.exists("|RANDINT GENERATION REPEATED| try again\n (there is 1 in 100 posibilities of getting this error, I appologize for your bad luck D:), or key limit exceeded (100)")
                
                else: print(f"\n->the key that just got generated is unique, use \"/keyinfo\" for more information\n")

            elif command == "/encrypt":
                #ENCRIPTION
                fern = Fernet(key=KEY)
                
                with open(file, "rb") as raw_f:
                   origFile = raw_f.read()
                
                encrypt = fern.encrypt(origFile)
                
                with open(file, "wb") as f:
                   f.write(encrypt)
                
                print("\nsuccesfully encripted: ",file)
        
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
        
            elif command == "/credits": print("""
             Made by P4rtyPi5#6988 -> discord|@p4rtypi5 -> Replit
             feel free to use this lil program for any use as long as credits are given
             made with certain modules and packages: sys, os, random and fernet.""")
                
            elif command == "/keyinfo":
                print("your sesion(sometimes information is wrong, look at:README.txt for more info):\n")
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
                                 
            elif command == "/load":
                from STORAGE import pytojson
                pytojson.user()
    
            elif command == "/decryptdict": menu("under construction", False) #DECRYPTS USING THE FILE SAVES. PASSING AS KEY, THE INPUT OF THE ID SAVED ON THE JSON
        
            elif command == "/destroydict": menu("under construction", False) #DELETES THE CONTENT INSIDE THE STORAGE FILE, IF THERE IS NO STORAGE SAVE FILE, PRINT ERROR

            elif command == "/delvars":
                menu("deleting variable storage..",  True)
                #fix some errors

            elif command == "/changedir":

                import file_moving
        
            elif command == "/cwd": print(os.getcwd())

            elif command == "/logs":
                with open("LOGS/fmLOGS", "r") as f:
                    logs = f.read()
                print(logs)

            elif command == "/check": menu("under construction", False) #check if value/key is on the storage dictionary, and if it is, it will print it's value/key

            elif command == "/file":
                try: print(file)
                
                except Exception: UnboundLocalError, menu("no file specified", False)
            
            elif command == "/setkey": #BE CAREFUL, IF YOU PLACE WRONG INFO. YOU'LL GET ERRORs LATER ON
                KEY = input("set the key if you've already got one:\n")
                #check if the key has been generated or setted | true = generated; false = setted
                genkey_checkpoint = False
            
            elif command == "/key":
                if genkey_checkpoint:
                    print(decoded_key)
                elif not genkey_checkpoint:
                    print(KEY)


            else: print("unknown")

    print("||fernet| p4tp5|| v.0.2b\ntry \"/new\" command first to select a file")
    commands = {
        "/new": "inputs a new file -> OTHER COMMANDS REQUIRE FROM THIS COMMAND|||RUN FIRST",
        "/genkey": "generates a key for decryption -> REQUIRES A KEY GENERATED FIRST",
        "/encrypt": "encrypts a file",
        "/decrypt": "decrypts a file -> REQUIRES A KEY GENERATED",
        "/exit": "save way of exitting",
        "/credits": "the credits",
        "/keyinfo": "prints useful information about the key -> REQUIERS A KEY GENERATED",
        "/delvars": "deletes all variables created during this sesion",
        "/cmds": "prints available commands",
        "/changedir": "change the directory were the encryption, decryption... files will be stored there, new working directory"
    }
    
    menu(None, False) #PRINTDEF=NONE FOR NO PRINT