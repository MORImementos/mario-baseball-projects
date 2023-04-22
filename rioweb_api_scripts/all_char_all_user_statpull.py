import requests
import csv

print("Enter '0' for stars-off data; '1' for stars-on")
stars = int(input())
print("Enter '0' for all data, '1' for ranked only")
ranked = int(input())

"""
pulls basic data from RioWeb API for everyone, by character and overall, and exports to csv file
"""



url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?exclude_pitching=1&exclude_fielding=1&exclude_misc=1&by_char=1&by_user=1"
era_multiplier = 9

if stars == 0:
    url += "&tag=Normal"
elif stars == 1:
    url += "&tag=Superstar"
    era_multiplier = 5
if ranked == 1:
    url += "&tag=Ranked"

response = requests.get(url).json()
char_stats = response["Stats"]

header = ['user', 'character', 'pa', 'avg', 'obp', 'slg', 'ops', 'hr', 'hr rate', 'rbi', 'ab']

with open('file.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

print("user, " + "character, " + "pa, " + "avg, " + "obp, " + "slg, " + "ops, " + "hr, " + "hr rate, " + "rbi, " + "ab")
for user in char_stats:
    characters = response["Stats"][user]
    user_summary_hits = 0
    user_summary_at_bats = 0
    user_summary_walks_hbp = 0
    user_summary_walks_bb = 0
    user_summary_singles = 0
    user_summary_doubles = 0
    user_summary_triples = 0
    user_summary_homeruns = 0
    user_summary_strikeouts = 0
    user_summary_rbi = 0
    user_walks = 0
    user_plate_appearances = 0
    for char in characters:
        char_stats = response["Stats"][user][char]["Batting"]
        if char_stats["plate_appearances"] and char_stats["summary_at_bats"] > 0:
            user_summary_hits += char_stats["summary_hits"]
            user_summary_at_bats += char_stats["summary_at_bats"]
            user_summary_walks_hbp += char_stats["summary_walks_hbp"]
            user_summary_walks_bb += char_stats["summary_walks_bb"]
            user_summary_singles += char_stats["summary_singles"]
            user_summary_doubles += char_stats["summary_doubles"]
            user_summary_triples += char_stats["summary_triples"]
            user_summary_homeruns += char_stats["summary_homeruns"]
            user_walks += (char_stats["summary_walks_hbp"] + char_stats["summary_walks_hbp"])
            user_summary_rbi += char_stats["summary_rbi"]
            user_plate_appearances += char_stats["summary_at_bats"]
            user_plate_appearances += char_stats["summary_walks_hbp"]
            user_plate_appearances += char_stats["summary_walks_bb"]

            avg = char_stats["summary_hits"] / char_stats["summary_at_bats"]
            pa = char_stats["summary_at_bats"] + char_stats["summary_walks_hbp"] + char_stats["summary_walks_bb"] + char_stats["summary_sac_flys"]
            obp = (char_stats["summary_hits"] + char_stats["summary_walks_hbp"] + char_stats["summary_walks_bb"]) / pa
            slg = (char_stats["summary_singles"] + (char_stats["summary_doubles"] * 2) + (char_stats["summary_triples"] * 3) + (char_stats["summary_homeruns"] * 4)) / char_stats["summary_at_bats"]
            ops = obp + slg

            # ops_plus = ((obp / ovr_obp) + (slg / ovr_slg) - 1) * 100

            if pa > 0:
                print(user + ", " + char + ", " + "{:.0f}".format(pa) + ", " + "{:.3f}".format(avg) + ", " + "{:.3f}".format(obp) + ", " + "{:.3f}".format(slg) + ", " + "{:.3f}".format(ops) + ", " + "{:.0f}".format(char_stats["summary_homeruns"]) + ", " + "{:.1f}".format(char_stats["summary_homeruns"]/char_stats["summary_at_bats"]*100) + ", " + "{:.0f}".format(char_stats["summary_rbi"]) + ", " + "{:.0f}".format(char_stats["summary_at_bats"]))

    data = [user, char, pa, avg, obp, slg, ops, user_summary_homeruns, user_summary_homeruns / user_summary_at_bats,
            user_summary_rbi, user_summary_at_bats]

    with open('file.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
avg = char_stats["summary_hits"] / char_stats["summary_at_bats"]
pa = char_stats["summary_at_bats"] + char_stats["summary_walks_hbp"] + char_stats["summary_walks_bb"] + char_stats["summary_sac_flys"]
obp = (char_stats["summary_hits"] + char_stats["summary_walks_hbp"] + char_stats["summary_walks_bb"]) / pa
slg = (char_stats["summary_singles"] + (char_stats["summary_doubles"] * 2) + (char_stats["summary_triples"] * 3) + ( char_stats["summary_homeruns"] * 4)) / char_stats["summary_at_bats"]
ops = obp + slg
print(user + ", Overall," + "{:.3f}".format(avg) + "," + "{:.3f}".format(obp) + "," + "{:.3f}".format(slg) + "," + "{:.1f}".format(ops))
