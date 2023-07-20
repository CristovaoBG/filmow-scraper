

#compare with current user
users_and_intersections= []
print("\n\ncalculating intersection between users...\n\n")
listOfUsersAndFavouritesIntersection = []
for unf in users_favorites_list:
	#converte para conjunto, faz intersecao e calcula comprimento
#	print(unf[1])
	sUnf = set(unf[1])
	sUser = set(user_favorites)
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
	if (uafi[0] == user or uafi[0] == "/usuario/hug0alex/" or uafi[0] == "/usuario/ariellybarbosa9/"):
		continue
	if (uafi[2] == 0):
		continue	#if the current user has zero favourites, continues
	coeficient = uafi[2]/users_favorites_length	# the bigger this coeficient, the lower this person's "score" is.
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
"""
	if (len(uafi[1])>lenOfBiggestIntersection):        #this calculates a coeficient based in the number of favourites this person has
		lenOfBiggestIntersection = len(uafi[1])
		UserWithBiggestIntersection = uafi[0]
		k = uafi
		c = coeficient
"""
u = UserWithBiggestIntersection
l = lenOfBiggestIntersection
print(u+" score:",biggestScore)
print(k)








