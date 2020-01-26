import string
import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import timeit

def openSoup(httpLink):
	htmlText = urllib.request.urlopen(httpLink).read()
	soup = BeautifulSoup(htmlText, 'html.parser')
	return soup

def readUserPages(pageStart,pageEnd, userList):
	for i in range(pageStart,pageEnd):
		global pagesRead
		url = urlBase + str(i)
		try:
			soup = openSoup(url)
		except:
			continue
		peopleList = soup.find_all("li",class_="people-list-item")
		for person in peopleList:
			userList.append(person.find("a")['href'])
		pagesRead += 1

def checkIfOver(threadList,usersList):
	allDone = False
	while (not allDone):
		allDone = True
		for t in threadList:
			if (t.isAlive()):
				allDone = False
				time.sleep(1)
				break
	print("salvando lista de usuarios...")
	with open("users.txt",'w') as f:
		for u in usersList:
			f.write(u+'\n')
	print("lista de usuarios salva com sucesso.")

def readUserNames(threadAmount,pagesToRead):
	global globalDoneReadingUserNames
#	threadAmount = 100
#	pagesToRead = 200#70000
	# go through the pages with users in it
	urlBase = "https://filmow.com/usuarios/?pagina="
	usersList = []

	chopNumber = int(pagesToRead/threadAmount)

	pageStart = 1
	pageEnd = chopNumber
	pagesRead = 0
	threadList = []
	while(pageStart < pagesToRead):
		#print("from "+str(pageStart)+" to "+str(pageEnd))
		newThread = threading.Thread(target = readUserPages, args = (pageStart,pageEnd,usersList))
		newThread.start()
		threadList.append(newThread)
		pageStart+=chopNumber
		pageEnd+=chopNumber
	#thread that checks if other threads are done
	threadThreadChecker = threading.Thread(target = checkIfOver, args = (threadList,usersList))
	threadThreadChecker.start()

#readUserNames(100,2000)

#exec(open("filmow.py").read())









