import requests

"""get character strikeout rate by player"""

stars = input("0 for stars off, 1 for stars on: ")
if stars == "0":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked&by_char=1"
if stars == "1":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Superstar&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked&by_char=1"

link = requests.get(url).json()
character_plate_appearances = {}
character_k_rates = {}
users_dict = {}

batting = link["Stats"]

for player, statistics in batting.items():
    users_dict[player] = {}
    character_k_rates[player] = {}
    character_plate_appearances[player] = {}
    for character, stats in statistics.items():
        batting_stats = stats["Batting"]
        pa = batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"]
        if pa > 0:
            character_plate_appearances[player][character] = pa
            character_k_rates[player][character] = batting_stats["summary_strikeouts"]
            strikeout_rate = batting_stats["summary_strikeouts"] / (batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"])
            k_rate = round(strikeout_rate * 100, 3)
            users_dict[player][character] = k_rate



for user in users_dict:
    for name, stat in users_dict[user].items():
        print(user, "/", name, "/", character_plate_appearances[user][name], "/", str(stat) + "% /", character_k_rates[user][name])
# dict_by_char = {}
# for players, characters in users_dict.items():
#     for name, values in characters.items():
#         try:
#             dict_by_char[name][players] = values
#
#         except KeyError:
#             continue
# print(dict_by_char)