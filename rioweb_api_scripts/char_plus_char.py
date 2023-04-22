import requests

"""pull stats based on games where 2 characters were on the same team"""

url = "https://projectrio-api-1.api.projectrio.app/plate_data/?users_as_batter=1&tag=normal&tag=ranked&username=MORI&batter_char=27&batter_char=38&batter_char=52&batter_char=53"
petey_list = []
bro_list = []
pull = requests.get(url).json()
stat = pull["Data"]
for game in stat:
    if game["batter_char_id"] == 27:
        if game["game_id"] not in bro_list:
            bro_list.append(game["game_id"])

    if game["batter_char_id"] == 52:
        if game["game_id"] not in bro_list:
            bro_list.append(game["game_id"])
    if game["batter_char_id"] == 53:
        if game["game_id"] not in bro_list:
            bro_list.append(game["game_id"])
    if game["batter_char_id"] == 38:
        if game["game_id"] not in bro_list:
            petey_list.append(game["game_id"])

# print(bro_list)
# print(petey_list)
# print(game_dict)
shared_list = []
for num in petey_list:
    if num in bro_list:
        if num not in shared_list:
            shared_list.append(num)

print(shared_list)

url_tag = "&games="
url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=normal&tag=ranked&username=MORI&exclude_misc=1&exclude_fielding=1&exclude_pitching=1&by_char=1"

for game in shared_list:
    url += url_tag + f'{game}'

print(url)

det_link = requests.get(url).json()

off = det_link["Stats"]

for char, stats in off.items():
    for stat in stats.values():
        if stat["summary_at_bats"] > 0 and stat["plate_appearances"] > 0:
            avg = stat["summary_hits"] / stat["summary_at_bats"]
            pa = stat["summary_at_bats"] + stat["summary_walks_hbp"] + stat["summary_walks_bb"] + stat["summary_sac_flys"]
            obp = (stat["summary_hits"] + stat["summary_walks_hbp"] + stat["summary_walks_bb"]) / pa
            slg = (stat["summary_singles"] + (stat["summary_doubles"] * 2) + (
                        stat["summary_triples"] * 3) + (stat["summary_homeruns"] * 4)) / stat[
                      "summary_at_bats"]
            ops = obp + slg

            print(char, "/ " + str(pa) + " PA / ", round(avg, 3), " / ", round(obp, 3), " / ", round(slg, 3), " / ", round(obp + slg, 3))
