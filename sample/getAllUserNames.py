import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import listUtils
from math import floor
import pandas as pd

url_base = "https://filmow.com/usuarios/?pagina="
pages_read = 0
is_all_done = False

def open_soup(http_link):
	html_text = urllib.request.urlopen(http_link).read()
	soup = BeautifulSoup(html_text, 'html.parser')
	return soup

def read_user_pages(page_start,page_end, user_list, verbose = False):
	global url_base
	global pages_read
	for i in range(page_start,page_end):
		#print("lendo pagina",str(i))
		global pages_read
		url = url_base + str(i)
		try:
			soup = open_soup(url)
		except:
			continue
		people_list = soup.find_all("li",class_="people-list-item")
		for person in people_list:
			#ignora /usuario/ e / do inicio e do final, respectivamente
			user_list.append(person.find("a")['href'][9:-1])
		pages_read += 1

def check_if_over(thread_list,users_list,filename, verbose = True):
	global is_all_done
	all_done = False
	# autosave
	while (not all_done):
		all_done = True
		for t in thread_list:
			if (t.is_alive()):
				all_done = False
				time.sleep(10)
				listUtils.save_list_file(users_list,f"partial_{filename}")
				print(floor(len(users_list)/30), "paginas lidas.")
				break
	print("Threads finalizadas. Total de paginas lidas:",floor(len(users_list)/30))
	print("salvando lista de usuarios...")
	
	udpate_user_list(users_list, filename)
	print("lista de usuarios salva com sucesso.")
	is_all_done = True

def udpate_user_list(user_list, filename):
    df_new = pd.DataFrame({'User':user_list})
    #try to read from file
    try:
        df = pd.read_csv(filename)
        df = pd.concat([df,df_new],ignore_index=True)
        df = df.drop_duplicates()
    except FileNotFoundError:
        df = df_new
        
    df.to_csv(filename, index = False)
    return df

def read_user_names(name_output = "users.txt", pages_to_read = 7000, thread_amount = 200,verbose=False, very_verbose = False): #TODO: usar niveis de log?
	print("lendo lista de usuarios, aguarde...")
	# go through the pages with users in it
	users_list = []

	chop_number = int(pages_to_read/thread_amount)

	page_start = 1
	page_end = chop_number
	thread_list = []
	while(page_start <= pages_to_read):
		if(verbose):
			print("from "+str(page_start)+" to "+ str(page_end))
		new_thread = threading.Thread(target = read_user_pages, args = (page_start,page_end,users_list,very_verbose))
		new_thread.start()
		thread_list.append(new_thread)
		page_start+=chop_number
		page_end+=chop_number
	#does last threads

	#thread that checks if other threads are done
	thread_threadchecker = threading.Thread(target = check_if_over, args = (thread_list,users_list,name_output, verbose))
	thread_threadchecker.start()

	#stops this thread if hasnt finished everything saveListFile
	while(is_all_done == False):
		time.sleep(1)

#exec(open("getAllUserNames.py").read())
if __name__ == "__main__":
    #df = updateUserList(['a','b','c'],"output.csv")
	read_user_names(name_output = "usersTest.txt", pages_to_read = 10000, thread_amount = 20,verbose = True, very_verbose = True )
    
    #usersTest.txt