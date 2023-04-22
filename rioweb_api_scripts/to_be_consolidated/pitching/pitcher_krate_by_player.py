import requests

"""get data from api and display player strikeout rate"""
stars = input("0 for stars off, 1 for stars on: ")
if stars == "0":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_batting=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked"
if stars == "1":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Superstar&exclude_batting=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked"


link = requests.get(url).json()
player_batters_faced = {}
player_k_rates = {}
pitching = link["Stats"]

for player, stats in pitching.items():
    pitching_stats = stats["Pitching"]
    strikeout_rate = pitching_stats["strikeouts_pitched"] / pitching_stats["batters_faced"]
    k_rate = round(strikeout_rate * 100, 2)
    player_k_rates[player] = k_rate
    player_batters_faced[player] = pitching_stats["batters_faced"]

k_rates = dict(sorted(player_k_rates.items(), key=lambda x: x[1], reverse=True))
sorted_player_k_rate = dict(k_rates)

for player, stats in sorted_player_k_rate.items():
    if player_batters_faced[player] > 0:
        print(player, "(" + str(player_batters_faced[player]) + " PA) /", str(stats) + "%") # strikeout rate")