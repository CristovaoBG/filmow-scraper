import string
import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import timeit
from listUtils import *
from math import *
import pandas as pd

urlBase = "https://filmow.com/usuarios/?pagina="
pagesRead = 0
isAllDone = False

def openSoup(httpLink):
	htmlText = urllib.request.urlopen(httpLink).read()
	soup = BeautifulSoup(htmlText, 'html.parser')
	return soup

def readUserPages(pageStart,pageEnd, userList, verbose = False):
	global urlBase
	global pagesRead
	for i in range(pageStart,pageEnd):
		#print("lendo pagina",str(i))
		global pagesRead
		url = urlBase + str(i)
		try:
			soup = openSoup(url)
		except:
			continue
		peopleList = soup.find_all("li",class_="people-list-item")
		for person in peopleList:
			#ignora /usuario/ e / do inicio e do final, respectivamente
			userList.append(person.find("a")['href'][9:-1])
		pagesRead += 1

def checkIfOver(threadList,usersList,fileName, verbose = True):
	global isAllDone
	allDone = False
	while (not allDone):
		allDone = True
		for t in threadList:
			if (t.is_alive()):
				allDone = False
				time.sleep(10)
				saveListFile(usersList,fileName)
				print(floor(len(usersList)/30), "paginas lidas.")
				break
	print("total de paginas lidas:",floor(len(usersList)/30))
	print("salvando lista de usuarios...")
	saveListFile(usersList,fileName)
	print("lista de usuarios salva com sucesso.")
	isAllDone = True

def readUserNames(nameOutput = "users.txt", pagesToRead = 7000, threadAmount = 200,verbose=False, veryVerbose = False):
	#def readUserNames(threadAmount,pagesToRead):
	#threadAmount = 200
	#pagesToRead = 70000
	print("lendo lista de usuarios, aguarde...")
	userList = []
	global globalDoneReadingUserNames
	#	threadAmount = 100
	#	pagesToRead = 200#70000
	# go through the pages with users in it
	usersList = []

	chopNumber = int(pagesToRead/threadAmount)

	pageStart = 1
	pageEnd = chopNumber
	pagesRead = 0
	threadList = []
	while(pageStart <= pagesToRead):
		if(verbose):
			print("from "+str(pageStart)+" to "+str(pageEnd))
		newThread = threading.Thread(target = readUserPages, args = (pageStart,pageEnd,usersList,veryVerbose))
		newThread.start()
		threadList.append(newThread)
		pageStart+=chopNumber
		pageEnd+=chopNumber
	#does last threads

	#thread that checks if other threads are done
	threadThreadChecker = threading.Thread(target = checkIfOver, args = (threadList,usersList,nameOutput, verbose))
	threadThreadChecker.start()

	#stops this thread if hasnt finished everything saveListFile
	while(isAllDone == False):
		time.sleep(1)

#exec(open("getAllUserNames.py").read())
if __name__ == "__main__":
    df = pd.DataFrame([],columns=['userName'])
	#readUserNames(nameOutput = "usersTest.txt", pagesToRead = 100, threadAmount = 20,verbose = True, veryVerbose = True )
    #usersTest.txt