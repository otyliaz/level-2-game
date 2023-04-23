#version 2.0:
#--made it print inventory when they type inv, prints this:
#What do you want to do? inv
#Your inventory: KNIFE

#--made it give some help when they type help; prints this:
#What do you want to do? help

#    Type "go [direction]" to go a direction.
#    Type "take" [item] to pick up an item.
#    Type "inv" to show your inventory.
#    Type "exit" to quit the game.

#checklist:
    
#make a thing like u can only go somewhere if u have something:
## "you can't go there, you need _____!"
#if pos is <=8, can't go to >8. if pos is >8, can go back.
#exit command

#make the map 💀

import re

WIDTH = 3
STARTING_POS = 0

inventory = []
#################################
#TEST map size: 4x3, so 0 to 11 pos
#        N
#      W-+-E
#        S
#################################

#the map. "desc" is the description of the place,
#"pos" is the player position in numbers,
#"directions" is the available directions that the player can go
#"items" is the items that are in the pos
#"req" is the requirements to enter this square
map = [{"desc":"You are in A1. This is the starting position.", "pos":0, "directions":"S/E"}, 
{"desc":"You are in A2.", "pos":1, "directions":"S/E/W"},
{"desc":"You are in A3.", "pos":2, "directions": "S/W", "items":["KNIFE"]},
{"desc":"You are in B1.", "pos":3, "directions": "N/S/E", "items":["ROPE"]},
{"desc":"You are in B2.", "pos":4, "directions": "N/S/E/W"},
{"desc":"You are in B3.", "pos":5, "directions": "N/S/W"},
{"desc":"You are in C1.", "pos":6, "directions": "N/E"},
{"desc":"You are in C2", "pos":7, "directions": "N/E/W"},
{"desc":"You are in C3", "pos":8, "directions": "N/W"},
{"desc":"You are in D1, only allowed if you have 'rope'", "pos":9, "directions": "N/E", "req":"ROPE"},
{"desc":"You are in D2, only allowed if you have 'rope'", "pos":10, "directions": "N/E/W", "req":"ROPE"},
{"desc":"You are in D3, only allowed if you have 'rope'", "pos":11, "directions": "N/W", "req":"ROPE"},]

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

        
        #if the key "items" exists for the new pos, and it is not empty,
        #print the items
        if "items" in map[pos] and map[pos]["items"]:
            print("There is: " + ', '.join(map[pos]["items"]))

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
    """Check if the user's input matches the ___ ___ pattern.
    If it does, return True; if it doesn't, return False"""
    
    #regular expression pattern
    pattern = r"[A-Za-z]+\s+[A-Za-z]+"

    #if it matches, return True. if not, return False
    if re.match(pattern, string):
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

#-------help commands-------------------

        #if they type "inv", print their inventory
        if user_input == "INV": 
            print("Your inventory: "+ ', '.join(inventory))
            continue

        if user_input == "EXIT":
            break

        #if they type "help", print some help 
        if user_input == "HELP":
            print("""
    Type "go [direction]" to go a direction.
    Type "take" [item] to pick up an item.
    Type "inv" to show your inventory.
    Type "exit" to quit the game.""")
            continue

#--------------------------------------

        #if the string can't be split in 2, ask again.
        if split_string(user_input) is False: 
            user_input = print("I don't understand that command.")
            continue
        else:
            #splits input in half
            command, noun = split_string(user_input) 
        
        #if they want to go somewhere..
        if command == "GO":
            
            #direction is the second part of the input, i.e north
            direction = noun
            #move them to new position
            pos = move(pos, direction)
    
        #if they want to take/pick up something
        elif command == "TAKE":

            #item is the second part of the input
            item = noun
            #takes item
            take(pos, item)

        #if they type something different
        else:
            print("I don't understand that command.")
