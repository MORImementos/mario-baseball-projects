from glob import glob
import json

summary = {}
"""calculate runs per play (RBIs don't always include total runs so baserunners must be added in)"""

def calc_runs(events, game_id):
    tot_runs = 0
    runs_per_event = {}
    for event in events:
        event_runs = 0



        if "Runner Batter" in event:
            if event["Runner Batter"].get("Runner Result Base", None) == 4:
                event_runs += 1
                tot_runs += 1
        if "Runner 1B" in event:
            if event["Runner 1B"].get("Runner Result Base", None) == 4:
                event_runs += 1
                tot_runs += 1
        if "Runner 2B" in event:
            if event["Runner 2B"].get("Runner Result Base", None) == 4:
                event_runs += 1
                tot_runs += 1
        if "Runner 3B" in event:
            if event["Runner 3B"].get("Runner Result Base", None) == 4:
                event_runs += 1
                tot_runs += 1
        if event["Event Num"] not in runs_per_event.keys():
            runs_per_event[event["Event Num"]] = event_runs
        else:
            runs_per_event[event["Event Num"]] += event_runs
        summary[game_id] = {"per_event": runs_per_event, "total": tot_runs}
        print(runs_per_event)
        print(tot_runs)
    return summary

for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            stat_file = json.load(json_file)
            sf = stat_file
            x = calc_runs(sf["Events"], sf["GameID"])
            print(x)
