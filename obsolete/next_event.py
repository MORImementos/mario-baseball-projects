from glob import glob
import json

"""function that ultimately became part of the statfile validation script"""
def next_events(file, events)   :
    # ==== NEXT EVENTS====
    # create variable for next event and last event
    last_event = events[-1]
    for event in events:
        if event["Event Num"] != last_event["Event Num"]:
            next_event = events[event["Event Num"] + 1]

        # ====HALF INNING TRANSITIONS====
        # determine if the game correctly transitions between half innings when 3 outs are reached
        try:
            if (event["Outs"] + event["Num Outs During Play"] == 3):
                if next_event["Half Inning"] == event["Half Inning"]:
                    print("Half Inning Error - half inning did not transition correctly between events " + str(event["Event Num"]) + " and " + str(next_event["Event Num"]))
        except KeyError:
            continue

        # ====END OF GAME====
        # standard end of game
        if last_event["Event Num"] == event["Event Num"]:
            # if it goes to bottom of the 9th
            try:
                if (event["Outs"] + event["Num Outs During Play"] == 3) and event["Half Inning"] == 1 and event["Inning"] == 9:
                    pass
                # if it ends top 9th because home team is ahead
                if (event["Outs"] + event["Num Outs During Play"] == 3) and event["Half Inning"] == 0 and event["Inning"] == 9:
                    if file["Home Score"] > file["Away Score"]:
                        pass
                    else:
                        print("Early ending error: the game file ends after the top of the 9th inning, but the home team was behind")

                # check if game ended via mercy
                elif event["Inning"] != 9 and event["Half Inning"] == 1:
                    runs = 0

                if "Runner Batter" in event:
                    if event["Runner Batter"].get("Runner Result Base", None) == 4:
                        runs += 1
                if "Runner 1B" in event:
                    if event["Runner 1B"].get("Runner Result Base", None) == 4:
                        runs += 1
                if "Runner 2B" in event:
                    if event["Runner 2B"].get("Runner Result Base", None) == 4:
                        runs += 1
                if "Runner 3B" in event:
                    if event["Runner 3B"].get("Runner Result Base", None) == 4:
                        runs += 1
                if (event["Home Score"] + runs) - event["Away Score"] >= 10:
                    pass

                # otherwise give error because it ended abnormally
                if ((event["Home Score"] + runs) - event["Away Score"]) < 10:
                    print("End of Game Error: the end of the game does not meet the criteria for a standard end of game or a mercy")
            except KeyError:
                continue


for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            sf = json.load(json_file)
            next_events(sf, sf["Events"])