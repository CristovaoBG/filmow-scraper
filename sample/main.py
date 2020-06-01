from getAllUserNames import *
from getFavourites import *

userFile = "../data/users.txt"
userName = "/usuario/dj_crissi/"
favouritesFile = "../data/usersFavourites.bin"
print("lendo arquivo de usuários...")
try:
    userList = readListFile(userFile)
except IOError:
    print("Arquivo de usuarios inexistente. Criando arquivo de usuarios..")
    readUserNames(nameOutput = "../data/users.txt", pagesToRead = 72600, threadAmount = 40,verbose = True, veryVerbose = True )
    userList = readListFile(userFile)

print("lendo favoriros dos usuarios...")
getAllUsersFavourites(userName,userList, outputFile = favouritesFile,NumberOfUsersToRead=60000,threadAmount=200)
