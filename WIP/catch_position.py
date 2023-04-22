from glob import glob
import json
from math import sqrt

for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            stat_file = json.load(json_file)
            sf = stat_file


def PosDistance(file, position):
    character_dict = {}
    for char in file["Character Game Stats"]:
        character_dict[char] = {}
        for event in file["Events"]:
            try:
                if event["Pitch"]["Contact"]["First Fielder"]["Fielder Position"] == position and \
                        event["Runner Batter"]["Out Type"] == "Caught" and char["Superstar"] == 0:
                    ball_pos_x = (x) - event["Pitch"]["Contact"]["Ball Landing Position - X"]

                    ball_pos_y = (y) - event["Pitch"]["Contact"]["Ball Landing Position - Y"]

                    ball_pos_z = (z) - event["Pitch"]["Contact"]["Ball Landing Position - Z"]

                    ball_sum = round(sqrt((ball_pos_x ** 2) + (ball_pos_z ** 2)), 3)

                def distance(char, char_list):
                    if event["Pitch"]["Contact"]["First Fielder"]["Fielder Character"] == char:
                        char_list.append(ball_sum)
                for char in character_dict:
                    distance(char, character_dict[char]["Events"]["Distance"])
            except KeyError:
                pass

