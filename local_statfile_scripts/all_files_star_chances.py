from utils import RioStatLib
import json
from glob import glob

"""just revised from MattGree's version that reads a single file to iterate over all files in a directory"""

for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            stat_file = json.load(json_file)
            sf = stat_file
            myStats = RioStatLib.StatObj(stat_file)

            all_events = myStats.events()
            star_chance_opportunity = 0
            star_chance = 0
            home_defensive_star_chance_opportunities = 0
            home_defensive_star_chance = 0
            away_defensive_star_chance_opportunities = 0
            away_defensive_star_chance = 0

            for event in all_events:
                if event["Balls"] == 0 and event["Strikes"] == 0:
                    if ("Runner 1B" not in event.keys()) and ("Runner 2B" not in event.keys()) and ("Runner 3B" not in event.keys()) and event["Event Num"] != 0 and ("Pitch" in event.keys()):
                        star_chance_opportunity +=1
                        if event["Half Inning"] == 0:
                            home_defensive_star_chance_opportunities += 1
                        else:
                            away_defensive_star_chance_opportunities += 1
                        if event["Star Chance"] == 1:
                            star_chance += 1
                            if event["Half Inning"] == 0:
                                home_defensive_star_chance += 1
                            else:
                                away_defensive_star_chance += 1
            if star_chance_opportunity > 0:
                print("Star Chance Opportunities: " + str(star_chance_opportunity) + "   " + "Star Chances: " + str(star_chance) + "   " + "Star Chance Rate: {:0.2f}%".format(float(100 * star_chance / star_chance_opportunity)))
                print("{} Defensive Star Chance Opportunities: ".format(myStats.player(0)) + str(home_defensive_star_chance_opportunities) + "   " "Star Chances: " + str(home_defensive_star_chance) + "   " + "Star Chance Rate: {:0.2f}%".format(float(100 * home_defensive_star_chance / home_defensive_star_chance_opportunities)))
                print("{} Defensive Star Chance Opportunities: ".format(myStats.player(1)) + str(away_defensive_star_chance_opportunities) + "   " "Star Chances: " + str(away_defensive_star_chance) + "   " + "Star Chance Rate: {:0.2f}%".format(float(100 * away_defensive_star_chance / away_defensive_star_chance_opportunities)))
                print()