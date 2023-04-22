"""make variables with empty lists at time of running script"""
def make_empty_lists(noprint=0):
	
	list_dict = {}
	
	while True:
		list_name = input("Enter name of list: ")
		title = str(list_name).replace(" ", "_")
		if title == "":
			if noprint == 1:
				break
			if noprint == 0:
				print("Lists created in list_dict: ")
				for name, list in list_dict.items():
					print(name)
			break
		else:
			
			list_dict[title] = []
		
		
				
	return list_dict
			
			
list_dict = make_empty_lists(1)
print(list_dict)
