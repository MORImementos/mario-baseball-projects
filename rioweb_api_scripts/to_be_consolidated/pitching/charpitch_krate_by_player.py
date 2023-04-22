import requests

"""character pitching strikeout rate by player"""
stars = input("0 for stars off, 1 for stars on: ")
if stars == "0":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_batting=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked&by_char=1"
if stars == "1":
    url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Superstar&exclude_batting=1&exclude_misc=1&exclude_fielding=1&by_user=1&tag=ranked&by_char=1"

link = requests.get(url).json()
character_batters_faced = {}
character_k_rates = {}
users_dict = {}

pitching = link["Stats"]

for player, statistics in pitching.items():
    users_dict[player] = {}
    character_k_rates[player] = {}
    character_batters_faced[player] = {}
    for character, stats in statistics.items():
        pitching_stats = stats["Pitching"]
        bf = pitching_stats["batters_faced"]
        if bf > 0:
            character_batters_faced[player][character] = bf
            character_k_rates[player][character] = pitching_stats["strikeouts_pitched"]
            strikeout_rate = pitching_stats["strikeouts_pitched"] / (bf)
            k_rate = round(strikeout_rate * 100, 3)
            users_dict[player][character] = k_rate

for user in users_dict:
    for name, stat in users_dict[user].items():
        print(user, "/", name, "/", character_batters_faced[user][name], "/", str(stat) + "% /", character_k_rates[user][name])