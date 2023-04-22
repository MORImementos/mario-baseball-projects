"""fill lists. I could have the output be more generic, but for now it has worked since it has mainly been related to the game."""

# empty lists to fill
char_input = []
player_input= []

# get character names and add to list. type and press enter. leave blank and press enter to move to players
print("Character names")
while True:

	char = input()
	if char == "":
		break
	char_input.append(char)

	

# works identically to the former
print("Player names") 

while True:

	player = input()
	if player == "":
		break
	player_input.append(player)

	
# just here to show inputs/be sure it works	
print(char_input)
print(player_input)

# after getting the lists, loop through whatever needs ro be looped through however it needs to be

# for char in char_input:
	# do stuff

# for player in player_input:
	# do stuff
