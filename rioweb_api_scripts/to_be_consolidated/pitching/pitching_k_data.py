import requests
from utils import character_aliases

"""get strikeout rate pitching data"""
# take input for character
char = input("Choose a character: ")
char_id = character_aliases.aliases[char]

# take input for username
# user = input("Choose a username: ")
user = "MORI"

# strikeout looking/swinging/bunting

strikeout_looking = 0
strikeout_swinging = 0
strikeout_bunting = 0
strikeout_ball = 0

pitch_count = 0
out_count = 0
batter_count = 0
strikeout_count = 0

url = "https://projectrio-api-1.api.projectrio.app/plate_data/?username=" \
      + f'{user}' + "&tag=Normal&tag=ranked&users_as_pitcher=1&pitcher_char=" + f'{char_id}'

# print the url just for troubleshooting
print(url)

# load the API call as json file
jsonObj = requests.get(url).json()

# iterate through each event and, depending on the data in them, add to the counters for each category mentioned above
for event in jsonObj["Data"]:

    # each event here should be a pitch
    pitch_count += 1

    # final result of 1 is a strikeout, and goal is to calc percentage of strikeouts by type of strikeout
    if event["final_result"] == 1:
        strikeout_count += 1

        # strikeout looking
        if event["pitch_result"] == 3:
            strikeout_looking += 1

        # strikeout swinging
        if event["pitch_result"] == 4:
            strikeout_swinging += 1

        # strikeout bunting
        if event["pitch_result"] == 5:
            strikeout_bunting += 1

        # "ball" pitch result, which for some reason is included in many strikeouts,
        # so it is included for statistical consistency (aligns more closely with summary stats)
        # not sure what causes it or what it means, however
        if event["pitch_result"] == 2:
            strikeout_ball += 1

    # list of all final results of event that result in an out on the play
    final_result = [1, 4, 5, 6, 13, 14, 15, 16]
    if event["final_result"] in final_result:
        out_count += 1

    # in theory, all of the final results section should be either hits or outs, so new events should indicate new batters
    if event["final_result"] != 0:
        batter_count += 1


total_count = strikeout_ball + strikeout_bunting + strikeout_looking + strikeout_swinging

k_rate = str(round((strikeout_count / batter_count)  * 100, 2)) + "%"

print(char)
print()
print(str(round((strikeout_looking / total_count) * 100, 2)) + "% Strike Looking" + " - " + str(strikeout_looking))
print(str(round((strikeout_swinging / total_count) * 100, 2)) + "% Strike Swinging" + " - " + str(strikeout_swinging))
print(str(round((strikeout_bunting / total_count) * 100, 2)) + "% Strike Bunting" + " - " + str(strikeout_bunting))
print(str(round((strikeout_ball / total_count) * 100, 2)) + "% Ball Count" + " - " + str(strikeout_ball))
print()
print(pitch_count, "Pitches Thrown")
print(out_count, "Outs Pitched")
print(total_count, "Strikeout Count")
print(batter_count, "Batters Faced")
print(k_rate, "Strikeout Rate")