import requests
from utils.make_percentage import percentage, add_percent_sign
"""calculate how unlucky a player is compared to average"""
misc_url = 'https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_batting=1&exclude_fielding=1&by_swing=1&tag=ranked&by_user=1'
fielding_url = 'https://projectrio-api-1.api.projectrio.app/detailed_stats/?tag=Normal&exclude_pitching=1&exclude_batting=1&exclude_misc=1&by_swing=1&tag=ranked&by_user=1'

# get url links for users
misc_response = requests.get(misc_url).json()
misc_stats = misc_response["Stats"]
misc_users = {}

fielding_response = requests.get(fielding_url).json()
fielding_stats = fielding_response["Stats"]
fielding_users = {}

for user in misc_stats:
    misc_users[user] = {}
    misc_users[user] = misc_stats[user]['Misc']

for user in fielding_stats:
    fielding_users[user] = {}
    fielding_users[user] = fielding_stats[user]["Fielding"]

unlucko = {}
bobbles = {}
for k, v in fielding_users.items():
    bobble = v['bobbles']
    bobbles[k] = v['bobbles']

star_chances = {}
for k, v in misc_users.items():
    def_star = v['defensive_star_chances']
    def_star_won = v['defensive_star_chances_won']
    off_star = v['offensive_star_chances']
    off_star_won = v['offensive_star_chances_won']
    star_chances[k] = [def_star, def_star_won, off_star, off_star_won]

ds = [bobbles, star_chances]
for k in bobbles.keys():
  unlucko[k] = tuple(unlucko[k] for unlucko in ds)

# print rate of defensive star chances to total
for k, v in unlucko.items():
    print(k, add_percent_sign(percentage(v[1][0] / (v[1][0] + v[1][2]))), "Defensive Star Chance Rate")
    print()

