import string
import urllib.request
from bs4 import BeautifulSoup
import pickle
import os

def openSoup(httpLink):
	htmlText = urllib.request.urlopen(httpLink).read()
	soup = BeautifulSoup(htmlText, 'html.parser')
	return soup

def read_list_file(fileName):
	with open(fileName,"rb") as fp:
		listReturn = pickle.load(fp)
	return listReturn

def save_list_file(listInput, fileName):
	with open(fileName,"wb") as fp:
		pickle.dump(listInput,fp)
        

def execFile(fileName):
	exec(open(fileName).read())
