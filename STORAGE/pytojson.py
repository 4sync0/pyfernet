from STORAGE import t2l
import json

#take list from t2l.py, and iterate it to store it to make it a dictionary and then store in a json file

storage = {}

#this is what will be contained in a storage file
for length in range(len(t2l.keylist)):
    storage[t2l.keylist[length]] = t2l.filelist[length]

#will execute only when called
def user():
    #this is what the user will see
    for key, value in storage.items():
        print(f"key: {key}  |  file: {value}")