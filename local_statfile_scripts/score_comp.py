import json
from glob import glob


"""calculate scores and deficits via local statfiles"""
# user_input = input()
user_input = "MORI"

win = 0
loss = 0
tie = 0
ahead = 0
behind = 0
innings_played = 0
game_count = 0
game_score = {}
walkoff = 0
win_game_score = {}
loss_game_score = {}
win_down_in_first = 0
down_in_first = 0
w_down_3plus_in_first = 0
w_down_2plus_in_first = 0
w_down_3plus_in_sixth = 0
w_down_2plus_in_sixth = 0
max_lead_deficit = []
comeback = []

# open files and iterate through them
for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        try:
            with open(f_name) as json_file:
                stat_file = json.load(json_file)
                sf = stat_file

                # assign variables and bools
                innings_played += sf["Innings Played"]
                away_score = sf['Away Score']
                away_player = sf['Away Player']
                home_score = sf['Home Score']
                home_player = sf['Home Player']
                player = user_input
                player_final = 0
                opponent_final = 0
                is_win = False
                is_comeback = False
                check_for_comeback = False
                is_blown_lead = False
                check_for_blown_lead = False
                is_home_player = False
                count = 0

                # assign scores / home and away to players
                if away_player == player:
                    player_final = away_score
                    opponent_final = home_score
                    opponent = home_player

                elif home_player == player:
                    player_final = home_score
                    opponent_final = away_score
                    opponent = away_player
                    is_home_player = True

                # track wins/losses
                if player_final > opponent_final:
                    win += 1
                    is_win = True

                if player_final < opponent_final:
                    loss += 1

                # variables for event data
                player_score = 0
                opponent_score = 0
                score_dif = []
                player_dif = []
                inning = []
                game_ahead = 0
                game_behind = 0
                game_tie = 0

                # iterate through events
                for event in sf["Events"]:
                    event_num = event["Event Num"]
                    half_inning = event["Half Inning"]

                    # add score differential from each to a list
                    score_dif.append(abs(event["Home Score"] - event["Away Score"]))

                    #
                    # def inning_check():
                    #     tot = 0
                    #     inning = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    #     lead_deficit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    #     w_down_by_inning = {}
                    #     w_up_by_inning = {}
                    #     l_down_by_inning = {}
                    #     l_up_by_inning = {}
                    #     win_games = {}
                    #     lose_games = {}
                    #
                    #     for i in inning:
                    #         w_down_by_inning[i] = {}
                    #         w_up_by_inning[i] = {}
                    #         l_down_by_inning[i] = {}
                    #         l_up_by_inning[i] = {}
                    #
                    #         for j in lead_deficit:
                    #             w_down_by_inning[i][j] = 0
                    #             w_up_by_inning[i][j] = 0
                    #             l_down_by_inning[i][j] = 0
                    #             l_up_by_inning[i][j] = 0
                    #
                    #         if event["Inning"] == i:
                    #             if is_win == True:
                    #                 w_l = {}
                    #                 if player_score > opponent_score:
                    #                     if abs(w_dif) == j:
                    #                         w_up_by_inning[i][j] += 1
                    #                 if opponent_score > player_score:
                    #                     if abs(w_dif) == j:
                    #                         w_down_by_inning[i][j] += 1
                    #
                    #             if is_win == False:
                    #                 if player_score > opponent_score:
                    #                     if abs(l_dif) == j:
                    #                         l_up_by_inning[i][j] += 1
                    #                 if opponent_score > player_score:
                    #                     if abs(l_dif) == j:
                    #                         l_down_by_inning[i][j] += 1
                    #
                    #     w_l = {'upwin': w_up_by_inning, 'downwin': w_down_by_inning, 'uplose': l_up_by_inning,
                    #            'downlose': l_down_by_inning}
                    #     return w_l
                    # x = inning_check()
                    # assign home/away, and add differential to list
                    # if home, check 0 outs bottom of inning
                    ## todo - check to make sure that the deficits are being properly recorded - i think they are perhaps being read as zero due to min/max or some other weird thing
                    if is_home_player == True:
                        player_score = event["Home Score"]
                        opponent_score = event["Away Score"]
                        w_dif = player_score - opponent_score
                        l_dif = opponent_score - player_score

                        # add differential to list
                        if player_score > opponent_score:
                            if w_dif not in player_dif:
                                player_dif.append(w_dif)

                            if event["Half Inning"] == 1 and event["Outs"] == 0 and event["Inning"] not in inning:
                                ahead += 1
                                game_ahead += 1
                                count += 1
                                inning.append(event["Inning"])

                        if player_score < opponent_score:
                            if l_dif not in player_dif:
                                player_dif.append(l_dif)

                            if event["Half Inning"] == 1 and event["Outs"] == 0 and event["Inning"] not in inning:
                                behind += 1
                                game_behind += 1
                                count += 1
                                inning.append(event["Inning"])
                                if event["Inning"] == 1:
                                    if is_win == True:
                                        win_down_in_first += 1
                                        down_in_first += 1
                                        if abs(l_dif) >= 3:
                                            w_down_3plus_in_first += 1
                                        if abs(l_dif) >= 2:
                                            w_down_2plus_in_first += 1
                                    if is_win == False:
                                        down_in_first += 1
                                        # if abs(l_dif) >= 3:
                                        #     w_down_3plus_in_first += 1
                                        # if abs(l_dif) >= 2:
                                        #     w_down_2plus_in_first += 1
                                        w_down_3plus_in_sixth = 0
                                        w_down_2plus_in_sixth = 0

                        if player_score == opponent_score:
                            player_dif.append(0)

                            if event["Half Inning"] == 1 and event["Outs"] == 0 and event["Inning"] not in inning:
                                tie += 1
                                game_tie += 1
                                count += 1
                                inning.append(event["Inning"])

                        if player_score <= opponent_score and event["Event Num"] == len(sf["Events"]) - 1:
                            if player_final > opponent_final:
                                if opponent_score != player_final:
                                    # print(opponent, player_score, opponent_score, player_final, opponent_final)
                                    walkoff += 1

                    # if away, check 0 outs top of inning
                    elif is_home_player == False:
                        player_score = event["Away Score"]
                        opponent_score = event["Home Score"]
                        w_dif = player_score - opponent_score
                        l_dif = opponent_score - player_score

                        # add differential to list and add to tie/ahead/behind lists
                        if player_score > opponent_score:
                            if w_dif not in player_dif:
                                player_dif.append(w_dif)

                            if event["Half Inning"] == 1 and event["Outs"] == 0 and event["Inning"] not in inning:
                                ahead += 1
                                game_ahead += 1
                                count += 1
                                inning.append(event["Inning"])

                        if player_score < opponent_score:
                            if l_dif not in player_dif:
                                player_dif.append(l_dif)

                            if event["Half Inning"] == 1 and event["Outs"] == 0 and event["Inning"] not in inning:
                                behind += 1
                                game_behind += 1
                                count += 1
                                inning.append(event["Inning"])

                        if player_score == opponent_score:
                            if 0 not in player_dif:
                                player_dif.append(0)

                            if event["Half Inning"] == 1 and event["Outs"] == 0 and event["Inning"] not in inning:
                                tie += 1
                                game_tie += 1
                                count += 1
                                inning.append(event["Inning"])

                        # if player_score <= opponent_score and event["Event Num"] == len(sf["Events"]) - 1:
                        #     if player_final > opponent_final:
                        #         print(opponent, player_score, opponent_score, player_final, opponent_final)
                        #         walkoff += 1

                score_dif.append(abs(player_final - opponent_final))

                # add final score differential to list
                if player_final > opponent_final:
                    player_dif.append(player_final - opponent_final)

                if opponent_final > player_final:
                    player_dif.append(opponent_final - player_final)

                # calc max score differential, and max lead/deficit for given player
                max_dif = max(score_dif)
                maxleadorloss_player = (min(player_dif), max(player_dif))
                max_lead_deficit += maxleadorloss_player

                game_score[game_count] = {}
                if is_win == True:
                    game_score[game_count] = {'tie': game_tie, 'ahead': game_ahead, 'behind': game_behind, 'total': game_tie + game_ahead + game_behind, 'is_win': True, 'opponent': opponent, 'player_score': player_final, 'opponent_score': opponent_final}
                    comeback.append(maxleadorloss_player)
                if is_win == False:
                    game_score[game_count] = {'tie': game_tie, 'ahead': game_ahead, 'behind': game_behind, 'total': game_tie + game_ahead + game_behind, 'is_win': False, 'opponent': opponent, 'player_score': player_final, 'opponent_score': opponent_final}

                game_count += 1

        except json.decoder.JSONDecodeError:
            continue
try:
    inning_sum = behind + tie + ahead
    behind_ratio = round((behind / inning_sum) * 100, 1)
    tie_ratio = round((tie / inning_sum) * 100, 1)
    ahead_ratio = round((ahead / inning_sum) * 100, 1)
except ZeroDivisionError:
    pass

w_ahead = 0
w_behind = 0
w_tie = 0
w_total = 0
l_ahead = 0
l_behind = 0
l_tie = 0
l_total = 0
w_nomercy_game_score = {}
wnma = 0
wnmt = 0
wnmb = 0
wnmtot = 0

for i in game_score:
    try:
        if game_score[i]['is_win'] == True and game_score[i]['total'] > 0:
            # print(str(round((game_score[i]['behind'] / game_score[i]['total']) * 100, 1)) + "% behind / " + str(round((game_score[i]['tie'] / game_score[i]['total']) * 100, 1)) + "% tied / " + str(round((game_score[i]['ahead'] / game_score[i]['total']) * 100, 1)) + "% ahead\n")
            win_game_score[i] = {}
            win_game_score[i] = game_score[i]

            if abs(game_score[i]['opponent_score'] - game_score[i]['player_score']) < 10:
                w_nomercy_game_score[i] = {}
                w_nomercy_game_score[i] = game_score[i]


        if game_score[i]['is_win'] == False:
            # print(str(round((game_score[i]['behind'] / game_score[i]['total']) * 100, 1)) + "% behind / " + str(round((game_score[i]['tie'] / game_score[i]['total']) * 100, 1)) + "% tied / " + str(round((game_score[i]['ahead'] / game_score[i]['total']) * 100, 1)) + "% ahead\n")
            loss_game_score[i] = {}
            loss_game_score[i] = game_score[i]

    except ZeroDivisionError:
        continue

for i in win_game_score:
    try:
        w_behind += win_game_score[i]['behind']
        w_ahead += win_game_score[i]['ahead']
        w_tie += win_game_score[i]['tie']
        w_total += win_game_score[i]['total']

    except ZeroDivisionError:
        continue

for i in loss_game_score:
    try:
        l_behind += loss_game_score[i]['behind']
        l_ahead += loss_game_score[i]['ahead']
        l_tie += loss_game_score[i]['tie']
        l_total += loss_game_score[i]['total']

    except ZeroDivisionError:
        continue

for i in w_nomercy_game_score:
    try:
        wnma += w_nomercy_game_score[i]['ahead']
        wnmb += w_nomercy_game_score[i]['behind']
        wnmt += w_nomercy_game_score[i]['tie']
        wnmtot += w_nomercy_game_score[i]['total']

    except ZeroDivisionError:
        continue

# up_win = x['upwin']
# up_lose = x['uplose']
# down_win = x['downwin']
# down_lose = x['downlose']
try:
    print("Wins:")
    print(str(round((w_behind / w_total) * 100, 1)) + "% behind / " + str(round((w_tie / w_total) * 100, 1)) + "% tied / " + str(round((w_ahead / w_total) * 100, 1)) + "% ahead\n")
    print("Wins (Excluding Mercies):")
    print(str(round((wnmb / wnmtot) * 100, 1)) + "% behind / " + str(round((wnmt / wnmtot) * 100, 1)) + "% tied / " + str(round((wnma / wnmtot) * 100, 1)) + "% ahead\n")
    print("Losses:")
    print(str(round((l_behind / l_total) * 100, 1)) + "% behind / " + str(round((l_tie / l_total) * 100, 1)) + "% tied / " + str(round((l_ahead / l_total) * 100, 1)) + "% ahead\n")

    print(str(round((down_in_first / game_count) * 100, 1)) + "% of games trailing in the first inning\n")
    print(str(round((win_down_in_first / win) * 100, 1)) + "% of wins trailing in the first inning\n")
    print(str(round((w_down_2plus_in_first / win) * 100, 1)) + "% of wins trailing 2+ in the first inning\n")
    print(str(round((w_down_3plus_in_first / win) * 100, 1)) + "% of wins trailing 3+ in the first inning\n")


    print(win, "wins /", loss, "losses /", win + loss, "total games /", str(round(win / (win + loss) * 100, 1)) + "% win rate\n")
    print(walkoff, "walkoffs\n")
except ZeroDivisionError:
    pass

print(comeback)
# print(down_win)
#
# for i in game_score:
#     if game_score[i]['is_win'] == True:
#         print(str(round((game_score[i]['behind'] / game_score[i]['total']) * 100, 1)) + "% behind / " + str(round((game_score[i]['tie'] / game_score[i]['total']) * 100, 1)) + "% tied / " + str(round((game_score[i]['ahead'] / game_score[i]['total']) * 100, 1)) + "% ahead")