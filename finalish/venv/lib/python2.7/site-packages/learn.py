
def recurList(the_list) :

	for i in the_list :

		if (isinstance(i, list)) :
			recurList(i)

		else :
			print(i)


