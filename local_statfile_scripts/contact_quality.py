import json
from glob import glob

"""generate contact quality values by character"""

# todo convert to function that can receive character, swing type, etc. as arguments
# char = input("Input character: ")
user = "MORI"

nice_cq = []
nice_avg_cq = 0
nice_count = 0
sour_cq = []
sour_avg_cq = 0
sour_count = 0
hr = 0
at_bat = 0
hits = 0
rbi = 0
nice = 0
sour = 0
perfect = 0
strikeouts = 0

for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            try:
                stat_file = json.load(json_file)
                events = stat_file["Events"]
                home_player = stat_file["Home Player"]
                away_player = stat_file["Away Player"]
                is_starsoff = False
                if home_player == user:
                    half_inning = 1
                    team = "0"
                if away_player == user:
                    half_inning = 0
                    team = "1"

                for char in stat_file["Character Game Stats"].values():
                    if char["CharID"] == "Petey" and char["Team"] == team and char["Superstar"] == 0:
                        hr += char["Offensive Stats"]["Homeruns"]
                        at_bat += char["Offensive Stats"]["At Bats"]
                        hits += char["Offensive Stats"]["Hits"]
                        rbi += char["Offensive Stats"]["Hits"]
                        strikeouts += char["Offensive Stats"]["Strikeouts"]

                        for event in events:
                            try:
                                if event["Runner Batter"]["Runner Char Id"] == "Petey" and event["Pitch"]["Type of Swing"] == "Charge" and char["Superstar"] == 0:
                                    type_of_contact = event["Pitch"]["Contact"]["Type of Contact"]
                                    if type_of_contact == "Nice - Left" or type_of_contact == "Nice - Right":
                                        nice += 1
                                    if type_of_contact == "Sour - Left" or type_of_contact == "Sour - Right":
                                        sour += 1
                                    if type_of_contact == "Perfect":
                                        perfect += 1
                            except KeyError:
                                continue


                    for event in events:
                        try:
                            # for when user is batting
                            if event["Half Inning"] == half_inning:
                                if (event["Pitch"]["Contact"]["Type of Contact"] == "Nice - Right") or (event["Pitch"]["Contact"]["Type of Contact"] == "Nice - Left") and event["Pitch"]["Type of Swing"] == "Charge":
                                    nice_cq.append(event["Pitch"]["Contact"]["Contact Quality"])
                                if (event["Pitch"]["Contact"]["Type of Contact"] == "Sour - Right") or (event["Pitch"]["Contact"]["Type of Contact"] == "Sour - Left") and event["Pitch"]["Type of Swing"] == "Charge":
                                    sour_cq.append(event["Pitch"]["Contact"]["Contact Quality"])
                                # if event["Runner Batter"]["Runner Char Id"] == "Petey" and event["Pitch"]["Type of Swing"] == "Charge" and char["Superstar"] == 0:
                                #     print(event["Pitch"]["Contact"]["Type of Contact"])
                                    # print(event["Pitch"]["Contact"]["Contact Result - Secondary"])

                        except KeyError:
                            continue



            except json.JSONDecodeError:
                continue

for i in nice_cq:
    nice_avg_cq += i
    nice_count += 1
print(round(nice_avg_cq / nice_count, 3))


for i in sour_cq:
    sour_avg_cq += i
    sour_count += 1
try:
    print(round(sour_avg_cq / sour_count, 3))
except ZeroDivisionError:
    pass

try:
    print(at_bat / hr)
except ZeroDivisionError:
    pass

try:
    print(at_bat / rbi)
except ZeroDivisionError:
    pass

try:
    print(hits / at_bat)
except ZeroDivisionError:
    pass

try:
    print((nice + perfect) / (nice + sour + perfect))
except ZeroDivisionError:
    pass

try:
    print(strikeouts / at_bat)
except ZeroDivisionError:
    pass




