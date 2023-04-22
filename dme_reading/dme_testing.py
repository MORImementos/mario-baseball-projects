import warnings
import memory_engine as me

"""test script, used to modify / read memory addresses of game in real-time"""
warnings.filterwarnings('ignore', '.*The NumPy module was reloaded*')

def print_live_update(*args):
    variables = []
    for i in args:
        variables.append(i)

    last_values = []
    while True:
        if len(last_values) == 0:
            last_values = [x.live_value for x in variables]

        for i in range(len(variables)):
            if variables[i].live_value != last_values[i]:
                print(f"{hex(variables[i].address)}: {variables[i].live_value}")

        last_values = [x.live_value for x in variables]



game_variable = me.DolphinFloat(0x80890954)
team_vars = [me.DolphinByte(0x803C6726), me.DolphinByte(0x803C6727), me.DolphinByte(0x803C6728), me.DolphinByte(0x803C6729),
             me.DolphinByte(0x803C672A), me.DolphinByte(0x803C672B), me.DolphinByte(0x803C672C), me.DolphinByte(0x803C672D),
             me.DolphinByte(0x803C672E)]
for i in team_vars:
    i.live_value = 0xFF
current_value = game_variable.live_value  # retrieves the value from the game
print(current_value)
game_variable.live_value = 5.0  # sets the value in the game

# try to write a program that opens, writes to memory, and closes itself