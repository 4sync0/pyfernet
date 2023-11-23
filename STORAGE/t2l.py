from STORAGE import storage_listKEY
from STORAGE import storage_listFILE


# (key) tuple -> list
keylist = list(storage_listKEY.keytuple)
# remove N, unnecessary value
keylist.pop(0)

# (file) tuple -> list
filelist = list(storage_listFILE.filetuple)
# ^^^
filelist.pop(0)