import requests

"""get stats by hit type (in this case, slap hits)"""
url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_char=1&tag=ranked&by_swing=1"
link = requests.get(url).json()

slap = {}
char_total = {}
plate_appearances = {}
bat = link["Stats"]

for char, stats in bat.items():
    batting_stats = stats["Batting"]
    # slap_ab += batting_stats["Slap"]["plate_appearances"]
    avg = (batting_stats["Slap"]["singles"] + batting_stats["Slap"]["doubles"] + batting_stats["Slap"]["triples"] + batting_stats["Slap"]["homeruns"]) / batting_stats["Slap"]["plate_appearances"]
    if batting_stats["Slap"]["plate_appearances"] > 150:
        slap[char] = round(avg,3)

slap_dict = dict(sorted(slap.items(), key=lambda x: x[1], reverse=True))
sorted_slap = dict(slap_dict)

for char, stat in sorted_slap.items():
    char_total[char] = str(stat) + " slap hit avg / "
print("\n")
url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_char=1&tag=ranked"
link = requests.get(url).json()

bat = link["Stats"]
strikeout_rate = {}

for char, stats in bat.items():
    batting_stats = stats["Batting"]
    k_rate = batting_stats["summary_strikeouts"] / batting_stats["summary_at_bats"]
    plate_appearances[char] = "(" + str(batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"]) + " PA)"
    if batting_stats["summary_at_bats"] > 200:
        strikeout_rate[char] = round(k_rate*100,2)

k_dict = dict(sorted(strikeout_rate.items(), key=lambda x: x[1], reverse=False))
sorted_strikeouts = dict(k_dict)



for char, stat in sorted_strikeouts.items():
    if char in char_total:
        char_total[char] += str(stat) + "% strikeout rate"
    else:
        continue

for char, stat in char_total.items():
    print(char, plate_appearances[char], "/", stat)