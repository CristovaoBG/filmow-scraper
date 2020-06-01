import string
import urllib.request
from bs4 import BeautifulSoup
import pickle

def openSoup(httpLink):
	htmlText = urllib.request.urlopen(httpLink).read()
	soup = BeautifulSoup(htmlText, 'html.parser')
	return soup

def readListFile(fileName):
	with open(fileName,"rb") as fp:
		listReturn = pickle.load(fp)
	return listReturn

def saveListFile(listInput, fileName):
	with open(fileName,"wb") as fp:
		pickle.dump(listInput,fp)

def execFile(fileName):
	exec(open(fileName).read())
