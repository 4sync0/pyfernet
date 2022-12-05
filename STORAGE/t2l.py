import storage_listKEY
import storage_listFILE


#key from tuple to list
keylist = list(storage_listKEY.keytuple)
#remove N/A, unnecessary variable
keylist.pop(0)

#file from tuple to list
filelist = list(storage_listFILE.filetuple)
#remove N/A too...
filelist.pop(0)


#print(keylist)
#print(filelist)