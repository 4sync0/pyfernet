#the purpose of this script is to protect the content inside .env in such way that it is not visible for anyone but usable for the scripts
import inspect
from hashlib import sha256
import secrets #to generate random strings each time it executes to be able to detect wether this things are made inside this script or not, kinda like a checkpoint
from cryptography import fernet

sesion_hash = secrets.randbits(8)

sesion_secret = sha256(sesion_hash.to_bytes(10, 'little'))
sesion_secret = sesion_secret.hexdigest()

cp_sesion_secret = sesion_secret


if sesion_secret == cp_sesion_secret and sesion_secret in bytes:
    e

    
with open("db/.env", "rb") as f:
    data = f.read()
    #assuming its already encrypted
    db_pw = fernet.Fernet.decrypt(data)
    fernet.Fernet.encrypt()

data = "NA"

#NOTE: todo -> genkey & key storage for it, load db basing on if these variables are correct...