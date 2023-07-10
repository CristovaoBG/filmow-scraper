import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import listUtils
from math import floor
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
	# autosave
	while (not allDone):
		allDone = True
		for t in threadList:
			if (t.is_alive()):
				allDone = False
				time.sleep(10)
				listUtils.saveListFile(usersList,f"partial_{fileName}")
				print(floor(len(usersList)/30), "paginas lidas.")
				break
	print("Threads finalizadas. Total de paginas lidas:",floor(len(usersList)/30))
	print("salvando lista de usuarios...")
	
	updateUserList(usersList, fileName)
	print("lista de usuarios salva com sucesso.")
	isAllDone = True

def updateUserList(usersList, fileName):
    dfNew = pd.DataFrame({'User':usersList})
    #try to read from file
    try:
        df = pd.read_csv(fileName)
        df = pd.concat([df,dfNew],ignore_index=True)
        df = df.drop_duplicates()
    except FileNotFoundError:
        df = dfNew
        
    df.to_csv(fileName, index = False)
    return df

def readUserNames(nameOutput = "users.txt", pagesToRead = 7000, threadAmount = 200,verbose=False, veryVerbose = False):
	print("lendo lista de usuarios, aguarde...")
	userList = []
	global globalDoneReadingUserNames
	# go through the pages with users in it
	usersList = []

	chopNumber = int(pagesToRead/threadAmount)

	pageStart = 1
	pageEnd = chopNumber
	pagesRead = 0
	threadList = []
	while(pageStart <= pagesToRead):
		if(verbose):
			print("from "+str(pageStart)+" to "+ str(pageEnd))
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
    #df = updateUserList(['a','b','c'],"output.csv")
	readUserNames(nameOutput = "usersTest.txt", pagesToRead = 100, threadAmount = 20,verbose = True, veryVerbose = True )
    
    #usersTest.txt