#version 1.0:
#I have a 3x3 map numbered A1 to C3, with a description, a position and valid directions.
#This map is just to test the function.
#The position number goes from 0 to 8.
#The player can move according to available directions until they quit.

WIDTH = 3
STARTING_POS = 0

inventory = []
############################
#map size: 3x3, so 0 to 8 pos
#        N
#      W-+-E
#        S
############################

#the map. "desc" is the description of the place,
#"pos" is the player position in numbers,
#and "directions" is the available directions that the player can go
map = [{"desc":"You are in A1.", "pos":0, "directions":"S/E"}, 
{"desc":"You are in A2.", "pos":1, "directions":"S/E/W"},
{"desc":"You are in A3. There is a knife.", "pos":2, "directions": "S/W", "items":"Knife"},
{"desc":"You are in B1.", "pos":3, "directions": "N/S/E"},
{"desc":"You are in B2.", "pos":4, "directions": "N/S/E/W"},
{"desc":"You are in B3.", "pos":5, "directions": "N/S/W"},
{"desc":"You are in C1.", "pos":6, "directions": "N/E"},
{"desc":"You are in C2", "pos":7, "directions": "N/E/W"},
{"desc":"You are in C3", "pos":8, "directions": "N/W"},]
 
def move(pos, direction, map):
    """Takes the player position and the direction to move to (N, S, E, or W).
        Returns the new pos of the player after moving."""

    #finds the available directions for this pos
    available_directions = map[pos]["directions"]
    
    direction=direction.upper()
    
    #if the direction entered is available,
    if direction in available_directions: 
        if direction == "E":
            pos += 1
        elif direction == "W":
            pos -= 1
        elif direction == "N":
            pos -= WIDTH
        elif direction == "S":
            pos += WIDTH

        #prints the new place description
        print(map[pos]["desc"])
        print(f"You can go {available_directions}.")

    #if they enter anything else,
    else:
        print("You can't go that way >:(")

    return pos

#main loop
def game():
    """Main loop for the game"""
    
    #starting position in A1
    pos=STARTING_POS
    print(map[pos]["desc"])
    
    
    print(f"You can go S/E.")
    
    while True:

        #input for which way the player wants to go
        direction = input("Which way do you want to go? ")
        
        #move them to new position
        pos = move(pos, direction, map)

game()


