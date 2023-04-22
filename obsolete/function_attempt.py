"""unsure of what this was supposed to be, it is very old I think"""

class RioValidation:
    def __init__(self, general_stats, summary_stats, event_stats):
        self.general_stats = general_stats
        self.summary_stats = summary_stats
        self.event_stats = event_stats
    def function(self):
        pass


















    # for char in dictionary.values():
    #     function












    # def stat_comparison(dict1, dict2):
    #     if char["Defensive Stats"]["Was Pitcher"] == 1:
    #         summary_stat_count += char["Defensive Stats"]["Pitches Thrown"]
    #         if char["CharID"] not in summary_stat:
    #             summary_stat[char["CharID"]] = char["Defensive Stats"]["Pitches Thrown"]
    #
    #     # add char to event stat dict and update number of pitches thrown
    #     for event in events:
    #
    #         if event["Pitch"]["Pitcher Char Id"] == char["CharID"]:
    #             event_stat_count += 1
    #
    #             if char["CharID"] not in event_stat:
    #                 event_stat[char["CharID"]] = 1
    #
    #             if char["CharID"] in event_stat:
    #                 event_stat[char["CharID"]] += 1
    #
    # if summary_stat_count != len(events):
    #     print("Pitch Count/Event Error: there is a discrepancy between the summary pitch count,",
    #           f'{summary_stat_count}', "and the event pitch count,", f'{len(events)}')
