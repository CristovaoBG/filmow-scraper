import string
import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import timeit
from listUtils import *

stop_all_threads = False
user_count = 0
def stop():
	stop_all_threads = True

def get_favorites(user_string):
	movie_name_list = []
	url_user = "https://filmow.com"+"/usuario/" + user_string + "/"
	page_id = 1
	while(True):
		try:
			user_favorites_soup = openSoup(url_user+"filmes/favoritos/?pagina="+str(page_id))
		except:
			break
		all_movies = user_favorites_soup.find_all("li",class_="movie_list_item")
		#print("reading: "+ urlUser+"filmes/favoritos/?pagina="+str(pageID))
		for movie in all_movies:
			movie_name = movie.find("a")['href'][1:-1] #[1:-1] pra eliminar os "/"
			movie_name_list.append(movie_name)
		page_id+=1
	return movie_name_list

def get_user_watched(user_string):
	movie_name_list = []
	url_user = "https://filmow.com" + user_string
	page_id = 1
	#https://filmow.com/usuario/dj_crissi/filmes/ja-vi/?pagina=
	while(True):
		try:
			user_favorites_soup = openSoup(url_user+"filmes/ja-vi/?pagina="+str(page_id))
		except:
			break
		all_movies = user_favorites_soup.find_all("li", class_="movie_list_item")
		print(f"reading: {url_user}filmes/ja-vi/?pagina={page_id}")
		for movie in all_movies:
			movie_name = movie.find("a")['title']
			movie_name_list.append(movie_name)
		page_id+=1
	return movie_name_list

def get_user_dont_want_to_see(user_string):
	movie_name_list = []
	url_user = "https://filmow.com"+user_string
	page_id = 1
	#https://filmow.com/usuario/dj_crissi/filmes/ja-vi/?pagina=
	while(True):
		try:
			user_unfavorites_soup = openSoup(url_user+"filmes/ja-vi/?pagina="+str(page_id))
		except:
			break
		all_movies = user_unfavorites_soup.find_all("li",class_="movie_list_item")
		print("reading: "+ url_user+"filmes/nao-quero-ver/?pagina="+str(page_id))
		for movie in all_movies:
			movie_name = movie.find("a")['title']
			movie_name_list.append(movie_name)
		page_id+=1
	return movie_name_list

def thread_test(thread_num):
	print("thread number "+ str(thread_num) + " started.")
	time.sleep(2)
	print("thread number "+ str(thread_num) + " finished.")


def get_all_users_favorites_thread(user_list,users_favorites_list):
	i=0
	global stop_all_threads
	global user_count
	for u in user_list:
		#print("reading user "+ u +"   user number: "+str(i))
		currentUserFavourite = get_favorites(u)
		userAndFavourites = []
		# userAndFavourites.append(u)
		# userAndFavourites.append(currentUserFavourite)
		# usersFavouritesList.append(userAndFavourites)
		if(len(currentUserFavourite)>0):
			users_favorites_list.append([u,currentUserFavourite])
		#print("DONE user "+ u +"   user number: "+str(i))
		user_count+=1
		i+=1
		if stop_all_threads:
			break

def wait_and_save(users_favorites_list, output_file):
	global stop_all_threads
	while (stop_all_threads == False):
		time.sleep(60)
		print("arquivo salvo!")
		save_list_file(users_favorites_list, output_file)



def get_all_users_favorites(user_list, thread_amount=200, output_file = "usersFavourites",number_of_users_to_read=1000):
	global stop_all_threads
	global user_count
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
		users_favorites_list = read_list_file(output_file)
	except IOError:
		save_list_file([],output_file)
		users_favorites_list = []

	users_read = []
	for u in users_favorites_list:
		users_read.append(u[0])

	user_list = list(set(user_list) - set(users_read))


	#limit = 1000
	first_user_id_to_read = 0
	last_user_id_to_read = number_of_users_to_read


	# chops list for the threads
	chop_number = int((last_user_id_to_read - first_user_id_to_read) / thread_amount)
	start_index = first_user_id_to_read
	end_index = first_user_id_to_read + chop_number
	l=[]
	#usersFavouritesList = []
	thread_list = []

	while(end_index < last_user_id_to_read):
		#print("from "+str(startIndex)+" to "+str(endIndex))
		user_chopped_list = user_list[start_index:end_index]
		thread_ = threading.Thread(target = get_all_users_favorites_thread, args = (user_chopped_list,users_favorites_list))
		thread_.start()
		for k in user_chopped_list:
			l.append(k)
		thread_list.append(thread_)
		start_index+=chop_number
		end_index+=chop_number

	#thread for saving file
	thread_ = threading.Thread(target = wait_and_save, args = (users_favorites_list,output_file,))
	thread_.start()

	all_done = False
	while(not all_done):
		all_done = True
		for t in thread_list:
			if (t.is_alive()):
				all_done = False
				time.sleep(5)
				print("usuarios lidos:",user_count)
				break
	stop_all_threads = True	#pra parar a thread de salvar, somente
	print("!!!!!!!!!!!!!!!Finalizado!!!!!!!!!!!!!!!!")
