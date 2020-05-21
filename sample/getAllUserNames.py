import string
import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import timeit
import pickle

urlBase = "https://filmow.com/usuarios/?pagina="
pagesRead = 0

def openSoup(httpLink):
	htmlText = urllib.request.urlopen(httpLink).read()
	soup = BeautifulSoup(htmlText, 'html.parser')
	return soup

def readUserPages(pageStart,pageEnd, userList):
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
#	with open("users.txt",'w') as f:
#		for u in usersList:
#			f.write(u+'\n')
	with open("users.txt","wb") as d:
		pickle.dump(usersList,f)
	print("lista de usuarios salva com sucesso.")

#def readUserNames(threadAmount,pagesToRead):
threadAmount = 200
pagesToRead = 70000
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









