import json
from glob import glob

# user_input = input()
user_input = "MORI"

win = 0
loss = 0
tie = 0
ahead = 0
behind = 0
innings_played = 0

# open files and iterate through them
for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            stat_file = json.load(json_file)
            sf = stat_file

            innings_played += sf["Innings Played"]
            # print(innings_played, sf["Innings Played"])
            away_score = sf['Away Score']
            away_player = sf['Away Player']
            home_score = sf['Home Score']
            home_player = sf['Home Player']
            player = user_input
            player_final = None
            opponent_final = None
            player_score = None
            opponent_score = None
            is_win = False
            count = 0

            # assign scores to players
            if away_player == player:
                player_final = away_score
                opponent_final = home_score

            elif home_player == player:
                player_final = home_score
                opponent_final = away_score

            else:
                continue

            # track wins/losses
            if player_final > opponent_final:
                win += 1
                is_win = True

            if player_final < opponent_final:
                loss += 1

            else:
                continue

            # iterate through events
            for event in sf["Events"]:
                event_num = event["Event Num"]
                # inning = event["Inning"]
                half_inning = event["Half Inning"]
                out = 0
                inning = 0

                # assign scores to players
                if away_player == player:
                    player_score = event["Away Score"]
                    opponent_score = event["Home Score"]

                elif home_player == player:
                    player_score = event["Home Score"]
                    opponent_score = event["Away Score"]

                else:
                    continue

                # if event["Inning"] == inning:
                #     continue
                #
                # elif event["Inning"] != inning:
                #     inning = event["Inning"]
                if event["Outs"] + event["Num Outs During Play"] == 3 and event["Half Inning"] == 1: # == 0 and event["Num Outs During Play"] == 3) or (event["Outs"] == 1 and event["Num Outs During Play"] == 2) or (event["Outs"] == 2 and event["Num Outs During Play"] == 1):
                    # print(event["Inning"], event["Half Inning"], event["Outs"] + event["Num Outs During Play"], player_score, opponent_score)
                    try:
                        start_of_next_inning = sf["Events"][event["Event Num"] + 1]
                        print(event["Inning"], start_of_next_inning["Inning"])
                        if start_of_next_inning["Inning"] == (event["Inning"] + 1):
                            if away_player == player:
                                player_score = start_of_next_inning["Away Score"]
                                opponent_score = start_of_next_inning["Home Score"]
                                if player_score == opponent_score:
                                    tie += 1
                                    count += 1

                                if player_score < opponent_score:
                                    behind += 1
                                    count += 1

                                if player_score > opponent_score:
                                    ahead += 1
                                    count += 1



                            elif home_player == player:
                                player_score = start_of_next_inning["Home Score"]
                                opponent_score = start_of_next_inning["Away Score"]
                                if player_score == opponent_score:
                                    tie += 1
                                    count += 1

                                if player_score < opponent_score:
                                    behind += 1
                                    count += 1

                                if player_score > opponent_score:
                                    ahead += 1
                                    count += 1



                        # print(start_of_next_inning)
                    except IndexError:

                        # final_event_of_game = event
                        continue
                        # print(final_event_of_game["Home Score"], final_event_of_game["Away Score"], final_event_of_game["Outs"], final_event_of_game["Inning"], sf["Innings Selected"])




                else:
                    continue
            print(tie, behind, ahead, innings_played, home_player, away_player)
            if count != sf["Innings Played"]:
                print("error", count, sf["Innings Played"])


print(tie, behind, ahead, win, loss)
print(tie + behind + ahead, innings_played)
