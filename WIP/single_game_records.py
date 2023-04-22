import json
from glob import glob

"""
Script for parsing local MSSB statfiles and outputting results that are among the best for the user.
"""

# todo implement a loop that iterates until the highest value has been reached instead of arbitrarily assigning values
# char = input("Input character: ")
user = "MORI"

hit = 0
doubles = 0
triples = 0
homeruns = 0
rbi = 0
sb = 0
strikeouts = 0
big_plays = 0
least_hits_allowed = None
o_stat_type = ['Hits', 'Doubles', 'Triples', 'Homeruns', 'RBI', 'Bases Stolen']
d_stat_type = ['Strikeouts', 'Big Plays', 'Hits Allowed']
for f_name in glob('*.json'):
	if f_name in glob('decoded.*'):
		with open(f_name) as json_file:

			try:
				stat_file = json.load(json_file)
				for char in stat_file["Character Game Stats"].values():
					o_stat_type = [stat for stat in char["Offensive Stats"]]
					if stat_file["Ranked"] == 0:
						if (char["Team"] == "0" and stat_file["Away Player"] == user) or (char["Team"] == "1" and stat_file["Home Player"] == user) and char["Superstar"] == 0:
							def single_game_high(stat_category):
								high_list = [0, 0, 0, 0, 0, 0, 0, 0, 100]
								if stat_category != "Strikeouts" or stat_category != "Big Plays" or stat_category != "Hits Allowed":
									dc = char["Offensive Stats"][stat_category]
									for i in range(6):
										if dc > high_list[i]:
											high_list[i] = dc
									print(dc)
								else:
									dc = char["Defensive Stats"][stat_category]


							o_stat = list(map(single_game_high, o_stat_type))
							d_stat = list(map(single_game_high, d_stat_type))
				print(o_stat_type, o_stat, d_stat_type, d_stat)
							# high = [single_game_high(s, "s") for s in o_stat_type]
							# print(high)

			# 				if char["Offensive Stats"]["Hits"] > hits:
			# 					hits = char["Offensive Stats"]["Hits"]
			# 				if char["Offensive Stats"]["Doubles"] >= doubles:
			# 					print(char["CharID"]+" Doubles", char["Offensive Stats"]["Doubles"])
			# 				if char["Offensive Stats"]["Triples"] >= 2:
			# 					print(char["CharID"]+" Triples", char["Offensive Stats"]["Triples"])
			# 				if char["Offensive Stats"]["Homeruns"] >= 3:
			# 					print(char["CharID"]+" Homeruns", char["Offensive Stats"]["Homeruns"])
			# 				if char["Offensive Stats"]["RBI"] >= 8:
			# 					print(char["CharID"]+" RBI", char["Offensive Stats"]["RBI"])
			# 				if char["Offensive Stats"]["Bases Stolen"] >= 2:
			# 					print(char["CharID"]+" SB", char["Offensive Stats"]["Bases Stolen"])
			# 				if char["Defensive Stats"]["Strikeouts"] >= 15:
			# 					print(char["CharID"]+" K", char["Defensive Stats"]["Strikeouts"])
			# 				if char["Defensive Stats"]["Big Plays"] >= 4:
			# 					print(char["CharID"] + " Big Plays", char["Defensive Stats"]["Big Plays"])
			#
			except json.JSONDecodeError:
			 	continue
