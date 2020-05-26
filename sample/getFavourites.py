import string
import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import timeit
from listUtils import *

stopAllThreads = False
userCount = 0
def stop():
	stopAllThreads = True

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
		#print("reading: "+ urlUser+"filmes/favoritos/?pagina="+str(pageID))
		for movie in allMovies:
			movieName = movie.find("a")['href']
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


def getAllUsersFavouritesThread(userList,usersFavouritesList):
	i=0
	global stopAllThreads
	global userCount
	for u in userList:
		#print("reading user "+ u +"   user number: "+str(i))
		currentUserFavourite = getFavourites(u)
		userAndFavourites = []
		userAndFavourites.append(u)
		userAndFavourites.append(currentUserFavourite)
		usersFavouritesList.append(userAndFavourites)
		#print("DONE user "+ u +"   user number: "+str(i))
		userCount+=1
		i+=1
		if (stopAllThreads):
			break

def waitAndSave(usersFavouritesList,outputFile):
	global stopAllThreads
	while (stopAllThreads == False):
		time.sleep(60)
		print("arquivoSalvo!")
		saveListFile(usersFavouritesList,outputFile)

"""
usersRead = []
for u in usersFavouritesList
	usersRead.append(u[0])
"""

def getAllUsersFavourites(user,userList, threadAmount=200, outputFile = "usersFavourites",NumberOfUsersToRead=1000):
	global stopAllThreads
	global userCount
	startTime = timeit.default_timer()
	#entra no usuario e le os favoritos
	"""
	userFavourites = getFavourites(user)
	userWatched = getUserWatched(user)
	userDontWantToSee = getUserDontWantToSee(user)
	userFavouritesLength = len(userFavourites)
	"""
	#abre arquivo de ja lidos e subtrai eles do userList
	try:
		usersFavouritesList = readListFile(outputFile)
	except IOError:
		saveListFile([],outputFile)
		usersFavouritesList = []

	usersRead = []
	for u in usersFavouritesList:
		usersRead.append(u[0])

	userList = list(set(userList) - set(usersRead))


	#limit = 1000
	firstUserIdToRead = 0
	lastUserIdToRead = NumberOfUsersToRead


	# chops list for the threads
	chopNumber = int((lastUserIdToRead - firstUserIdToRead) / threadAmount)
	startIndex = firstUserIdToRead
	endIndex = firstUserIdToRead + chopNumber
	l=[]
	#usersFavouritesList = []
	threadList = []

	while(endIndex < lastUserIdToRead):
		#print("from "+str(startIndex)+" to "+str(endIndex))
		userChoppedList = userList[startIndex:endIndex]
		threadThread = threading.Thread(target = getAllUsersFavouritesThread, args = (userChoppedList,usersFavouritesList))
		threadThread.start()
		for k in userChoppedList:
			l.append(k)
		threadList.append(threadThread)
		startIndex+=chopNumber
		endIndex+=chopNumber

	#thread for saving file
	threadThread = threading.Thread(target = waitAndSave, args = (usersFavouritesList,outputFile,))
	threadThread.start()

	allDone = False
	while(not allDone):
		allDone = True
		for t in threadList:
			if (t.isAlive()):
				allDone = False
				time.sleep(5)
				print("usuarios lidos:",userCount)
				break
	stopAllThreads = True	#pra parar a thread de salvar, somente
	print("!!!!!!!!!!!!!!!Finalizado!!!!!!!!!!!!!!!!")
