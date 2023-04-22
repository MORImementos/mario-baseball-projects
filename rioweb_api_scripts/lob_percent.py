import requests

"""look up user stats on RioWeb and determine the left on base % of each user"""
url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?exclude_pitching=1&exclude_fielding=1&exclude_misc=1&tag=ranked&tag=normal&by_user=1"

response = requests.get(url).json()
stats = response["Stats"]
stat_dict = {}

# pull user information
for user, stats in stats.items():

    pitch = stats["Batting"]
    lob = (pitch["summary_hits"] + pitch["summary_walks_hbp"] + pitch["summary_walks_bb"] - pitch["summary_rbi"]) / (
                pitch["summary_hits"] + pitch["summary_walks_hbp"] + pitch["summary_walks_bb"] - (
                    pitch["summary_homeruns"] * 1.4))
    if pitch["summary_at_bats"] > 500:
        # print(user, "/", str(round(lob * 100, 1)) + "%")
        stat_dict[user] = {}
        stat_dict[user] = str(round(lob * 100, 1)) + "%"

url2 = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?exclude_pitching=1&exclude_fielding=1&exclude_misc=1&tag=ranked&tag=normal"

# pull overall information
response = requests.get(url2).json()
stats = response["Stats"]["Batting"]

pitch = stats
sum_lob = (pitch["summary_hits"] + pitch["summary_walks_hbp"] + pitch["summary_walks_bb"] - pitch["summary_rbi"]) / (
            pitch["summary_hits"] + pitch["summary_walks_hbp"] + pitch["summary_walks_bb"] - (
                pitch["summary_homeruns"] * 1.4))
print("Summary", "/", str(round(sum_lob * 100, 1)) + "%\n")

# sort dict and print in ascending order
stat_dict = dict(sorted(stat_dict.items(), key=lambda item: item[1]))
for k, v in stat_dict.items():
    print(k, v)