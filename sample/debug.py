from listUtils import *
import computeRelations
import random
#generateFakeUsersAndFavorites(50,30,20)
def generateFakeUsersAndFavorites(usersNum,moviesNum,maxFav):
    usersAndFavorites = []
    for i in range(0,usersNum):
        favList = []
        userName = "user"+str(i)
        #numero de favoritos entre 1 e maxFav
        favAmnt = random.randint(1,maxFav)
        for j in range(0,maxFav):
            favName = "movie"+str(random.randint(1,moviesNum))
            if not favName in favList:
                favList.append(favName)
        usersAndFavorites.append([userName,favList])
    return usersAndFavorites

def pf(list):
    for l in list:
        print(l)

def pn(movieName):
    print(man[[m[0] for m in man].index(movieName)])

#countRepetitions(mr,"superbad-e-hoje-t3581")
def countRepetitions(list,name):
    rep = 0
    i=0
    for l in list:
        if l[0]==name:
            print("repetition at:", i)
            rep+=1
        i+=1
    print("repetitions:",rep)

def listToStr(list):
    string = ""
    for i in list:
        string = string + str(i) + ' '
    return string

def textifyMovieNumbers():
    list = read_list_file("moviesAndNumbers.bin")
    string = ""
    for item in list:
        # stringLine = item[0] + " " + str(item[1])
        # string += stringLine + "\n"
        string += item[0] + " " + str(item[1]) + "\n"
    f=open("moviesAndNumbers.txt","w+")
    f.write(string)
    f.close()

def textifyFiles():
    i=0
    exit = False
    while not exit:
        try:
            print("reading file",i)
            list = read_list_file("teste/movies"+str(i)+".bin")
            string = listToStr(list)
            f=open("teste/movies"+str(i)+".txt","w+")
            f.write(string)
            f.close()
            i+=1
        except:
            exit = True
# import pdb;pdb.set_trace()
mr = []
man = []

def debugSetup():
    global mr
    global man
    mr = read_list_file("mr.bin")
    man = read_list_file("moviesAndNumbers.bin")
    print("done reading")

def debugFiles():
#    fuaf = generateFakeUsersAndFavorites(50,20,20)
#    computeRelations.computeMovieRelations(fuaf)
    print("lendo arquivos mr e man...")
    fmr = read_list_file("movieRelations.bin")
#    fman = computeRelations.countFavouritedTimes(fuaf)
    fman = read_list_file("moviesAndNumbers.bin")
    print("ok.")
    computeRelations.generateFiles(fman,fmr,directory = "teste/")
    rec = computeRelations.reconstructMovieRelations(fman,"superbad-e-hoje-t3581")
    import pdb; pdb.set_trace()

def formatMoviesNames():
    man = read_list_file("moviesAndNumbers.bin")
    nameList = []
    for m in man:
        newName = ""
        # import pdb; pdb.set_trace()
        for letter in m[0]:
            newName += letter if letter != '-' else ' '
        newName = newName.rsplit(' ', 1)[0] #remove ultima palavra
        nameList.append(newName)
    #convert nameList para nameString pra salvar txt
    nameString = ""
    for name in nameList:
        nameString+=name+"\n"
    #salva
    f=open("movieNames.txt","w+")
    f.write(nameString)
    f.close()
    print(len(nameList))



# debugFiles()
formatMoviesNames();
