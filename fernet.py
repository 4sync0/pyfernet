try:
    import os
    from cryptography.fernet import Fernet, InvalidToken, MultiFernet
    from random import randrange
    from sys import exit
    import json
    import subprocess
    import pymongo
    from base64 import urlsafe_b64encode
    import mysql.connector

    # imported files
    from LOGS import logs_setup as logger
    from STORAGE import pytojson
    import file_moving

except Exception as e: print("error on loading modules/files/packages"), logger.logging.error(e), exit(1)
finally: print("loaded modules & files")




def menu(printdef: str, clear: bool, redb: bool):
        
        system_name = os.name
        multiQ = False

        if printdef: print(printdef)
        else: pass

        if clear: vars().clear()
        else: pass

        if redb:
            try:
                # default connection with database
                client = pymongo.MongoClient("mongodb+srv://vscode:KCHZ2YJPx5qsjLJs@cluster4pyfernet.mutcgi3.mongodb.net/")
                keys_db = client["keys"]
            finally: print("connected to default database, custom db is recommended")
        else: pass


        # access the id through here so I get no UnboundLocalError
        with open("last_id.txt", "r") as f:
            id_num = f.read()

        while True:
            if multiQ == True:
                command: str = input("multi.cmd->\t")
            else: command: str = input("cmd->\t")

            if command == "/new":
                file: str = input("select file's relative path\tdont forget to place its extension at the end\n-->> ")
                file_checking = os.path.exists(file)
                if not file_checking:
                    print("file doesn't exist or you made a typo")
                    menu(None, False, False)
                    break
                else: pass

            elif command == "/genkey":
                try: file
                except UnboundLocalError as e: print("no file on this session, use '/new'"), logger.logging.error(e) 

                keys_collection = keys_db[str(id_num)]
                collections = keys_db.list_collection_names()


                for collection in collections:
                    keys_collection_indent = keys_db[str(collection)]
                    if keys_collection_indent.find_one({"file": file}) != None: # only new files that arent in the db will continue
                        menu(f"key already exists for {file}", False, False)
                    
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
                        first_space_checkpoint = False
                        for each_key in KEY:
                            if first_space_checkpoint:
                                f_key.write(" ".encode())
                            else: pass
                            f_key.write(each_key)
                            first_space_checkpoint = True
                            
                    else:
                       f_key.write(KEY)
                

                genkey_checkpoint = True

                print(f"\n->the key that just got generated is unique, use \"/sesion\" for more information\n")
                #encode and decode to base64 to stop the key value from getting saved with  BinData (BSON)

                try:
                    urlsafe_b64encode(KEY).decode()
                except Exception: #multi keys
                    TypeError

                    base64KEY = []
                    for i in KEY:
                        base64KEY.append(urlsafe_b64encode(bytes(i)).decode())

                    base64KEY_str = " ".join(base64KEY)
                    
                    doc_gen = {
                        "file": file,
                        "key" : base64KEY_str
                    }
                else: #single key
                    base64KEY = urlsafe_b64encode(KEY).decode()

                    doc_gen = {
                        "file": file,
                        "key" : base64KEY
                    } 

                keys_collection.insert_one(doc_gen)

                print("key saved in the database, ready to use")
                    
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
                    logger.logging.info(f"{file} encrypted")

                except PermissionError as e: print("lack of privileges to modify the file. Try executing pyfernet with the necessary perms"), logger.logging.error(e)
                except ValueError as e: print("invalid key"), logger.logging.error(e)
                except UnboundLocalError as e: print("no key generated or specified"), logger.logging.error(e)
        
            elif command == "/exit":
                exit("bai")
        
            elif command == "/decrypt":
                keys_collection = keys_db[str(id_num)]

                # check if key has been setted or not, no longer needs to input keys every time you decrypt a file
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
                    f = Fernet(key_inp) # THIS COULD CAUSE AN ERROR, WATCH!!
                    with open(file, "rb") as encrypted_f:
                        encrypted = encrypted_f.read()
                    
                    decrypted = f.decrypt(encrypted)
            
                    with open(file, "wb") as decrypted_f:
                        decrypted_f.write(decrypted)
            
                    print(f"succesfully decripted {file}")
                    logger.logging.info(f"{file} decrypted")

                    # delete from the db
                    keys_collection.delete_one({"name": id_num})
                except InvalidToken as e: print("invalid token"), logger.logging.error(str(e))
                
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

                except UnboundLocalError as e: print("no key generated during this sesion"), logger.logging.error(e)
            
            elif command == "/save": # will only store the last change made into both "file" and "key" variables
                try:
                    with open("STORAGE/storage_listKEY.py", "a") as f:
                        # check if it has the key in bytes or if the user just setted it, so it's not on bytes hence it needs no decode
                        if multiQ:
                            if genkey_checkpoint:
                                forloop_detect_save = False
                                f.write(", [") # determinates the start of the list
                                for element in decoded_key:
                                    if forloop_detect_save:
                                        f.write(f", '{str(element)}'")
                                    else:
                                        f.write(f"'{str(element)}'")
                                        forloop_detect_save = True
                                f.write("]") # determinates the end of the list
                                
                            elif not genkey_checkpoint:
                                forloop_detect_save = False
                                f.write(", [") # ^
                                for element in KEY:
                                    if forloop_detect_save:
                                        f.write(f", '{str(element)}'")
                                    else:
                                        f.write(f"'{str(element)}'")
                                        forloop_detect_save = True
                                f.write("]") # ^
                        else:
                            if genkey_checkpoint:
                                f.write(f", '{decoded_key}'")
                            elif not genkey_checkpoint:
                                f.write(f", '{KEY}'")  
                        
                    with open("STORAGE/storage_listFILE.py", "a") as f:
                        f.write(f", '{file}'")

                    logger.logging.info("info saved to storage")

                except UnboundLocalError as e: print("no key specified"), logger.logging.error(e)
                                 
            elif command == "/load":
                pytojson.start(True)

            elif command == "/destroydict":
                # running the bash script to clear x,y files
                if system_name == "nt":
                    subprocess.run(["truncate -s 0 STORAGE/storage_listFILE.py && truncate -s 0 STORAGE/storage_listKEY.py"])
                elif system_name == "posix":
                    subprocess.run(["sudo  truncate -s 0 STORAGE/storage_listFILE.py && truncate -s 0 STORAGE/storage_listKEY.py"])
                
                # rewrite to place "N" on the lists to avoid errors while appending values & place the variable again
                with open("STORAGE/storage_listFILE.py", "w") as f:
                    f.write("filetuple = 'N'")

                with open("STORAGE/storage_listKEY.py", "w") as f:
                    f.write("keytuple = 'N'")

                print("successful")

            elif command == "/delvars":
                menu("deleting variable storage..",  True, True)

            elif command == "/changedir":
                file_moving.start()
        
            elif command == "/cwd": print(os.getcwd())

            elif command == "/logs":
                with open("LOGS/logs.log", "r") as f:
                    logs = f.read()
                print(logs)

            elif command == "/file":
                try: print(file)
                
                except UnboundLocalError as e: print("no file specified"), logger.logging.error(e)
            
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

                # check if the key is in db
                collections = keys_db.list_collection_names()

                for collection in collections:
                    keys_collection_indent = keys_db[str(collection)]
                    if keys_collection_indent.find_one({"file".replace('"', ""): file, "key".replace('"', ""): ask_key}) != None:
                        KEY = ask_key

                        genkey_checkpoint = False
                        break
                    else:
                        print(f"No key or incorrect on {file}")
                        break

            elif command == "/key":
                try:
                    if genkey_checkpoint:
                        print(decoded_key)
                    elif not genkey_checkpoint:
                        print(KEY)
                except UnboundLocalError as e: print("no key specified"), logger.logging.error(e)

            elif command == "/tojson":
                # converts the dictionary stored in the storage directory to json file
                print("json file will get stored in: " + os.getcwd())

                # destroys last file and rewrites to avoid errors
                subprocess.run(["rm", "storage.json"])

                pytojson.start(False) # to update the new conent into the storage variable

                with open("storage.json", "w") as f:
                    json.dump(pytojson.storage, f, indent=2)

            elif command == "/jsonformat": menu("under development", False, False) #change the json formatting

            elif command == "/relogs":
                try:
                    subprocess.run(["rm", "LOGS/logs.log"])

                    with open("LOGS/logs.log", "x") as f:
                        f.write("")

                except FileNotFoundError as e: print("file error"), logger.logging.error(e)
            
            elif command == "/update":
                import repo.repo_update

            elif command == "/multi -s":
                multiQ = True

                # NOTE:
                # the main idea is to make a multifernet mode that activates running /multi -s command, when activated, most commands will be modified to work
                # using multifernet
            
            elif command == "/multi -q":
                multiQ = False

            elif command == "/decrypt -t":
                # same as /decrypt but with the at_time function
                if KEY:
                    key_inp = KEY
                else:
                    key_inp: str = input("input keys:\n")
                if multiQ:
                    menu("this feature has not been tested in multifernet yet", False, False)
                else:
                        decrypt_when = input(f"insert the time (in seconds) when the key for: {file} will be available for decryption\n")
                        Fernet.decrypt_at_time(key_inp, int(decrypt_when))
                
                        print(f"\n {file}'s key will stop working for decryption in: {decrypt_when} seconds")
                        logger.logging.info(f"{file}'s key will be functional until {decrypt_when} sec.")
                
            elif command == "/encrypt -t":
                # same as /encrypt but with the at_time function
                if multiQ:
                    menu("this feature has not been tested in multifernet yet", False, False)
                else:
                    encrypt_when = input(f"insert the time (in seconds) when the key for: {file} will be available for encryption\n")
                    Fernet.encrypt_at_time(key_inp, file, int(encrypt_when))

                    print(f"\n {file}'s key will stop working for encryption in: {encrypt_when} seconds")
                    logger.logging.info(f"{file}'s key will be functional until {encrypt_when} sec.")
            
            elif command == "/search":
                set_db = str(input("id:\t"))
                if set_db not in keys_db.list_collection_names(): #seach if it is on the database
                    menu("the id is invalid or it doesn't exist", False, False)
                else:
                    searched_collection = keys_db[set_db]
                    for doc in searched_collection.find():
                        print(doc)
                # (possibly obsolete by now, ignore down comment)
                # NOTE: Make it so that it also gets a different, safe unique identifier for the person who saved it on the db (add a specific value to the doc that only the file owner has/knows)

            elif command == "/connect mongodb":
                try: open("dbsettings.json")

                except Exception:
                    connectionI_mongodb = input("cluster token:\t")

                    try:
                        client = pymongo.MongoClient(connectionI_mongodb)
                        keys_db = client["keys"]
                    except pymongo.errors.ConfigurationError as e: print("token is incorrect")
                    else:
                        print("connection established")
                        mysql_checkpoint = False

                    connection_info = {
                    "type": "mongodb",
                    "client": connectionI_mongodb,
                    "keys_db": "keys"
                    }

                    with open("dbsettings.json", "w") as f:
                        f.write(json.dumps(connection_info))

                else:
                    dbsettings = open("dbsettings.json")
                    dbsettings = json.load(dbsettings)

                    if dbsettings["type"] == "mongodb":
                        client = pymongo.MongoClient(dbsettings["client"])
                        keys_db = client["keys"]
                        print("connection established")
                        mysql_checkpoint = False
                        continue
                    else: menu("database type not supported, delete dbsetting.json and make sure the type is mysql or mongodb", False, True)
            
            elif command == "/connect mysql":
                try: open("dbsettings.json")
                
                #new connection
                except Exception:
                    connectionI_mysql = input("|user password host and database| in that same order sepparated by a space:\t")

                    connection_keys = ["user", "password", "host", "database"]
                    try:
                        connection_values = dict(zip(connection_keys, connectionI_mysql.split(" ")))


                        mysql_connection = mysql.connector.connect(
                            user=connection_values["user"],
                            password=connection_values["password"],
                            host=connection_values["host"],
                            database=connection_values["database"]
                        )

                        connection_info = {
                            "type": "mysql",
                            "user": connection_values["user"],
                            "password": connection_values["password"],
                            "host": connection_values["host"],
                            "database": connection_values["database"]
                        }

                        mysql_cursor = mysql_connection.cursor()

                        with open("dbsettings.json", "w") as f:
                            f.write(json.dumps(connection_info))

                        mysql_checkpoint = True

                        print("connection established")
                        
                    except Exception as e: print("incorrect value(s) or order not followed, try again"), logger.logging.error(f"mysql connection err- {e}")




                #previous save
                else:
                    try:
                        dbsettings = open("dbsettings.json")
                        connection_info = json.load(dbsettings)

                        if connection_info["type"] == "mysql":

                            mysql_connection = mysql.connector.connect(
                            user=connection_info["user"],
                            password=connection_info["password"],
                            host=connection_info["host"],
                            database=connection_info["database"]
                            )

                            mysql_cursor = mysql_connection.cursor()

                            mysql_checkpoint = True

                            print("connection established")
                            continue
                        else: menu("database type not supported, delete dbsetting.json and make sure the type is mysql or mongodb", False, True)

                    except json.decoder.JSONDecodeError as e: print("no 'type' value on the json file"), logger.logging.error(e)
            
            else: print("unknown")

print("||fernet||\ntry \"/new\" command first to select a file")
 # automatically set to false

 # unique sesion identifier
id_num = randrange(0, 1000000000)
with open("last_id.txt", "r") as f:
    last_id = f.read()
with open("last_id.txt", "w") as f:
    current_id = f.write(str(id_num))

if current_id == last_id:
    subprocess.run(["rm", "last_id"])
# if taken
try:
    while current_id == last_id:
        id_num = randrange(0, 1000000000)
finally:
    with open("last_id.txt", "w") as f:
        f.write(str(id_num))

mysql_checkpoint = False

menu(None, False, True)

