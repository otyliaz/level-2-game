#version 2.0:
#fixed the input so that it doesn't error when there is bad input
#testing:
#game()
#    You are in A1. This is the starting position.
#    You can go S/E.

#    What do you want to do? gonorth
#    I don't understand that command.

#    What do you want to do? fjsiod north
#    I don't understand that command.

#    What do you want to do? go north
#    You can't go that way...
    
#    What do you want to do? go east
#    You are in A2.
#    You can go S/E/W.

import re

WIDTH = 3
STARTING_POS = 0

inventory = []
#################################
#map size: 3x3, so 0 to 8 pos
#        N
#      W-+-E
#        S
#################################

#the map. "desc" is the description of the place,
#"pos" is the player position in numbers,
#and "directions" is the available directions that the player can go
map = [{"desc":"You are in A1. This is the starting position.", "pos":0, "directions":"S/E"}, 
{"desc":"You are in A2.", "pos":1, "directions":"S/E/W"},
{"desc":"You are in A3.", "pos":2, "directions": "S/W", "items":["KNIFE"]},
{"desc":"You are in B1.", "pos":3, "directions": "N/S/E"},
{"desc":"You are in B2.", "pos":4, "directions": "N/S/E/W"},
{"desc":"You are in B3.", "pos":5, "directions": "N/S/W"},
{"desc":"You are in C1.", "pos":6, "directions": "N/E"},
{"desc":"You are in C2", "pos":7, "directions": "N/E/W"},
{"desc":"You are in C3", "pos":8, "directions": "N/W"},]

def canmove(pos, direction):
    #finds the available directions for this pos
    available_directions = map[pos]["directions"]

    #if the direction that they entered is valid,
    if direction[0] in available_directions:
        return True
    else:
        return False

def move(pos, direction):
    """Takes the player position and the direction to move to (N, S, E, or W).
        Returns the new pos of the player after moving."""
    
    #direction=direction.upper()
    
    #if the direction entered is available,
    if canmove(pos, direction): 
        if direction == "E" or direction == "EAST":
            pos += 1
        elif direction == "W" or direction == "WEST":
            pos -= 1
        elif direction == "N" or direction == "NORTH":
            pos -= WIDTH
        elif direction == "S" or direction == "SOUTH":
            pos += WIDTH

        #prints the new place description
        print(map[pos]["desc"])

        new_directions = map[pos]["directions"]
        print(f"You can go {new_directions}.")

    #if they enter anything else,
    else:
        print("You can't go that way...")
        
    return pos
 
def cantake(pos, item):
    """checks if the item that the user entered is actually there"""
    #checks if the pos has the key "items", and that it is not null.
    if "items" in map[pos] and map[pos]["items"]:

        #checks if the item that the user entered matches the real one
        if item in map[pos]["items"]:
            return True
        else:
            return False
    
    else:
        return False   
    
def take(pos, item):
    """Take an item, and see if it is in the list of items.
    If it is there, add the item to player's inventory."""
    
    #if what they write matches the item 
    if cantake(pos, item):
        #add item to their inventory
        inventory.append(item)
            
        #remove item from pos so they can't get it again
        map[pos]["items"].remove(item)

        #shows them their inventory
        print("Your inventory: "+ ', '.join(inventory))

    else:
        print("That item does not exist, sorry")

def regex(string):
    """Check if the user's input matches the ___ ___ pattern."""
    
    #regular expression pattern
    pattern = r"[A-Za-z]+\s+[A-Za-z]+"

    #if it matches, return True. if not, return False
    if (re.match(pattern, string)):
        return True
    
    else:   
        return False  

def split_string(string):
    """Splits the user's input into two parts, e.g "go", "north", and then returns it."""

    #if the player's input is in the right format,
    if regex(string):

        #split it into two parts
        command = string.split(" ")[0]
        noun = string.split(" ")[1]

        return command, noun
    
    else: #else return false
        return False 

#main loop
def game():
    """Main loop for the game"""
    
    #starting description of the game
    pos=STARTING_POS
    print(map[pos]["desc"])
    print("You can go S/E.")
    
    while True:
        #asks player what they want to do
        user_input = input("\nWhat do you want to do? ").upper()

        if split_string(user_input) is False: 
            user_input = print("I don't understand that command.")
            continue
        else:
            #splits input in half
            command, noun = split_string(user_input) 
        
        #if they want to go somewhere..
        if command == "GO":
            
            #direction is the second part of the input
            direction = noun
            #move them to new position
            pos = move(pos, direction)
            
            #if the key "items" exists for the new pos, and it is not empty,
            #print the items
            if "items" in map[pos] and map[pos]["items"]:
                print("There is: " + ', '.join(map[pos]["items"]))
    
        #if they want to take/pick up something
        elif command == "TAKE":

            #item is the second part of the input
            item = noun
            #takes item
            take(pos, item)

        #if they type something different
        else:
            print("I don't understand that command.")
