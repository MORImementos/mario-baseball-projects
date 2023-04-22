import json
from glob import glob

#### check statfiles to make sure that they are being produced correctly ####

# TODO make sure that all the looping through events happens at once if possible, not several loops
# ====INITIAL SETUP====
# for opening local file for easy testing
try:
    for f_name in glob('*.json'):
        if f_name in glob('decoded.*'):
            with open(f_name) as json_file:
                    stat_file = json.load(json_file)
                    sf = stat_file

                    # automate creation of variables for statfiles
                    stat_file_dict = {}
                    for key, value in sf.items():
                        stat_file_dict[key] = value

                    # defining variables for summary and event stats for easier access
                    summary_stats = stat_file_dict["Character Game Stats"]
                    for char in summary_stats.values():
                        summary_def = char["Defensive Stats"]
                        summary_off = char["Offensive Stats"]
                    events = stat_file_dict["Events"]

                    # place to put the summary in a central location for summary output
                    validation_summary = {}

                    # ====EVENT COUNT====
                    # make sure the events progress in order, and that they are counted correctly
                    event_count = 0
                    for event in events:
                            if event_count != event["Event Num"]:
                                print("Event Num Error:", "Event", f'{event_count}', "is incorrectly listed as Event", f'{event["Event Num"]}')
                            event_count += 1
                            if (event_count >= len(events)):
                                break

                    # ====PITCH COUNT====
                    # function to assess total pitch count and ensure that it lines up between summary and event data
                    summary_pitchers = {}
                    summary_pitch_count = 0
                    event_pitchers = {}
                    event_pitch_count = 0

                    # add char to summary stat dict and update number of pitches thrown
                    for char in summary_stats.values():
                        if char["Defensive Stats"]["Was Pitcher"] == 1:
                            summary_pitch_count += char["Defensive Stats"]["Pitches Thrown"]
                            if char["CharID"] not in summary_pitchers:
                                summary_pitchers[char["CharID"]] = char["Defensive Stats"]["Pitches Thrown"]

                        # add char to event stat dict and update number of pitches thrown
                        for event in events:
                            try:
                                if event["Pitch"]["Pitcher Char Id"] == char["CharID"]:
                                    event_pitch_count += 1

                                    if char["CharID"] not in event_pitchers:
                                        event_pitchers[char["CharID"]] = 1

                                    if char["CharID"] in event_pitchers:
                                        event_pitchers[char["CharID"]] += 1
                            except KeyError:
                                continue

                    if summary_pitch_count != event_pitch_count:
                        print("Pitch Count/Event Error: there is a discrepancy between the summary pitch count,", f'{summary_pitch_count}', "and the event pitch count,", f'{event_pitch_count}')

                    # ====STRIKEOUT COUNT====
                    # compare event and summary strikeouts and indicate any discrepancies
                    summary_pitchers = {}
                    summary_k_count = 0
                    event_pitchers = {}
                    event_k_count = 0

                    for char in summary_stats.values():
                        if char["Defensive Stats"]["Was Pitcher"] == 1:
                            summary_k_count += char["Defensive Stats"]["Strikeouts"]
                            if char["CharID"] not in summary_pitchers:
                                summary_pitchers[char["CharID"]] = char["Defensive Stats"]["Strikeouts"]
                            event_pitchers[char["CharID"]] = 0

                        for event in events:
                            try:

                                if event["Pitch"]["Pitcher Char Id"] == char["CharID"]:
                                    if event["Result of AB"] == "Strikeout":
                                        event_k_count += 1
                                        event_pitchers[char["CharID"]] += 1
                            except KeyError:
                                continue

                    if summary_k_count != event_k_count:
                        print("Strikeout Count/Event Error: there is a discrepancy between the summary strikeout count,", f'{summary_k_count}', "and the event strikeout count,", event_k_count)

                    # ==== NEXT EVENTS====
                    # create variable for next event and last event
                    last_event = events[-1]
                    if event["Event Num"] != last_event["Event Num"]:
                        next_event = events[event["Event Num"] + 1]
                    else:
                        continue

                    # ====HALF INNING TRANSITIONS====
                    # determine if the game correctly transitions between half innings when 3 outs are reached
                    try:
                        if (event["Outs"] + event["Num Outs During Play"] == 3):
                            if next_event["Half Inning"] == event["Half Inning"]:
                                print("Half Inning Error - half inning did not transition correctly between events " + str(
                                    event["Event Num"]) + " and " + str(next_event["Event Num"]))
                    except KeyError:
                        print("Error: one of Outs or Num Outs During Play returned a key error.")


                    # ====END OF GAME====
                    # standard end of game
                    if last_event["Event Num"] == event["Event Num"]:
                        # if it goes to bottom of the 9th
                        if (event["Outs"] + event["Num Outs During Play"] == 3) and event["Half Inning"] == 1 and event["Inning"] == 9:
                            pass
                        # if it ends top 9th because home team is ahead
                        if (event["Outs"] + event["Num Outs During Play"] == 3) and event["Half Inning"] == 0 and event[
                            "Inning"] == 9:
                            if sf["Home Score"] > sf["Away Score"]:
                                pass
                            # added this check because I remembered in the past the game ending early seemed to be an issue
                            else:
                                print(
                                    "Early ending error: the game file ends after the top of the 9th inning, but the home team was behind")

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
                                print(
                                    "End of Game Error: the end of the game does not meet the criteria for a standard end of game or a mercy")

# ====JSON FORMATTING====
# check to ensure there are no errors in the JSON formatting
except json.decoder.JSONDecodeError:
    print("JSON formatting error: the file returned a JSON decoding error")

# on contact, ensure that the frame given for contact is within the legal range














# return boolean, dict{problematic event:description}
