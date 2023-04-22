import json
from glob import glob

"""older script that was used to determine the 'career high' of a player in several categories"""

# char = input("Input character: ")
user = "MORI"
k = {}
o_k = {}
sum_k = 0
games = 0
sum_o_k = 0
sum_bf = 0
sum_o_bf = 0

for f_name in glob('*.json'):
	if f_name in glob('decoded.*'):
		with open(f_name) as json_file:
			try:
				stat_file = json.load(json_file)
				for char in stat_file["Character Game Stats"].values():
					if (char["Team"] == "1" and stat_file["Away Player"] == user) or (char["Team"] == "0" and stat_file["Home Player"] == user) and char["Superstar"] == 0:
						for i in range(1, 16):
							if char["Defensive Stats"]["Strikeouts"] == i:
								if i not in k:
									k[i] = 0
									k[i] += 1
								else:
									k[i] += 1
						if char["Offensive Stats"]["Hits"] >= 8:
							print(char["CharID"]+" Hits", char["Offensive Stats"]["Hits"])
						if char["Offensive Stats"]["Doubles"] >= 5:
							print(char["CharID"]+" Doubles", char["Offensive Stats"]["Doubles"])
						if char["Offensive Stats"]["Triples"] >= 3:
							print(char["CharID"]+" Triples", char["Offensive Stats"]["Triples"])
						if char["Offensive Stats"]["Homeruns"] >= 3:
							print(char["CharID"]+" Homeruns", char["Offensive Stats"]["Homeruns"])
						if char["Offensive Stats"]["RBI"] >= 8:
							print(char["CharID"]+" RBI", char["Offensive Stats"]["RBI"])
						if char["Offensive Stats"]["Bases Stolen"] >= 4:
							print(char["CharID"]+" SB", char["Offensive Stats"]["Bases Stolen"])
						if char["Defensive Stats"]["Strikeouts"] >= 15:
							print(char["CharID"]+" K", char["Defensive Stats"]["Strikeouts"])
						if char["Defensive Stats"]["Big Plays"] >= 7:
							print(char["CharID"] + " Big Plays", char["Defensive Stats"]["Big Plays"])

						sum_k += char["Defensive Stats"]["Strikeouts"]
						sum_bf += char["Defensive Stats"]["Batters Faced"]

					if (char["Team"] == "1" and stat_file["Away Player"] != user) or (char["Team"] == "0" and stat_file["Home Player"] != user) and char["Superstar"] == 0:
						for i in range(1, 16):
							if char["Defensive Stats"]["Strikeouts"] == i:
								if i not in o_k:
									o_k[i] = 0
									o_k[i] += 1
								else:
									o_k[i] += 1
						sum_o_k += char["Defensive Stats"]["Strikeouts"]
						sum_o_bf += char["Defensive Stats"]["Batters Faced"]


				games += 1
			# 	for event in stat_file["Events"]:
			# 		try:
			# 			if event["Runner Batter"]["Runner Char Id"] == char:
			# 			#if data["Pitch"]["Contact"]["Contact Result - Primary"] == "Fair" and data["Pitch"]["Contact"]["Contact Result - Secondary"] == "foul":
			# 				print(event["Event Num"], event["Result of AB"], "/", event["Pitch"]["Contact"]["Type of Contact"], "/", event["Pitch"]["Contact"]["Frame of Swing Upon Contact"], "/", event["Pitch"]["Contact"]["Contact Result - Primary"],"/", event["Pitch"]["Contact"]["Contact Result - Secondary"], "/", event["Pitch"]["Contact"]["Input Direction - Stick"])
			# 			else:
			# 				pass
			# 		except KeyError:
			# 			pass
			except json.JSONDecodeError:
			 	continue

print(sorted(k.items()))
tot = 968

print(sorted(o_k.items()))

per_count = [218/tot, 170/tot, 154/tot, 104/tot, 100/tot, 67/tot, 56/tot, 30/tot, 27/tot, 12/tot, 7/tot, 5/tot, 5/tot, 3/tot, 4/tot, 3/tot]
for i in per_count:
	print(round(i * 100, 1))

print(sum_k / sum_bf)
print(sum_o_k / sum_o_bf)

