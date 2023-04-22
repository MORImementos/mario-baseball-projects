import requests
from utils import character_aliases
from utils.make_percentage import percentage, add_percent_sign

"""pull swing event data from restful api and output various requested stats"""

url = 'https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_swing=1&tag=ranked'

# get user request
print("Enter name of character (blank for all stats):")
char = input()

if char.lower() in character_aliases.aliases:
    char = character_aliases.mappings[character_aliases.aliases[char.lower()]]

print("Enter '0' for bunt; '1' for none; '2 for slap'; '3 for charge'; '4 for star':")
hit_type = int(input())

if hit_type == 0:
    swing = "Bunt"
elif hit_type == 1:
    swing = "None"
elif hit_type == 2:
    swing = "Slap"
elif hit_type == 3:
    swing = "Charge"
elif hit_type == 4:
    swing = "Star"

if char != "":
    url += "&by_char=1"

# get url link for both summary and by user information
total_response = requests.get(url).json()
total_char_response = requests.get(url + "&by_user=1").json()

user_dict = {}

overall = {}

# add overall stats to character specific dict and to overall dict
if char == "":
    overall = total_response["Stats"]["Batting"][swing]
else:
    overall = total_response["Stats"][char]["Batting"][swing]

# naming lots of variables
singles = overall["singles"]
doubles = overall["doubles"]
triples = overall["triples"]
homeruns = overall["homeruns"]
plate_appearances = overall["plate_appearances"]
extra_base_hits = str(round((doubles + triples + homeruns) / (singles + doubles + triples + homeruns) * 100, 1))
perfect_hits = overall["perfect_hits"]
sour_hits = overall["sour_hits"]
nice_hits = overall["nice_hits"]
strikeouts = overall["strikeouts"]
multi_out = overall["multi_out"]
fair = overall["fair_hits"]
foul = overall["foul_hits"]
outs = overall["outs"]
contact_rates = {"sour": sour_hits / (sour_hits + nice_hits + perfect_hits),
                 "nice": nice_hits / (sour_hits + nice_hits + perfect_hits),
                 "perfect": perfect_hits / (sour_hits + nice_hits + perfect_hits)}
sour = contact_rates["sour"]
nice = contact_rates["nice"]
perfect = contact_rates["perfect"]

# print overall stats
print(f'{char}', "-", "Overall:", plate_appearances, "PA /",
      round((singles + doubles + triples + homeruns) / plate_appearances, 3), "AVG / ",
      extra_base_hits + "% extra base hits")
print(str(round(sour * 100, 1)) + "% sour / " + str(round(nice * 100, 1)) + "% nice / " + str(
    round(perfect * 100, 1)) + "% perfect")
print(add_percent_sign(percentage(multi_out / plate_appearances)), "Multi Out Rate /",
      add_percent_sign(percentage(foul / (fair + foul))), "Foul Rate /",
      add_percent_sign((percentage(strikeouts / plate_appearances))), "Strikeout Rate\n")

# calculate user stats
for user in total_char_response["Stats"]:
    stats = {}
    # add to dict
    try:
        if char == "":
            stats = total_char_response["Stats"][user]["Batting"][swing]
        elif char in total_char_response["Stats"][user]:
            stats = total_char_response["Stats"][user][char]["Batting"][swing]
        else:
            continue

        singles = stats["singles"]
        doubles = stats["doubles"]
        triples = stats["triples"]
        homeruns = stats["homeruns"]
        rbi = stats["rbi"]
        plate_appearances = stats["plate_appearances"]

        strikeouts = stats["strikeouts"]
        multi_out = stats["multi_out"]
        fair = stats["fair_hits"]
        foul = stats["foul_hits"]
        outs = stats["outs"]
        total_outs = strikeouts + multi_out + outs

        perfect_hits = stats["perfect_hits"]
        sour_hits = stats["sour_hits"]
        nice_hits = stats["nice_hits"]

        # run stat calcs
        try:
            extra_base_hits = round((doubles + triples + homeruns) / (singles + doubles + triples + homeruns) * 100, 1)
            contact_rates = {"sour": sour_hits / (sour_hits + nice_hits + perfect_hits),
                             "nice": nice_hits / (sour_hits + nice_hits + perfect_hits),
                             "perfect": perfect_hits / (sour_hits + nice_hits + perfect_hits)}
            sour = contact_rates["sour"]
            nice = contact_rates["nice"]
            perfect = contact_rates["perfect"]
            average = round((singles + doubles + triples + homeruns) / plate_appearances, 3)
        except ZeroDivisionError:
            continue

        # make dict of all values to use for printing
        user_dict[user] = (
            singles, doubles, triples, homeruns, rbi, plate_appearances, strikeouts, multi_out, outs, perfect_hits,
            sour_hits, nice_hits, extra_base_hits, contact_rates, sour, nice, perfect, average, fair, foul)

    except KeyError:
        continue

#sort list by whatever
# todo make this editable by input?
# todo add fair/foul/star burn rate
sorted_user_list = sorted(user_dict.keys(), key=lambda x: user_dict[x][-4], reverse=True)

# print user stats
# todo iterate via function instead of all manually typed
for user in sorted_user_list:
    singles = user_dict[user][0]
    doubles = user_dict[user][1]
    triples = user_dict[user][2]
    homeruns = user_dict[user][3]
    rbi = user_dict[user][4]
    plate_appearances = user_dict[user][5]
    strikeouts = user_dict[user][6]
    multi_out = user_dict[user][7]
    outs = user_dict[user][8]
    perfect_hits = user_dict[user][9]
    nice_hits = user_dict[user][10]
    sour_hits = user_dict[user][11]
    extra_base_hits = user_dict[user][12]
    contact_rates = user_dict[user][13]
    sour = user_dict[user][14]
    nice = user_dict[user][15]
    perfect = user_dict[user][16]
    average = user_dict[user][17]
    fair = user_dict[user][18]
    foul = user_dict[user][19]

    if plate_appearances >= 20:
        # print(user, "/", average)
        # print(user + ":", plate_appearances, "PA / ", singles, " / ", doubles, " / ", triples, " / ", homeruns, " / ",  str(extra_base_hits) + "% extra base hits")

        print(user, f"({plate_appearances} PA):", add_percent_sign(percentage(contact_rates["sour"])) + " sour / ",
              add_percent_sign(percentage(contact_rates["nice"])) + " nice / ",
              add_percent_sign(percentage(contact_rates["perfect"])) + " perfect")
        try:
            print(str(extra_base_hits) + "% extra base hits / ", rbi, "RBI /", round(plate_appearances / rbi, 2), "PA per RBI")
        except ZeroDivisionError:
            print(str(extra_base_hits) + "% extra base hits / ", rbi, "RBI")
        print(add_percent_sign(percentage(multi_out / plate_appearances)), "Multi Out Rate /", add_percent_sign(percentage(foul / (fair + foul))), "Foul Rate /", add_percent_sign((percentage(strikeouts / plate_appearances))), "Strikeout Rate\n")
