from listUtils import *
import math
import threading
import time
# import gc
#from computeRelations import *; countFavouritedTimes("usersFavourites.bin")
#APAGAR!!!!!!!!!!!!!!!!!!!!
def saveOnIntervall2(listToSave,onUser,filename):
    while(True):
        time.sleep(60)
        saveListFile(listToSave,filename)
        print("Arquivo",filename,"salvo. Tamanho:",len(listToSave)," no usuario:",onUser[0])
#APAGAR!!!!!!!!!!!!!!!!!!!!
#conta quantas vezes cada filme foi favoritado
moviesAndNumbers = []
onUser = [0]
def countFavouritedTimes(usersAndFavouritesFileName):
    usersAndFavouritesList = readListFile(usersAndFavouritesFileName)
    global moviesAndNumbers
    global onUser
    threadThread = threading.Thread(target = saveOnIntervall2, args = (moviesAndNumbers,onUser,"moviesAndNumbers.bin"))
    threadThread.start()
    #varre favoritos de todos os usuarios
    for uaf in usersAndFavouritesList:
        #import pdb; pdb.set_trace()
        onUser[0]+=1
        for fav in uaf[1]:
            #verifica se o filme fav ja esta na lista moviesAndNumbers, se tiver pega o id, se nao insere.
            try:
                favId = [man[0] for man in moviesAndNumbers].index(fav)
                #se achou, incrementa valor
                newNumber = moviesAndNumbers[favId][1]+1
                #substitui
                moviesAndNumbers[favId] = [fav, newNumber]
                #import pdb; pdb.set_trace()
            except:
                #insere na lista
                moviesAndNumbers.append([fav,1])
    saveListFile(moviesAndNumbers,"moviesAndNumbers.bin")
    return moviesAndNumbers;

def saveOnIntervall(listToSave,filename,total):
    while(True):
        time.sleep(200)
        saveListFile(listToSave,filename)
        print("Arquivo",filename,"salvo. Lidos:",len(listToSave,"de",total))

moviesAndProximityScores = []
def computeMovieRelations(userAndFavouritesFileName):
    usersAndFavouritesList = readListFile(userAndFavouritesFileName)
    uafSize = len(usersAndFavouritesList)
    #moviesAndProximityScores = [movie_name,[[movie1,score],[movie2,score],...],movie_name2,[[movie1,score],[movie2,score],...],...]
    global moviesAndProximityScores
    movieAndScores = []
    threadThread = threading.Thread(target = saveOnIntervall, args = (moviesAndProximityScores,"movieRelations.bin",uafSize))
    threadThread.start()
    #varre todos os usuarios
    for user in usersAndFavouritesList:
        # le cada favorito e adiciona a um na pontuacao de cada outro favorito
        for movie in user[1]:   #user[1] eh a lista de favoritos
            #dois casos, ou esse filme ja tem scores ou eh a primeira vez que aparece
            #caso ja exista, copia o existente.
            newCurrentFavourite = True # True if the movie is not on the list yet
            try:
                currentFavouriteID = [movieAndScores[0] for movieAndScores in moviesAndProximityScores].index(movie)
                movieAndScores = moviesAndProximityScores[currentFavouriteID]
                newCurrentMovie = False;
            #caso seja a primeira vez, cria novo item filmeAndScores
            except ValueError:
                movieAndScores = [movie,[]] #nessa lista vazia vai um conjunte de itens contendo filme e score
            #varre demais favoridos e adiciona 1 para na sua respectiva pontuacao
            for otherFavourite in user[1]:  #user[1] eh a lista de favoritos
                if (otherFavourite != movie):
                    #verifica se ja existe pontuacao para o filme otherFavourite no filme movie
                    #movieAndScores[1] sao pares de itens contendo o filme o respectivo score
                    try:
                        otherFavouriteID = [ms[0] for ms in movieAndScores[1]].index(otherFavourite)
                        movieAndScores[1][otherFavouriteID][1] += 1 # score do otherFavourite ja presente na lista do currentFavourite
                    except ValueError:
                        movieAndScores[1].append([otherFavourite,1]) # cria com o nome e atribui score 1
            #atualiza lista mestre de moviesAndProximityScores para o currentMovie (movie)
            if(len(movieAndScores[1])>0):
                if (newCurrentFavourite):
                    moviesAndProximityScores.append(movieAndScores)
                else:
                    moviesAndProximityScores[currentFavouriteID] = movieAndScores
    saveListFile(moviesAndProximityScores,"movieRelations.bin")
    print("computation of movie relations complete.")

def findClosestMovieOld(movieRelationsFile,moviename):
    movieRelations = readListFile(movieRelationsFile)
    #remove acento de todos os filmes indices para busca funcionar
    #from unidecode import unidecode
    #moviename = moviename.encode('latin1').decode('utf8')
    #moviename = unidecode(moviename)
    #for i in range(0,len(movieRelations)):
        #movieRelations[i][0] = unidecode(movieRelations[i][0])
    #try:
    id = [movieAndScores[0] for movieAndScores in movieRelations].index(moviename)
    #print(movieRelations[id])
    #encontra o maior
    othersScores = movieRelations[id][1]
    biggestScore = 0
    bestId = 0
    i=0
    for movieScore in othersScores:
        if (movieScore[1]>=biggestScore):
            bestId = i
            biggestScore = movieScore[1]
            print("----",biggestScore,"----",othersScores[bestId][0])
        i += 1
    print("-->",othersScores[bestId][0])

def findClosestMovie(movieRelations,moviesAndNumbers,moviename,exponent):

    #remove acento de todos os filmes indices para busca funcionar
    #from unidecode import unidecode
    #moviename = moviename.encode('latin1').decode('utf8')
    #moviename = unidecode(moviename)
    #for i in range(0,len(movieRelations)):
        #movieRelations[i][0] = unidecode(movieRelations[i][0])
    #try:
    id = [movieAndScores[0] for movieAndScores in movieRelations].index(moviename)
    #print(movieRelations[id])
    # moviesAndNumbers = readListFile("moviesAndNumbers.bin")
    #encontra o maior
    getSecond = lambda a:a[1]
    moviesAndNumbers.sort(key=getSecond)
    othersScores = movieRelations[id][1]
    biggestScore = moviesAndNumbers[-1][1]
    #import pdb; pdb.set_trace()
    bestId = 0
    i=0
    scoresList = []
    for movieScore in othersScores:
        #import pdb; pdb.set_trace()
        #procura peso do filme na lista de numeros
        if(movieScore[1] == 1):
            continue
        idAtNum = [m[0] for m in moviesAndNumbers].index(movieScore[0])
        factor = moviesAndNumbers[idAtNum][1]
        score = movieScore[1]/pow(factor,exponent)
        # if (score>=biggestScore):
        #     bestId = i
        #     biggestScore = score
        #     print("----",biggestScore,"----",othersScores[bestId][0])
        scoresList.append([movieScore[0],score])
        i += 1

    scoresList.sort(key=getSecond)
    print("-->",othersScores[bestId][0])
    return scoresList;

#DEBUG_START
mr = readListFile("movieRelations.bin")
man = readListFile("moviesAndNumbers.bin")

def pf(list):
    for l in list:
        print(l)

def pn(movieName):
    print(man[[m[0] for m in man].index(movieName)])

#import pdb; pdb.set_trace()
#DEBUG_END
#DEBUG_END
#k = findClosestMovie(mr,man,"acordar-para-a-vida-t1414",0.55)
#k = findClosestMovie(mr,man,"tenacious-d-uma-dupla-infernal-t3598",0.55)
#k = findClosestMovie(mr,man,"a-mao-assassina-t2070",0.55)
k = findClosestMovie(mr,man,"superbad-e-hoje-t3581",0.55)
import pdb; pdb.set_trace()
#except:
    #print("FAILED")
#movieRelations = readListFile("newMovieRelations.bin")
#l = findClosestMovie(movieRelations,"/superbad-e-hoje-t3581/")
#computeMovieRelations("usersFavourites.bin")

#exec(open("script.py").read())

#normalizeMovieRelations("movieRelations.bin")
