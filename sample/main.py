from getAllUserNames import *
from getFavourites import *
from computeRelations import *

userFile = "../data/users.txt"
favouritesFile = "../data/usersFavourites.bin"
print("lendo arquivo de usuários...")
try:
    userList = readListFile(userFile)
except IOError:
    print("Arquivo de usuarios inexistente. Criando arquivo de usuarios..")
    #readUserNames(nameOutput = "../data/users.txt", pagesToRead = 200, threadAmount = 40,verbose = True, veryVerbose = True )
    read_user_names(name_output = "../data/users.txt", pages_to_read = 10, thread_amount = 20,verbose = True, very_verbose = True )
    userList = readListFile(userFile)

print("lendo favoriros dos usuarios...")
#import pdb; pdb.set_trace()
#getAllUsersFavourites(userList, outputFile = favouritesFile,NumberOfUsersToRead=200,threadAmount=200)
getAllUsersFavourites(userList, outputFile = favouritesFile,NumberOfUsersToRead=100000,threadAmount=40)
#computa numero de usuarios que favoritaram cada filme
