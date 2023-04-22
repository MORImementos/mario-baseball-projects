import json
from glob import glob

"""
Search local MSSB statfiles and print specified event data
"""

# todo make it so user can give custom input
def contact_data(char, contact, swing_type):
	for f_name in glob('*.json'):
		if f_name in glob('decoded.*'):
			with open(f_name) as json_file:
				try:
					stat_file = json.load(json_file)
					for data in stat_file["Events"]:
						try:
							if data["Runner Batter"]["Runner Char Id"] == char:
								if data["Pitch"]["Contact"]["Type of Contact"] == contact:
									if data["Pitch"]["Type of Swing"] == swing_type:
										# print(data)
										print(data["Pitch"]["Contact"]["Frame of Swing Upon Contact"], "/", data["Pitch"]["Contact"]["Input Direction - Push/Pull"], "/", data["Result of AB"],"/", data["Pitch"]["Contact"]["Contact Result - Secondary"])
						except KeyError:
							continue
				except json.JSONDecodeError:
					continue

contact_data("Petey", "Nice - Right", "Charge")