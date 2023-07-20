from listUtils import *
import time
import os
import threading

unableToRead = []
# imgUrl = "https://media.fstatic.com/VvP43i1nI5NXQAdLE8GmrsdJ2Vo=/fit-in/210x312/smart/media/movies/covers/2016/01/los-parecidos_t198932.jpg"
# urllib.request.urlretrieve(imgUrl, "local-filename2.jpg")
#pega link da imagem de uma pagina
def getMovieImage(movieId, moviesAndNumbers,destinFolder = "images/"):
    #nao faz nada se arquivo destino ja existente
    if os.path.isfile(destinFolder+str(movieId)+".jpg"):
        print("arquivo "+str(movieId)+" ja existente.")
        return
    base = "https://filmow.com/"
    # movieName = "superbad-e-hoje-t3581"
    #descobre nome do filme
    movieName = moviesAndNumbers[movieId][0]
    print("lendo "+movieName + "...")
    url = base + movieName
    tryMovie = 200
    tryImage = 200
    while tryMovie > 0:
        try:
            soup = openSoup(url)
            movie = soup.find("img",class_="img-full")
            imgUrl = movie['src']
            #salva imagem no repositorio devido
            while tryImage > 0:
                try:
                    urllib.request.urlretrieve(imgUrl, destinFolder+str(movieId)+".jpg")
                    tryImage = -1   #para sair do loop
                    tryMovie = -1   #para sair do loop maior
                    print("sucesso na captura da imagem de "+ movieName)
                except:
                    tryImage -=1    #decrementa tentativa
                    print("falha na captura de "+ movieName)
                    time.sleep(2)
        except:
            tryMovie -= 1 #decrementa tentativa de acesso a pagina do filme
            print("falha na captura da url de "+ movieName)
            time.sleep(2)

    if (tryImage != -1 or tryMovie != -1):
        print("algo errado na leitura de ", movieName)
        global unableToRead
        unableToRead.append(movieName)


def getMoviesImagesRange(startId,endId,moviesAndNumbers):
    for i in range(startId,endId):
        getMovieImage(i, moviesAndNumbers)

def getAllMoviesImages(threadAmount = 200):
    moviesAndNumbers = readListFile("moviesAndNumbers.bin")
    manLen = len(moviesAndNumbers)
    chopNumber = int(manLen/threadAmount)
    startId = 0
    endId = chopNumber
    while (startId<manLen):
        #nova thread
        newThread = threading.Thread(target = getMoviesImagesRange, args = (startId,endId,moviesAndNumbers))
        newThread.start()

        #recalculate
        startId += chopNumber
        endId +=chopNumber
        if endId > manLen:
            endId = manLen

def moveImagesToDir(dirAmount = 100, destinBase = "packed/",origin = "images/", biggestMovie = 19799):
    from shutil import copyfile
    movieId = 0
    maxIterations = biggestMovie
    #cria pasta master se nao existir
    if (not os.path.isdir(destinBase)):
        os.mkdir(destinBase)

    while (movieId<maxIterations):
        if (movieId%dirAmount == 0):
            destin = destinBase+str(movieId)+"/"
            if (not os.path.isdir(destin)):
                os.mkdir(destin)
        if (os.path.isfile(origin+str(movieId)+".jpg")):
            copyfile(origin+str(movieId)+".jpg",destin+str(movieId)+".jpg")
        movieId+=1

def removeEmptys(dirAmount = 100, directoryBase = "packed/"):
    emptys = []
    page = 0
    for i in range(0,25000):
        if (i%dirAmount == 0):
            page = i
        fileDir = directoryBase + str(page) + "/" + str(i) + ".jpg"
        #se existir, verifica se tamanho eh zero
        if(os.path.isfile(fileDir)):
            fileSize = os.stat(fileDir).st_size
            if(fileSize == 0):
                print(i)
                emptys.append(i)
                os.remove(fileDir)
                #remove file
    save_list_file(emptys,"emptys.bin")

# moveImagesToDir()
removeEmptys()
import pdb; pdb.set_trace()
