import requests
"""player strikeout rate batting"""
stars = input("0 for stars off, 1 for stars on: ")
if stars == "0":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked"
if stars == "1":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Superstar&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked"
link = requests.get(url).json()
player_plate_appearances = {}
player_k_rates = {}
batting = link["Stats"]

for player, stats in batting.items():
    batting_stats = stats["Batting"]
    pa = batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"]
    strikeout_rate = batting_stats["summary_strikeouts"] / (batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"])
    k_rate = round(strikeout_rate * 100, 2)
    player_k_rates[player] = k_rate
    player_plate_appearances[player] = pa

k_rates = dict(sorted(player_k_rates.items(), key=lambda x: x[1], reverse=False))
sorted_player_k_rate = dict(k_rates)

for player, stats in sorted_player_k_rate.items():
    if player_plate_appearances[player] > 500:
        print(player, "(" + str(player_plate_appearances[player]) + " PA) /", str(stats) + "% strikeout rate")

url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&tag=ranked"
link = requests.get(url).json()
batting = link["Stats"]
batting_stats = batting["Batting"]
pa = batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"]
strikeout_rate = batting_stats["summary_strikeouts"] / (batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"])
print("\n", "Overall:", str(round(strikeout_rate * 100,3)) + "%")