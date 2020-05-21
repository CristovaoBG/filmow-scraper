import string
import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import timeit
import pickle

stopAllThreads = False

def stop():
	stopAllThreads = True

def openSoup(httpLink):
	htmlText = urllib.request.urlopen(httpLink).read()
	soup = BeautifulSoup(htmlText, 'html.parser')
	return soup
"""
def readListFile(fileName):
	f = open(fileName,"r")
	string = f.read();
	listReturn = string.split('\n',-1)
	return listReturn
"""

def readListFile(fileName):
	with open(fileName,"rb") as fp:
		listReturn = pickle.load(fp)
	return listReturn

def saveListFile(listInput, fileName):
	with open(fileName,"wb") as fp:
		pickle.dump(listInput,fp)

def getFavourites(userString):
	movieNameList = []
	urlUser = "https://filmow.com"+userString
	pageID = 1
	while(True):
		try:
			userFavouritesSoup = openSoup(urlUser+"filmes/favoritos/?pagina="+str(pageID))
		except:
			break
		allMovies = userFavouritesSoup.find_all("li",class_="movie_list_item")
		print("reading: "+ urlUser+"filmes/favoritos/?pagina="+str(pageID))
		for movie in allMovies:
			movieName = movie.find("a")['title']
			movieNameList.append(movieName)
		pageID+=1
	return movieNameList

def getUserWatched(userString):
	movieNameList = []
	urlUser = "https://filmow.com"+userString
	pageID = 1
	#https://filmow.com/usuario/dj_crissi/filmes/ja-vi/?pagina=
	while(True):
		try:
			userFavouritesSoup = openSoup(urlUser+"filmes/ja-vi/?pagina="+str(pageID))
		except:
			break
		allMovies = userFavouritesSoup.find_all("li",class_="movie_list_item")
		print("reading: "+ urlUser+"filmes/ja-vi/?pagina="+str(pageID))
		for movie in allMovies:
			movieName = movie.find("a")['title']
			movieNameList.append(movieName)
		pageID+=1
	return movieNameList

def getUserDontWantToSee(userString):
	movieNameList = []
	urlUser = "https://filmow.com"+userString
	pageID = 1
	#https://filmow.com/usuario/dj_crissi/filmes/ja-vi/?pagina=
	while(True):
		try:
			userFavouritesSoup = openSoup(urlUser+"filmes/ja-vi/?pagina="+str(pageID))
		except:
			break
		allMovies = userFavouritesSoup.find_all("li",class_="movie_list_item")
		print("reading: "+ urlUser+"filmes/nao-quero-ver/?pagina="+str(pageID))
		for movie in allMovies:
			movieName = movie.find("a")['title']
			movieNameList.append(movieName)
		pageID+=1
	return movieNameList

def threadTest(threadNum):
	print("thread number "+ str(threadNum) + " started.")
	time.sleep(2)
	print("thread number "+ str(threadNum) + " finished.")


def getAllUsersFavourites(userList,usersFavouritesList):
	i=0
	global stopAllThreads
	for u in userList:
		print("reading user "+ u +"   user number: "+str(i))
		currentUserFavourite = getFavourites(u)
		userAndFavourites = []
		userAndFavourites.append(u)
		userAndFavourites.append(currentUserFavourite)
		usersFavouritesList.append(userAndFavourites)
		print("DONE user "+ u +"   user number: "+str(i))
		i+=1
		if (stopAllThreads):
			break

def waitAndSave(usersFavouritesList):
	global stopAllThreads
	while (stopAllThreads == False):
		print("arquivoSalvo!")
		saveListFile(usersFavouritesList,"data2.bin")
		time.sleep(120)

"""
usersRead = []
for u in usersFavouritesList
	usersRead.append(u[0])
"""		




startTime = timeit.default_timer()

"""
	#entra no usuario e le os favoritos
user = "/usuario/dj_crissi/"
#user = "/usuario/lauar/"
userFavourites = getFavourites(user)
userWatched = getUserWatched(user)
userDontWantToSee = getUserDontWantToSee(user)
userFavouritesLength = len(userFavourites)
	#abre lista de usuários
"""


threadAmount = 200

userList = readListFile("users.txt")
#abre arquivo de ja lidos e subtrai eles do userList
try:
	usersFavouritesList = readListFile("data2.bin")
except IOError:
	saveListFile([],"data2.bin")
	usersFavouritesList = []

usersRead = []
for u in usersFavouritesList:
	usersRead.append(u[0])

userList = list(set(userList) - set(usersRead))


#limit = 1000
firstUserIdToRead = 0
lastUserIdToRead = 100000


# chops list for the threads
chopNumber = int((lastUserIdToRead - firstUserIdToRead) / threadAmount)
startIndex = firstUserIdToRead
endIndex = firstUserIdToRead + chopNumber 
l=[]
#usersFavouritesList = []
threadList = []

while(endIndex < lastUserIdToRead):
	print("from "+str(startIndex)+" to "+str(endIndex))
	userChoppedList = userList[startIndex:endIndex]
	threadThread = threading.Thread(target = getAllUsersFavourites, args = (userChoppedList,usersFavouritesList))
	threadThread.start()
	for k in userChoppedList:
		l.append(k)
	threadList.append(threadThread)
	startIndex+=chopNumber
	endIndex+=chopNumber

#thread for saving file
threadThread = threading.Thread(target = waitAndSave, args = (usersFavouritesList,))
threadThread.start()


"""
allDone = False
while (not allDone):
	allDone = True
	for t in threadList:
		if (t.isAlive()):
			#allDone = False
			time.sleep(1)
			break


	#compare with current user
usersAndIntersection = []
print("\n\ncalculating intersection between users...\n\n")
listOfUsersAndFavouritesIntersection = []
for unf in usersFavouritesList:
	#converte para conjunto, faz intersecao e calcula comprimento
#	print(unf[1])
	sUnf = set(unf[1])
	sUser = set(userFavourites)
	favouritesIntersection = sUnf & sUser
	userAndIntersection = []
	userAndIntersection.append(unf[0])	#name
	userAndIntersection.append(list(favouritesIntersection))
	userAndIntersection.append(len(unf[1]))		# amount of favorites
	listOfUsersAndFavouritesIntersection.append(userAndIntersection)
l = listOfUsersAndFavouritesIntersection
	#calculates user with biggest intersection

UserWithBiggestIntersection = ""
biggestScore = 0
index = 0
for uafi in listOfUsersAndFavouritesIntersection:
	if (uafi[0] == user):
		continue
	if (uafi[2] == 0):
		continue	#if the current user has zero favourites, continues
	coeficient = uafi[2]/userFavouritesLength	# the bigger this coeficient, the lower this person's "score" is.
	if (coeficient <= 1):
		coeficient = 1	#div by zero correction (and else)
	score = len(uafi[1])/coeficient
	if (score>biggestScore):
		biggestScore = score
		lenOfBiggestIntersection = len(uafi[1])
		UserWithBiggestIntersection = uafi[0]
		k = uafi
		c = coeficient		
		matchIdo = index
	index += 1

u = UserWithBiggestIntersection
l = lenOfBiggestIntersection
print(u+" score:",biggestScore)
print(k)

"""






