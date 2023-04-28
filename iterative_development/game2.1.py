#version 2.0:
#-made it print inventory when they type inv:
#What do you want to do? inv
#Your inventory: KNIFE

#-made it print help when they type help; like this:
#What do you want to do? help

#    Type "go [direction]" to go a direction.
#    Type "inv" to show your inventory.
#    Type "take [item] to pick up an item.

# I have a map now, descriptions aren't finished yet

import re

WIDTH = 10
STARTING_POS = 27

inventory = []
#################################
#map size: 6x10, so 0 to 59 pos
#        N      |----10---------|
#      W-+-E    |               |
#        S      8               8
#               |               |
#               |-----10--------|
#################################

#the map. "desc" is the description of the place,
#"pos" is the player position in numbers,
#"directions" is the available directions that the player can go
#"items" is the items that are in the pos
#"req" is the requirements to enter this square
map = [{"desc":"A1. Your high-school is to the south-east. The city wall surrounds you from the north and west.", "pos":0, "directions":"S/E"}, 
{"desc":"A2. The back wall of your high-school is directly south of you. The city wall surrounds you from the north.", "pos":1, "directions":"E/W"},
{"desc":"A3. The back wall of your high-school is directly south of you. The city wall surrounds you from the north.", "pos":2, "directions": "E/W"},
{"desc":"A4. The back wall of your high-school is directly south of you. The city wall surrounds you from the north.", "pos":3, "directions": "E/W"},
{"desc":"A5. Your high-school is to the south-west of you. The city wall surrounds you from the north. Directly to the west of you is a busy road... those zombies are ruthless. Try not to get hit.", "pos":4, "directions": "S/E/W"},
{"desc":"A6. You're in the middle road. Hurry, before you get ran over.", "pos":5, "directions": "S/E/W"},
{"desc":"A7. You see your house to the south. The city wall surrounds you from the north. Directly to the east of you is a busy road...", "pos":6, "directions": "S/E/W"},
{"desc":"A8. You see your house to the south. The city wall surrounds you from the north.", "pos":7, "directions": "S/E/W"},
{"desc":"A9. You see your backyard to the south. The city wall surrounds you from the north.", "pos":8, "directions": "S/E/W"},
{"desc":"A10. You see your backyard to the south-west. The city wall surrounds you from the north and the east", "pos":9, "directions": "S/W"},

{"desc":"B1. The city wall surrounds you from the west. The wall of your high-school is directy to the east of you. Through the window you can see that the room is infested with zombies.", "pos":10, "directions": "N/S"},
{"desc":"B2. You feel the hands of a zombie on your body. DEATH SCENE", "pos":11, "directions": "N/S/E/W"},
{"desc":"B3. You made it another step, but you can still feel zombies surrounding you. Just get to the stairs.", "pos":12, "directions": "S/E/W"},
{"desc":"B4. You made it.  *WIN SCENE* you run up the stairs, and get saved", "pos":13, "directions": " "},
{"desc":"B5. The wall of your high-school is directly to the west of you. Directly east, there is a busy road.", "pos":14, "directions": "N/S/E/W"},
{"desc":"B6. You're in the middle road.", "pos":15, "directions": "N/S/E/W"},
{"desc":"B7. road to your east, your house south of you.", "pos":16, "directions": "N/E/W"},
{"desc":"B8. house south of you", "pos":17, "directions": "N/E/W"},
{"desc":"B9. your backyard south of you", "pos":18, "directions": "N/S/E/W"},
{"desc":"B10. city wall to your east", "pos":19, "directions": "N/S/W"},

{"desc":"C1. school to your east, wall to your west", "pos":20, "directions": "N/S",},
{"desc":"C2. zombies. you die.", "pos":21, "directions": "N/E"},
{"desc":"C3. you have entered the school. its dark as", "pos":22, "directions": "N/S/E/W"},
{"desc":"C4. zombies. you die.", "pos":23, "directions": "N/W"},
{"desc":"C5. school to your west, road to your east", "pos":24, "directions": "N/S/E"},
{"desc":"C6. in the road.", "pos":25, "directions": "N/S/E/W"},
{"desc":"C7. your house to your east", "pos":26, "directions": "N/S/E/W"},
{"desc":"C8. you are in your room. STARTING POS", "pos":27, "directions": "E",},
{"desc":"C9. you are in your living room.", "pos":28, "directions": "S/E/W", "items":["BAT"]},
{"desc":"C10. you are in your backyard. the wall is on your east", "pos":29, "directions": "N/S/W"},

{"desc":"D1. wall to your west", "pos":30, "directions": "N/S/E",},
{"desc":"D2. school to your north", "pos":31, "directions": "S/E/W"},
{"desc":"D3. school to your north you. you are at the entrance.", "pos":32, "directions": "N/S/E/W"},
{"desc":"D4. school to your north", "pos":33, "directions": "S/E/W"},
{"desc":"D5. road to your east.", "pos":34, "directions": "N/S/E/W"},
{"desc":"D6. in the road", "pos":35, "directions": "N/S/E/W"},
{"desc":"D7. road to your west", "pos":36, "directions": "N/S/E/W"},
{"desc":"D8. your house to your north and west", "pos":37, "directions": "N/S/W"},
{"desc":"D9. you are in your bathroom", "pos":38, "directions": "N", "items":["BANDAID"]},
{"desc":"D10. your house on your west. wall on your east", "pos":39, "directions": "N/S/W"},

{"desc":"E1. wall to your west", "pos":40, "directions": "N/S/E",},
{"desc":"E2.", "pos":41, "directions": "N/S/E/W"},
{"desc":"E3. probably inside some structure with items", "pos":42, "directions": "N/S/E/W"},
{"desc":"E4. same", "pos":43, "directions": "N/S/E/W"},
{"desc":"E5. same ", "pos":44, "directions": "N/S/E/W"},
{"desc":"E6. road", "pos":45, "directions": "N/S/E/W"},
{"desc":"E7.", "pos":46, "directions": "N/S/E/W"},
{"desc":"E8.", "pos":47, "directions": "N/S/E/W"},
{"desc":"E9.", "pos":48, "directions": "N/S/E/W"},
{"desc":"E10. wall on east", "pos":49, "directions": "N/S/W"},

{"desc":"F1.", "pos":50, "directions": "N/E",},
{"desc":"F2.", "pos":51, "directions": "N/E/W"},
{"desc":"F3.", "pos":52, "directions": "N/W"},
{"desc":"F4.", "pos":53, "directions": "N/E/W"},
{"desc":"F5.", "pos":54, "directions": "N/E/W"},
{"desc":"F6.", "pos":55, "directions": "N/E/W"},
{"desc":"F7.", "pos":56, "directions": "N/E/W"},
{"desc":"F8.", "pos":57, "directions": "N/E/W"},
{"desc":"F9.", "pos":58, "directions": "N/E/W"},
{"desc":"F10.", "pos":59, "directions": "N/W", "items":["ROPE"]},]


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
    print("You can go EAST.")

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

            if pos == 13:
                print("win.")
                break
    
        #if they want to take/pick up something
        elif command == "TAKE":

            #item is the second part of the input
            item = noun
            #takes item
            take(pos, item)

        #if they type something different
        else:
            print("I don't understand that command.")
            
game()
