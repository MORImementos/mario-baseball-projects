import requests

"""measure various stats vs the broader player average"""

print("Enter name of character (blank for all stats):")
char = input()
print("Enter '0' for stars-off data; '1' for stars-on")
stars = int(input())
print("Enter '0' for all data, '1' for ranked only")
ranked = int(input())

url = "https://projectrio-api-1.api.projectrio.app/detailed_stats/?exclude_pitching=1&exclude_fielding=1&exclude_misc=1"
if stars == 0:
    url += "&tag=Normal"
elif stars == 1:
    url += "&tag=Superstar"
if ranked == 1:
    url += "&tag=Ranked"

if char != "":
    url += "&by_char=1"

total_response = requests.get(url).json()
print(url)

url += "&by_user=1"

user_response = requests.get(url).json()

user_dict = {}

overall = {}
if char == "":
    overall = total_response["Stats"]["Batting"]
else:
    overall = total_response["Stats"][char]["Batting"]
overall_avg = overall["summary_hits"] / overall["summary_at_bats"]
overall_pa = overall["summary_at_bats"] + overall["summary_walks_bb"] + overall["summary_walks_hbp"] + overall[ "summary_sac_flys"]
overall_obp = (overall["summary_hits"] + overall["summary_walks_hbp"] + overall["summary_walks_bb"]) / overall_pa
overall_slg = (overall["summary_singles"] + (overall["summary_doubles"] * 2) + (overall["summary_triples"] * 3) + (overall["summary_homeruns"] * 4)) / overall["summary_at_bats"]

def v_average(user, overall):
    difference = round(user - overall,3)
    if difference > 0:
        return difference
    if difference < 0:
        return difference

for user in user_response["Stats"]:
    # todo
    stats = {}
    if char == "":
        stats = user_response["Stats"][user]["Batting"]
    elif char in user_response["Stats"][user]:
        stats = user_response["Stats"][user][char]["Batting"]
    else:
        pass
    if "plate_appearances" in stats and "summary_at_bats" in stats:
        if stats["summary_at_bats"] > 0:
            pa = stats["summary_at_bats"] + stats["summary_walks_bb"] + stats["summary_walks_hbp"] + stats["summary_sac_flys"]
            vs_avg = stats["summary_hits"] / stats["summary_at_bats"]
            vs_obp = (stats["summary_hits"] + stats["summary_walks_hbp"] + stats["summary_walks_bb"]) / pa
            vs_slg = (stats["summary_singles"] + (stats["summary_doubles"] * 2) + (stats["summary_triples"] * 3) + (stats["summary_homeruns"] * 4)) / stats["summary_at_bats"]
            vs_ops = vs_obp + vs_slg
            vs_pa = stats["plate_appearances"]
            ops_plus = ((vs_obp / overall_obp) + (vs_slg / overall_slg) - 1) * 100
            avg_dif = v_average(vs_avg, overall_avg)
            obp_dif = v_average(vs_obp, overall_obp)
            slg_dif = v_average(vs_slg, overall_slg)
            cum_dif = obp_dif + slg_dif
            user_dict[user] = (vs_pa, vs_avg, vs_obp, vs_slg, vs_ops, ops_plus, avg_dif, obp_dif, slg_dif, cum_dif)

sorted_user_list = sorted(user_dict.keys(), key=lambda x: user_dict[x][9], reverse=True)

print("OBP / SLG") # OPS")"AVG /
print("ALL (" + str(overall["plate_appearances"]) + " PA): " + "{:.3f}".format(overall_obp) + " / " + "{:.3f}".format(overall_slg), "\n") #+ "{:.3f}".format(overall_avg) + " / "  + " / " + "{:.3f}".format(overall_obp + overall_slg))

for user in sorted_user_list:
    pa = user_dict[user][0]
    avg = user_dict[user][1]
    obp = user_dict[user][2]
    slg = user_dict[user][3]
    ops = user_dict[user][4]
    ops_plus = user_dict[user][5]
    avg_dif = user_dict[user][6]
    obp_dif = user_dict[user][7]
    slg_dif = user_dict[user][8]
    cum_dif = user_dict[user][9]
    c_o = " cOPS+"
    if char == "":
        c_o = " OPS+"
    avg_dif = v_average(avg, overall_avg)
    obp_dif = v_average(obp, overall_obp)
    slg_dif = v_average(slg, overall_slg)
    cum_dif = obp_dif + slg_dif
    if obp_dif > 0:
        obp_dif = "+" + str(obp_dif)
    if slg_dif > 0:
        slg_dif = "+" + str(slg_dif)
    if pa > 50:
        print(user, "\n", obp_dif, "\n", slg_dif, "\n") # , " | ", str(round(ops_plus)) + c_o)
