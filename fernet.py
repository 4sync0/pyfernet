print("loading...")

import os
from cryptography.fernet import Fernet, InvalidToken, MultiFernet
from random import randrange
from sys import exit
import json
import subprocess
from pymongo import MongoClient, errors

#imported files
from LOGS import logs_setup as logger
from STORAGE import pytojson
import file_moving


#connect with the db
client = MongoClient("mongodb+srv://vscode:vscusr_limited11@cluster4pyfernet.mutcgi3.mongodb.net/test")
dbs = client.list_database_names()
keys_db = client.keys




def menu(printdef: str, clear: bool): #PRINTDEF=NONE FOR NO PRINT
        if printdef: print(printdef)
        else: pass

        if clear: vars().clear() #clear all variables regardless of the parameter input
        else: pass

        multiQ = False

        #access the id through here so I get no UnboundLocalError
        with open("last_id.txt", "r") as f:
            id_num = f.read()

        while True:
            if multiQ == True: #to make the user know whether they're on multifernet encryption mode or not
                command: str = input("multi.cmd->\t")
            else: command: str = input("cmd->\t")

            if command == "/new":
                file: str = input("select file's relative path\tdont forget to place its extension at the end\n-->> ")
                file_checking = os.path.exists(file)
                if not file_checking:
                    print("file doesn't exist or you made a typo")
                    menu(None, False)
                    break
                else: pass

            elif command == "/genkey":
                keys_collection = keys_db[str(id_num)] #set collection
                collections = keys_db.list_collection_names()


                for collection in collections: #check every collection within the db
                    keys_collection_indent = keys_db[str(collection)]
                    if keys_collection_indent.find_one({"file": file}) != None: #only new files that arent in the db will continue
                        menu(f"key already exists for {file}", False)
                    
                    else: continue

                    
                if multiQ:
                    keysnum = int(input("how many keys do you want?\t"))
                    KEY = []
                    decoded_key = [] #decoded vers. of KEY
                    for _ in range(keysnum):
                        new_key_instance = Fernet.generate_key()
                        decoded_key.append(new_key_instance.decode()) #just decoding it and adding to decoded_key list -> decoded
                        KEY.append(bytes(new_key_instance)) #it goes through every key inputted and adds it to KEY list -> encoded
                else:
                    KEY = Fernet.generate_key()
                    decoded_key = KEY.decode()


                with open(f"FERNETKEY{id_num}.txt", "wb") as f_key:
                    if multiQ:
                        #forloop_detect is to avoid a space at the beginning of the file where the key is stored
                        forloop_detect = False
                        for each_key in KEY:
                            if forloop_detect:
                                f_key.write(" ".encode())
                            else: pass
                            f_key.write(each_key)
                            forloop_detect = True
                            
                    else:
                       f_key.write(KEY)
                
                #check if the key has been generated or setted | true = generated; false = setted
                genkey_checkpoint = True

                print(f"\n->the key that just got generated is unique, use \"/sesion\" for more information\n")

                #to the db
                doc_gen = {
                    "file": file,
                    "key" : KEY
                }

                keys_collection.insert_one(doc_gen)

                #NOTE: on 2/2, fix BinData saves on the db, to just store the key 
                    
            elif command == "/encrypt":
                try:
                    if multiQ:
                        fern = MultiFernet(KEY)
                    else:
                        fern = Fernet(key=KEY)
                
                    with open(file, "rb") as raw_f:
                       origFile = raw_f.read()
                    
                    encrypt = fern.encrypt(origFile)
                    
                    with open(file, "wb") as f:
                       f.write(encrypt)
                    
                    print("\nsuccesfully encripted: ",file)
                    logger.logging.debug(f"{file} encrypted")

                except Exception: ValueError, print("invalid key"), logger.logging.error("ValueError while encryption")
        
            elif command == "/exit":
                logger.logging.debug("sesion ended")
                exit("bai")
        
            elif command == "/decrypt":
                keys_collection = keys_db[str(id_num)] #set collection

                #check if key has been setted or not, now longer needs to input keys every time you decrypt a file
                if KEY:
                    key_inp = KEY
                else:
                    key_inp: str = input("input keys:\n")
                if multiQ:
                    key_inp = key_inp.split(" ")
                    temp_keylist2 = []
                    for keys in key_inp:
                        temp_keylist2.append(keys)
                    key_inp = temp_keylist2
                else:
                    pass
                try:
                    f = Fernet(key_inp) #THIS COULD CAUSE AN ERROR, WATCH!!
                    with open(file, "rb") as encrypted_f:
                        encrypted = encrypted_f.read()
                    
                    decrypted = f.decrypt(encrypt)
            
                    with open(file, "wb") as decrypted_f:
                        decrypted_f.write(decrypted)
            
                    print(f"succesfully decripted {file}")
                    logger.logging.debug(f"{file} decrypted")

                    #delete from the db
                    keys_collection.drop(id_num)
                except Exception: InvalidToken, print("invalid token"), logger.logging.error("InvalidToken(fernet) while decryption")
                
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

                except Exception: UnboundLocalError, print("no key generated during this sesion"), logger.logging.error("UnboundLocalError while loading sesion")
            
            elif command == "/save": #will only store the last change made into both "file" and "key" variables
                try:
                    #append key tuple
                    with open("STORAGE/storage_listKEY.py", "a") as f:
                        #check if it has the key in bytes or if the user just setted it, so it's not on bytes so it needs no decode
                        if multiQ:
                            if genkey_checkpoint:
                                forloop_detect_save = False
                                f.write(", [") #determinates the start of the list
                                for element in decoded_key:
                                    if forloop_detect_save:
                                        f.write(f", '{str(element)}'")
                                    else:
                                        f.write(f"'{str(element)}'")
                                        forloop_detect_save = True
                                f.write("]") #determinates the end of the list
                                
                            elif not genkey_checkpoint:
                                forloop_detect_save = False
                                f.write(", [") #determinates the start of the list
                                for element in KEY:
                                    if forloop_detect_save:
                                        f.write(f", '{str(element)}'")
                                    else:
                                        f.write(f"'{str(element)}'")
                                        forloop_detect_save = True
                                f.write("]") #determinates the end of the list
                        else:
                            if genkey_checkpoint:
                                f.write(f", '{decoded_key}'")
                            elif not genkey_checkpoint:
                                f.write(f", '{KEY}'")  
                        
                    #append file tuple
                    with open("STORAGE/storage_listFILE.py", "a") as f:
                        f.write(f", '{file}'")

                    logger.logging.debug("info saved to storage")

                except Exception: UnboundLocalError, print("no key specified"), logger.logging.error("UnboundLocalError while saving")
                                 
            elif command == "/load":
                pytojson.start(True)

            elif command == "/destroydict":
                #running the bash script to clear x,y files
                subprocess.run(["STORAGE/rmdict_cmd.sh"])
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
                
                except Exception: UnboundLocalError, print("no file specified"), logger.logging.error("UnboundLocalError while loading file")
            
            elif command == "/setkey":
                keys_collection = keys_db[id_num]
                if multiQ:
                    KEY = str(input("set the keys if you've already got one:(each one separated by a space)\n"))
                    KEY = KEY.split("/")
                    temp_keylist = []
                    for keys in KEY:
                        temp_keylist.append(keys)
                    ask_key = temp_keylist
                else:
                    ask_key = input("set the key: \n")

                #check if the key is in db
                collections = keys_db.list_collection_names()

                for collection in collections:
                    keys_collection_indent = keys_db[str(collection)]
                    if keys_collection_indent.find_one({"file": file, "key": ask_key}) != None: #only files with their keys that are in the db will continue
                        KEY = ask_key
                        #to check if the key has been generated or setted | true = generated; false = setted
                        genkey_checkpoint = False
                        break
                    elif keys_collection_indent.find_one({"file": file, "key": ask_key}) == None:
                        menu(f"There's no key for: {file}", False)

            elif command == "/key":
                try:
                    if genkey_checkpoint:
                        print(decoded_key)
                    elif not genkey_checkpoint:
                        print(KEY)
                except Exception: UnboundLocalError, print("no key specified"), logger.logging.error("UnboundLocalError while loading key")

            elif command == "/tojson":
                #converts the dictionary stored in the storage directory to json file
                print("json file will get stored in: " + os.getcwd())

                #destroys last file and rewrites to avoid errors
                subprocess.run(["rm", "storage.json"])

                pytojson.start(False) #to update the new conent into the storage variable

                with open("storage.json", "x") as f:
                    json.dump(pytojson.storage, f, indent=2)

            elif command == "/jsonformat": menu("under construction", False)#change the json formatting

            elif command == "/relogs":
                try:
                    #destroy logs witht he ultimate power of god (aka bash)
                    subprocess.run("rm LOGS/logs.log", shell=True)
                    #then create it back but empty
                    with open("LOGS/logs.log", "x") as f:
                        f.write("")

                except Exception: FileNotFoundError, print("file error"), logger.logging.error("FileNotFoundError while relogs")
            
            elif command == "/update":
                import repo.repo_update

            elif command == "/multi -s":
                multiQ = True
                #the main idea is to make a multifernet mode that activates running /multi -s command, when activated, most commands will be modified to work
                #using multifernet
            
            elif command == "/multi -q":
                #quit multifernet mode
                multiQ = False
                menu("left multifernet mode", True)

            elif command == "/decrypt -t":
                #same as /decrypt but with the at_time function
                if KEY:
                    key_inp = KEY
                else:
                    key_inp: str = input("input keys:\n")
                if multiQ:
                    menu("this feature has not been tested in multifernet yet", False)
                else:
                        decrypt_when = input(f"insert the time (in seconds) when the key for: {file} will be available for decryption\n")
                        Fernet.decrypt_at_time(key_inp, int(decrypt_when))
                
                        print(f"\n {file}'s key will stop working for decryption in: {decrypt_when} seconds")
                        logger.logging.debug(f"{file}'s key will be functional until {decrypt_when} sec.")
                
            elif command == "/encrypt -t":
                #same as /encrypt but with the at_time function
                if multiQ:
                    menu("this feature has not been tested in multifernet yet", False)
                else:
                    encrypt_when = input(f"insert the time (in seconds) when the key for: {file} will be available for encryption\n")
                    Fernet.encrypt_at_time(key_inp, file, int(encrypt_when))

                    print(f"\n {file}'s key will stop working for encryption in: {encrypt_when} seconds")
                    logger.logging.debug(f"{file}'s key will be functional until {encrypt_when} sec.")
            
            elif command == "/search":
                set_db = str(input("id:\t"))
                if set_db not in keys_db.list_collection_names(): #seach if it is on the database
                    menu("the id is invalid or it doesn't exist", False)
                else:
                    searched_collection = keys_db[set_db]
                    for doc in searched_collection.find():
                        print(doc)
                #NOTE: Make it so that it also gets a different, safe unique identifier for the person who saved it on the db (add a specific value to the doc that only the file owner has/knows)
            else: print("unknown")

print("||fernet | p4tp5||\ntry \"/new\" command first to select a file")
 # automatically set to false

 #unique sesion identifier
id_num = randrange(0, 1000000000)
with open("last_id.txt", "r") as f:
    last_id = f.read()
with open("last_id.txt", "w") as f:
    current_id = f.write(str(id_num))

if current_id == last_id:
    subprocess.run(["rm last_id"])
#if taken
try:
    while current_id == last_id:
        id_num = randrange(0, 1000000000)
finally:
    with open("last_id.txt", "w") as f:
        f.write(str(id_num))
    
menu(None, False) #PRINTDEF=NONE FOR NO PRINT