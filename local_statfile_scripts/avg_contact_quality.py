from glob import glob
import os
import json
from collections import defaultdict
from statistics import mean

"""get average quality of contact of a given hit"""
# todo convert to function that can receive arguments for swing type etc
directory = os.chdir(r"C:\Users\micah\Documents\Project Rio\StatFiles")

event_list = []
events = defaultdict(list)
contact_quality = {}
contact_type = {}

for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            stat_file = json.load(json_file)

            if stat_file["Ranked"] == 1:
                user = "MORI"
                if user == stat_file["Home Player"]:
                    half_inning = 1
                elif user == stat_file["Away Player"]:
                    half_inning = 0

                else:
                    continue

                for data in stat_file["Events"]:
                    try:
                        for char in stat_file["Character Game Stats"].values():
                            if char["Superstar"] == 0:
                                if data["Half Inning"] == half_inning:
                                    if data["Pitch"]["Contact"]:
                                        if data["Pitch"]["Type of Swing"] == "Charge":
                                            contact = data["Pitch"]["Contact"]
                                            batter = data["Runner Batter"]["Runner Char Id"]

                                            if batter not in contact_quality:
                                                if contact["Type of Contact"] != "Sour - Right" and contact["Type of Contact"] != "Sour - Left" and contact["Type of Contact"] != "Perfect":
                                                    contact_quality[batter] = []
                                                    contact_quality[batter].append(contact["Contact Quality"])
                                            else:
                                                if contact["Type of Contact"] != "Sour - Right" and contact["Type of Contact"] != "Sour - Left" and contact["Type of Contact"] != "Perfect":
                                                    contact_quality[batter].append(contact["Contact Quality"])

                    except KeyError:
                            continue
                

for k, v in contact_quality.items():
    maximum = max(v)
    maximum = round(maximum, 5)
    minimum = min(v)
    minimum = round(minimum, 5)
    average = round(mean(v), 5)

    # if minimum != 0:
    #     print(k, "/", maximum, "max /", minimum, "min /", average, "average")
    # else:
    #     print(k, "/", maximum, "max /", average, "average")

    print(k, average, "average")
    # print(k, v)

