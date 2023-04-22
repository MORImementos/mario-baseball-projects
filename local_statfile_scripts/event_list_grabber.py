import json
from glob import glob

def return_event_values_as_list(key):
    """input a key from event data and return all recorded values associated with that key"""
    event_results = []
    for f_name in glob('*.json'):
        if f_name in glob('decoded.*'):
            with open(f_name) as json_file:
                stat_file = json.load(json_file)
                sf = stat_file
                try:
                    for event in sf["Events"]:
                        try:
                            if event[key] not in event_results:
                                event_results.append(event[key])
                        except KeyError:
                            continue
                except json.JSONDecodeError:
                    continue
    return event_results


print(return_event_values_as_list("Num Outs During Play"))