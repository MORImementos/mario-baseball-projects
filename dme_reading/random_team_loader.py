import memory_engine as me
import random
"""read game memory addresses and update values in real time to give random teams"""
# list of random values generated
team_1 = [random.randint(0, 53) for i in range(9)]
team_2 = [random.randint(0, 53) for i in range(9)]
hex_1 = []
hex_2 = []

for i in team_1:
    hex_1.append(i)

for i in team_2:
    hex_2.append(i)

print(hex_1, hex_2)
# randomizer script to apply values to both lists here
# inMem locations for team roster 1
team_1_roster = [
    me.DolphinByte(0x803C6726),
    me.DolphinByte(0x803C6727),
    me.DolphinByte(0x803C6728),
    me.DolphinByte(0x803C6729),
    me.DolphinByte(0x803C672A),
    me.DolphinByte(0x803C672B),
    me.DolphinByte(0x803C672C),
    me.DolphinByte(0x803C672D),
    me.DolphinByte(0x803C672E)
]
print(team_1_roster)
# inMem location for team roster 1
team_2_roster = [
    me.DolphinByte(0x803C672F),
    me.DolphinByte(0x803C6730),
    me.DolphinByte(0x803C6731),
    me.DolphinByte(0x803C6732),
    me.DolphinByte(0x803C6733),
    me.DolphinByte(0x803C6734),
    me.DolphinByte(0x803C6735),
    me.DolphinByte(0x803C6736),
    me.DolphinByte(0x803C6737),
]
print(team_2_roster)
# zeroes out team (upon random press maybe?)


# addresses for when the random button is pressed on captain select screen
first_player_r_press = me.DolphinByte(0x8033673D)
second_player_r_press = me.DolphinByte(0x8033673E)

fp_count = 0
while True:
    if team_1_roster[0].live_value == 0xFF:
        for i in team_1_roster:
            i.live_value = hex_1[fp_count]
            print(i.live_value)
            fp_count += 1
        break

sp_count = 0
while True:
    if team_2_roster[0].live_value == 0xFF:
        for i in team_2_roster:
            i.live_value = hex_2[sp_count]
            sp_count += 1
        break

# # addresses for when players press okay on the css screen
# p_1_okay = me.DolphinByte(0x803A2EC8)
# p_2_okay = me.DolphinByte(0x803A2F88)
#
# while True:
#     team_1_count = 0
#     team_2_count = 0
#     if p_1_okay == 1:
#         for i in team_1_roster:
#             i.live_value = hex_1[team_1_count]
#             team_1_count += 1
#
#         if p_1_okay != 1:
#             p_1_okay = 4
#             p_1_okay = 0
#
#         else:
#             break
#
#     elif p_1_okay == 0:
#         break
#
#     if p_2_okay == 1:
#         for i in team_2_roster:
#             i.live_value = hex_2[team_2_count]
#             team_2_count += 1
#
#         if p_2_okay != 1:
#             p_2_okay = 4
#             p_2_okay = 0
#
#         else:
#             break
#
#     elif p_2_okay == 0:
#         break
#
# if team_1 == team_1_roster and team_2 == team_2_roster:
#     pass
