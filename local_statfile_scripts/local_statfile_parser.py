import json
from glob import glob


def specify_user():
    """specify username"""
    user = input("Enter player name: ")
    if user == "":
        user = None
    return user


def home_or_away(file, user):
    """determine home or away for each file"""
    user_home = False

    # assign player home/away
    if file["Home Player"].lower() == user.lower():
        user_home = True
    elif file["Away Player"].lower() == user.lower():
        user_home = False

    # match team id according to version
    if file["Version"] == "1.9.4":
        home_team = "1"
        away_team = "0"
    else:
        home_team = "0"
        away_team = "1"

    # return team id for user
    if user_home:
        return home_team
    elif not user_home:
        return away_team


def open_local_files():
    # get username
    user = specify_user()
    
    # open json files and organize them
    character_dict = {}
    events = {}
    
    # open files
    game_id_list = []
    for f_name in glob('*.json'):
        if f_name in glob('decoded.*'):
            with open(f_name) as json_file:
                stat_file = json.load(json_file)
                sf = stat_file
                game_id_list.append(sf["GameID"])
                
                # stars on or stars off
                stars_on = 0
                for character in sf["Character Game Stats"].values():
                    if character["Superstar"] == 1:
                        stars_on = 1
                        
                # assign user team
                if user is not None:
                    team_id = home_or_away(sf, user)

                # automate creation of variables for statfiles
                count = 0
                game_information = {}

                # overall stat file dictionary
                stat_file_dict = {}
                for key, value in sf.items():
                    stat_file_dict[key] = value

                    # create non-character, non-event stat dictionary (game info, date, etc.)
                    if count < 16:
                        game_information[key] = value
                    count += 1

                # defining variables for summary and event stats
                for character in stat_file_dict["Character Game Stats"].values():
                    char_name = character["CharID"]

                    # get selected user stats
                    # todo create stars on vs off input so that this function can filter it
                    def stars_on_off():
                        if character["Team"] == team_id:
                            if stars_on == 1:
                                if character["Superstar"] == 1:
                                    pass

                    def stat_collect(dict_for_chars, chars):
                        """iterate through characters and add them to the dictionary to compile offensive and defensive stats"""
                        if char_name not in dict_for_chars:
                            dict_for_chars[char_name] = {}
                            dict_for_chars[char_name]["Offensive Stats"] = chars["Offensive Stats"]
                            dict_for_chars[char_name]["Defensive Stats"] = chars["Defensive Stats"]
                            dict_for_chars[char_name]["Fielding Stats"] = {}
                            dict_for_chars[char_name]["Winrate Stats"] = {"Games Played": 0, "Wins": 0}
                        else:
                            def add_offensive_defensive(dict_for_chars, chars, char_name):
                                names = ["Offensive", "Defensive"]
                                for name in names:
                                    for stat in chars[f"{name} Stats"]:
                                        if stat in dict_for_chars[char_name][f"{name} Stats"]:
                                            dict_for_chars[char_name][f"{name} Stats"][stat] += chars[f"{name} Stats"][
                                                stat]
                                        else:
                                            dict_for_chars[char_name][f"{name} Stats"][stat] = chars[f"{name} Stats"][
                                                stat]

                            add_offensive_defensive(dict_for_chars, chars, char_name)

                    stat_collect(character_dict, character)
                
                # add events to dict
                events[sf["GameID"]] = stat_file_dict["Events"]

    # create a dictionary to return
    dict_for_return = {"game_info": game_information, "events": events, "character_stats": {}}

    for char in character_dict:
        dict_for_return["character_stats"][char] = {"summary_def":{}, "summary_off":{}}
        dict_for_return["character_stats"][char]["summary_def"] = character_dict[char]["Defensive Stats"]
        dict_for_return["character_stats"][char]["summary_off"] = character_dict[char]["Offensive Stats"]
        
    # return dict
    return dict_for_return




def organize_character_statdict(stat_dict):
    """organize character stats in slightly different way for easier manipulation in some scenarios"""
    char_dict = {}
    for char, stats in stat_dict["character_stats"].items():
        char_dict[char] = {"summary_off":stats["summary_off"], "summary_def":stats["summary_def"]}
    return char_dict


# x = open_local_files()
# print(organize_character_statdict(x))
# print(x.keys())
# print(x['events'].keys())
# print(x['character_stats']['Boo'])

# todo by stadium, opponent, more finely organize data into smaller categories so that accessing dict in manner like below isn't needed
# avg = x["character_stats"]["Boo"]["summary_def"]["Strikeouts"] / x["character_stats"]["Boo"]["summary_def"]["Batters Faced"]

# print(f"{str(round(avg * 100, 2))}%")

def offensive_stats(stat_dict): 
    """a start to adding stats into the auto generation as well""" 
    for char, stat in stat_dict["summary_off"].items(): 
        pa = stat["At Bats"] + stat["Walks (4 Balls)"] + stat["Walks (Hit)"] + stat["Sac Flys"] 
        avg = round(stat["Hits"] / stat["At Bats"], 3) 
        obp = round((stat["Hits"] + stat["Walks (4 Balls)"] + stat["Walks (Hit)"]) / pa, 3) 
        slg = round((stat["Singles"] + (stat["Doubles"] * 2) + (stat["Triples"] * 3) + (stat["Homeruns"] * 4)) / stat["At Bats"], 3) 
        ops = round(obp + slg, 3) 
        print(char, "(" + str(pa) + " PA)", "/", "{:.3f}".format(avg), "/", "{:.3f}".format(obp), "/", "{:.3f}".format(slg), "/", "{:.3f}".format(ops))

x = open_local_files()

print(x)
print(x.keys())
print(x["character_stats"].keys())