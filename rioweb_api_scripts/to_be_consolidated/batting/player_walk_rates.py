import requests

"""calc player walk rates from api"""
url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked"
link = requests.get(url).json()
player_plate_appearances = {}
player_w_rates = {}
batting = link["Stats"]

for player, stats in batting.items():
    batting_stats = stats["Batting"]
    pa = batting_stats["summary_at_bats"] + batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"] + batting_stats["summary_sac_flys"]
    walk_rate = (batting_stats["summary_walks_bb"] + batting_stats["summary_walks_hbp"]) / pa
    w_rate = round(walk_rate * 100, 2)
    player_w_rates[player] = w_rate
    player_plate_appearances[player] = pa

w_rates = dict(sorted(player_w_rates.items(), key=lambda x: x[1], reverse=True))
sorted_player_w_rate = dict(w_rates)

for player, stats in sorted_player_w_rate.items():
    if player_plate_appearances[player] > 500:
        print(player, "(" + str(player_plate_appearances[player]) + " PA) /", str(stats) + "% walk rate")