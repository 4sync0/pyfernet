from STORAGE import storage_listKEY
from STORAGE import storage_listFILE


#key from tuple to list
keylist = list(storage_listKEY.keytuple)
#remove N, unnecessary value
keylist.pop(0)

#file from tuple to list
filelist = list(storage_listFILE.filetuple)
#remove N too...
filelist.pop(0)


#print(keylist)
#print(filelist)