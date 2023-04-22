import requests
import CharAliases

#detailed_stats
# def AddTags():
#     url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?"



# characters endpoint

url = "https://projectrio-api-1.api.projectrio.app/characters"

"""script for ease of access to rioweb api"""
# games parameters
# todo figure out a way to prevent adding & for the first parameter added

url = "https://projectrio-api-1.api.projectrio.app/games/?"

def UrlConstruction(num):

    endpoint = ["characters", "games", "events", "plate_data", "landing_data", "star_chances", "pitch_analysis", "detailed_stats"]

    url = "https://projectrio-api-1.api.projectrio.app/" + f'{endpoint[num]}' + "/?"

    def CharacterEndpoint():
        url = "https://projectrio-api-1.api.projectrio.app/characters"

    def GamesParameters():

        def GamesLimit():
            g_limit = int(input())
            limit_games = "&limit_games=" + f'{g_limit}'

        def GamesUser(num):
            user_parameters = ["username", "vs_username", "exclude_username"]
            user = input()
            user_select = "&" + f'{user_parameters[num]}' + "=" + f'{user}'
            print(user_select)
            # user = []
            # username = "&username =" + f'{user}'
            # vs_user = []
            # vs_username = "&vs_username =" + f'{vs_user}'
            # exclude_user = []
            # exclude_username = "&exclude_username =" + f'{exclude_user}'

        def GamesCaptain(num):
            captain_parameters = ["captain", "vs_captain", "exclude_captain"]
            cap = CharAliases.char_alias(0)
            captain_select = "&" + f'{captain_parameters[num]}' + "=" + f'{cap}'
            print(captain_select)
            # cap = CharAliases.char_alias()
            # captain = "&captain=" + f'{cap}'
            # vs_cap = CharAliases.char_alias()
            # vs_captain = "&vs_captain=" + f'{vs_cap}'
            # exclude_cap = CharAliases.char_alias()
            # exclude_captain = "&exclude_captain=" + f'{exclude_cap}'

        def GamesTags(num):
            tag_parameters = ["Superstar", "Normal", "Ranked", "Unranked", "Local", "Netplay"]
            tag = "&tag =" + f'{tag_parameters[num]}'
            print(tag)
            # stars_on = "&tag=Superstar"
            # stars_off = "&tag=Normal"
            # ranked = "&tag=Ranked"
            # unranked = "&tag=Unranked"
            # local = "&tag=Local"
            # netplay = "&tag=Netplay"

        def GamesTime(num):
            time_parameters = ["start_time", "end_time"]
            time_input = input()
            time = "&" + f'{time_parameters[num]}' + "=" + f'{time_input}'
            print(time)

        # parameters = ["limit_games", "user", "captain", "tag", "time"]
        # num = input()
        # parameter_select = parameters[int(num)]
        #
        # if parameter_select == 0:
        #     GamesUser()
        # if parameter_select == 1:
        #     GamesCaptain()
        # if parameter_select == 2:
        #     GamesTags()
        # # if parameter_select = 3:
        # #     def GamesTime(num):
    def EventsParameters():
        # not sure how to have this function be optionally called here, but I'll get to that eventually
        GamesParameters()

        def EventsLimits(num):
            e_limit = int(input())
            limit_events = "&limit_events=" + f'{e_limit}'

        def EventsChars():
            char_id = CharAliases.char_alias(1)
            events_char = ["pitcher", "batter", "fielder", "fielder_pos"]
            pitcher_char = "&" + f'{events_char[0]}' + "_char=" + char_id
            batter_char = "&" + f'{events_char[1]}' + "_char=" + char_id
            fielder_char = "&" + f'{events_char[2]}' + "_char=" + char_id
            fielder_pos = "&" + f'{events_char[3]}' + "_pos=" + char_id

        def EventsHandedness():
            handedness = int(input("0 for left, 1 for right"))
            pitcher_or_batter = int(input("0 for pitcher, 1 for batter"))
            if pitcher_or_batter == 0:
                pitcher_hand = "&pitcher_hand=" + handedness
            if pitcher_or_batter == 1:
                batter_hand = "&batter_hand=" + handedness

        def EventsPitchSwingContact():
            # pitch - not implemented yet
            contact = {"Miss": 5, "Sour - Left": 0, "Nice - Left": 1,
                       "Perfect": 2, "Nice - Right": 3, "Sour - Right": 4}
            swing = ["None", "Slap", "Star", "Charge", "Bunt"]

        def EventsChemLinks():
            chem = [0, 1, 2, 3, 4]
            chem_input = int(input())
            chem_links = "&chem_link=" + f'{chem[chem_input]}'

        def EventsInningHalfInning():
            inning_input = int(input())
            inning = "&inning=" + f'{inning_input}'
            half_inning_input = int(input())
            half_inning = "&half_inning=" + f'f{half_inning_input}'

        # def EventsStates():
        #     balls =  "&balls=" + f'{}'
        #     strikes = "&strikes=" + f'{}'
        #     outs = "&outs=" + f'{}'
        #     multi_out = "&multi_out=" + f'{}'
        #     star_chance = "&star_chance=" + f'{}'

        def EventUsersAs():
            batter_pitcher = int(input("0 for batter, 1 for pitcher"))
            if batter_pitcher == 0:
                users_as_batter = "&users_as_batter=1"
            if batter_pitcher == 1:
                users_as_pitcher = "&users_as_pitcher=1"

    def PlateData():

        url = "https://projectrio-api-1.api.projectrio.app/plate_data/"

    def LandingData():

        url = "https://projectrio-api-1.api.projectrio.app/landing_data/"

    def StarChances():

        url = "https://projectrio-api-1.api.projectrio.app/star_chances/"

    def PitchAnalysis():

        url = "https://projectrio-api-1.api.projectrio.app/pitch_analysis/"

    def DetailedStats():

        url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?"

        # def DetailedGamesUserChars():
        #
        #     game_list = []
        #     games = "&games=" + f'{game_list}'
        #     user = input()
        #     username = "&username=" + f'{user}'
        #     character = "&character=" + f'{CharAliases.char_alias(1)}'
        #
        # def DetailedByX():
        #     by_type = ["user", "char", "swing"]
        #     by_x = "by_" + 'f{}'

        def DetailedExclude():
            exclude = ["nonfair", "batting", "pitching", "misc", "fielding"]

    ## stuff happens before here to add all the parameters
    response = requests.get(url).json()











user = []
username = "&username =" + f'{user}'
game_id = []
games = "&games=" + f'{game_id}'

stars_on = "&tag=Superstar"
stars_off = "&tag=Normal"
ranked = "&tag=Ranked"
by_char = "&by_char=1"
by_user = "&by_user=1"
by_swing = "&by_swing=1"

batting_only = "&exclude_pitching=1&exclude_misc=1&exclude_fielding=1"
pitching_only = "&exclude_batting=1&exclude_misc=1&exclude_fielding=1"
misc_only = "&exclude_pitching=1&exclude_batting=1&exclude_fielding=1"
fielding_only = "&exclude_pitching=1&exclude_misc=1&exclude_batting=1"
exclude_nonfair = "&exclude_nonfair=1"