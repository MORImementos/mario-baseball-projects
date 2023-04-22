import json
from glob import glob
"""calculate runs per inning"""

user = "MORI"

for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            innings = []
            try:
                sf = json.load(json_file)
                events = sf["Events"]

                inning_select_9 = False
                user_home = False
                user_in_game = False

                if sf["Away Player"] == user:
                    user_in_game = True

                if sf["Home Player"] == user:
                    user_home = True
                    user_in_game = True
                    half_inning = 1

                    for event in events:
                        try:
                            if event["Half Inning"] == 1 and event["Outs"] + event["Num Outs During Play"] == 3:
                                if user_home == True:
                                    for i in range(1,10):
                                        if event["Inning"] == i:
                                            innings.append(event["Home Score"] + event["RBI"])
                        except json.JSONDecodeError:
                            continue
                print(json_file.name, [j-1 for i, j in zip(innings[:-1], innings[1:])])
            except json.JSONDecodeError:
                print(json_file.name)

