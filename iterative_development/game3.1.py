#version 3.1:
# going on the road now has a 20% chance of killing you. 
# made a function to fight zombies: if you have a knife, they will die 100%.
#   if you don't have a knife, you have a 50% chance of getting killed, or 50% of being safe.

# added a help crew that will guide you if you need help

import re, time, random

WIDTH = 10 #the width of the map
STARTING_POS = 27 #starting position
death = False #death variable; turns True when the player dies.

inventory = []
#################################
#map size: 6x10, so 0 to 59 pos
#        N      |----10---------|
#      W-+-E    |               |
#        S      6               6
#               |               |
#               |-----10--------|
#################################

#the map. "desc" is the description of the place,
#"pos" is the player position in numbers,
#"directions" is the available directions that the player can go
#"items" is the items that are in the pos
map = [
{"desc":"A1. Your high-school is to the south-east. The city wall surrounds you from the north and west.", "pos":0, "directions":"S/E"}, 
{"desc":"A2. The back wall of your high-school is directly south of you. The city wall surrounds you from the north.", "pos":1, "directions":"E/W"},
{"desc":"A3. The back wall of your high-school is directly south of you. The city wall surrounds you from the north.", "pos":2, "directions": "E/W"},
{"desc":"A4. The back wall of your high-school is directly south of you. The city wall surrounds you from the north.", "pos":3, "directions": "E/W"},
{"desc":"A5. Your high-school is to the south-west of you. The city wall surrounds you from the north.\nDirectly to the east of you is a busy road.", "pos":4, "directions": "S/E/W"},
{"desc":"A6. You're in the middle of the road. The city wall surrounds you from the north.", "pos":5, "directions": "S/E/W"},
{"desc":"A7. You see your house to the south-east. The city wall surrounds you from the north. Directly to the west of you is a busy road.", "pos":6, "directions": "S/E/W", "zombie":True}, #zombie here
{"desc":"A8. You see your house to the south. The city wall surrounds you from the north.", "pos":7, "directions": "S/E/W"},
{"desc":"A9. You see your house to the south. The city wall surrounds you from the north.", "pos":8, "directions": "S/E/W"},
{"desc":"A10. You see your backyard to the south. The city wall surrounds you from the north and the east", "pos":9, "directions": "S/W"},

{"desc":"B1. The city wall surrounds you from the west. The wall of your high-school is directy to the east of you. Through the window you can see that the room is infested with zombies.", "pos":10, "directions": "N/S"},
{"desc":"B2. You feel a zombie grab your neck. Oh no! You're infected.", "pos":11}, # no directions because you die if you come here
{"desc":"B3. You made it another step, but you can still feel zombies surrounding you.\nAll you need to do is just get to the stairs.", "pos":12, "directions": "S/E/W"},
{"desc":"B4. You made it to the stairs.", "pos":13}, ############# winning scene
{"desc":"B5. The wall of your high-school is directly to the west of you. Directly east, there is a busy road.", "pos":14, "directions": "N/S/E"},
{"desc":"B6. You're in the middle of the road.", "pos":15, "directions": "N/S/E/W"},
{"desc":"B7. There is a busy road directly to the west, and your house is to the south-east.", "pos":16, "directions": "N/S/E/W"},
{"desc":"B8. Your house is directly south of you. You are facing the back wall of your room.", "pos":17, "directions": "N/E/W"},
{"desc":"B9. Your house is directly south of you, and you can see your living room through the window", "pos":18, "directions": "N/E/W", "zombie":True},
{"desc":"B10. Your backyard is directly south of you, and the city wall surrounds you from the east.", "pos":19, "directions": "N/S/W"},

{"desc":"C1. The wall of the school is directly on the east, and the city wall is on the west", "pos":20, "directions": "N/S",},
{"desc":"C2. You step right into the cold embrace of a zombie. You are bitten and die.", "pos":21}, 
{"desc":"C3. You enter the school. It's dark inside, and you can't seem to find the light switch. \nYou can feel the presence of some things that really shouldn't be there. \nAll you need to do is find the stairs, and you'll be safe. Any wrong move will cost you.", "pos":22, "directions": "N/S/E/W"},
{"desc":"C4. Oh no! You went the wrong way, and walked straight towards a gargling sound. \nThe zombie turns to grab you, and you get infected.", "pos":23},
{"desc":"C5. The side your school is directly to the west, and there is a busy road to the east.", "pos":24, "directions": "N/S/E"},
{"desc":"C6. You are in the middle of the road.", "pos":25, "directions": "N/S/E/W"},
{"desc":"C7. Your house is directly to the east, and there is a busy road on the west.", "pos":26, "directions": "N/S/E/W"},
{"desc":"C8. You are in your room. The living room is to the east.", "pos":27, "directions": "E"}, ############# starting pos!!!!!!!
{"desc":"C9. You are in your living room. Your room is to the west, and the bathroom is to the south. \nYour backyard is to the east, where you can leave the house.", "pos":28, "directions": "S/E/W"},
{"desc":"C10. You are in your backyard. The city wall surrounds you to the east.", "pos":29, "directions": "N/S/W"},

{"desc":"D1. The city wall surrounds you from the west. Your high-school is to the north-east.", "pos":30, "directions": "N/S/E"},
{"desc":"D2. The front wall of school is directly to the north, and the entrance is to the east. \nThere is an abandoned warehouse to the south-east.", "pos":31, "directions": "S/E/W"},
{"desc":"D3. You are at the entrance of the school, to the north. The gate is locked, and you need a key.\nThere is an abandoned warehouse to the south.", "pos":32, "directions": "S/E/W"}, ##special pos, you need a key to enter###
{"desc":"D4. The front wall of your school is directly to the north, and the entrance is to the west. \nThere is an abandoned warehouse to the south.", "pos":33, "directions": "S/E/W"},
{"desc":"D5. Your school is to the north-west, and there is a busy road directly to the east. \nThere is an abandoned warehouse to the south-west.", "pos":34, "directions": "N/S/E/W", "zombie":True}, #zombie here
{"desc":"D6. You are in the middle of the road.", "pos":35, "directions": "N/S/E/W"},
{"desc":"D7. The road is to the west, and your house is to the east.", "pos":36, "directions": "N/S/E/W"},
{"desc":"D8. You can enter your room to the north, and another part of your house is on the west.", "pos":37, "directions": "N/S/W"},
{"desc":"D9. You are in your bathroom. Your living room is to the north.", "pos":38, "directions": "N", "items":["TOOTHBRUSH"]},
{"desc":"D10. Your house is on the west. The city wall surrounds you to the east.", "pos":39, "directions": "N/S"},

{"desc":"E1. The city wall surrounds you from the west.", "pos":40, "directions": "N/S/E",},
{"desc":"E2. There is some sort of small abandoned warehouse to the east. Your high-school is somewhere to the north.", "pos":41, "directions": "N/S/E/W"},
{"desc":"E3. You are inside the storage warehouse. There's a few zombies wandering around inside, be careful.", "pos":42, "directions": "N/S/E/W", "items":["ROPE"]},
{"desc":"E4. You are inside the storage warehouse.", "pos":43, "directions": "N/S/E/W", "zombie":True}, ######################## should encounter a fightable zombie here
{"desc":"E5. There is some sort of small abandoned warehouse to the west. \nYou can see that there are a few zombies roaming around inside, let's hope you don't encounter one. \nThere is a busy road to the east.", "pos":44, "directions": "N/S/E/W"},
{"desc":"E6. You are in the middle of a busy road.", "pos":45, "directions": "N/S/E/W"},
{"desc":"E7. There is a busy road to the west. You can see your house to the north-east.", "pos":46, "directions": "N/S/E/W" },
{"desc":"E8. Your house is to the north. To the south is a patch of bushes.", "pos":47, "directions": "N/S/E/W", "zombie":True}, #zombie here
{"desc":"E9. Your house - the bathroom wall - is directly north of you. To the south is a patch of bushes.", "pos":48, "directions": "S/E/W"},
{"desc":"E10. The city wall surrounds you to the east.", "pos":49, "directions": "N/S/W"},

{"desc":"F1. The city wall surrounds you from the south and west. Further to the east is a small abandoned warehouse.", "pos":50, "directions": "N/E", "zombie":True}, #zombie  here
{"desc":"F2. The city wall surrounds you to the south. Directly to the east is a storage warehouse.", "pos":51, "directions": "N/E/W"},
{"desc":"F3. You are inside the storage warehouse. There are zombies wandering around.", "pos":52, "directions": "N/E/W",  "items":["KNIFE"]},
{"desc":"F4. You are inside the storage warehouse.  You find nothing in this corner.", "pos":53, "directions": "N/E/W"},
{"desc":"F5. The city wall surrounds you from the south. There is an abandoned warehouse to the east, and a busy road to the east.", "pos":54, "directions": "N/E/W"},
{"desc":"F6. You are in the middle of the road. The city wall surrounds you from the south.", "pos":55, "directions": "N/E/W"},
{"desc":"F7. You are walking inside small bushes. There is a busy road to the west, and the city wall surrounds you from the south.", "pos":56, "directions": "N/E/W"},
{"desc":"F8. You are walking in a patch of small bushes. The city wall surrounds you from the south.\nYou see something glistening on the ground.", "pos":57, "directions": "N/E/W", "items":["KEY"]},
{"desc":"F9. You are walking in a patch of small bushes. The city wall surrounds you from the south.", "pos":58, "directions": "N/E/W"},
{"desc":"F10. The city wall surrounds you from the south and east.", "pos":59, "directions": "N/W"},
]

#----------------------game functions--------------------------------------------------------------

def canmove(pos, direction):
    """This function checks if the"""
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
    
        describe(pos)

    #if they enter anything else,
    else:
        print("You can't go that way...")
        
    return pos

def describe(pos):
    """A function that prints out the description of the player's new position, and things related to that, i.e the directions that they can go and the items that are there.
    This function also contains the fight function."""

    #prints the new pos description
    print("\n"+map[pos]["desc"])

    if "zombie" in map[pos] and map[pos]["zombie"] is False:
        print("There is a dead zombie body at your feet")

    #if there is a zombie in this pos,
    if "zombie" in map[pos] and map[pos]["zombie"]:
        #this is a list of things that it can say when there is a zombie.
        print_list=["There is a zombie staring directly at you.","You come face-to-face with a zombie.","You encounter a vicious zombie."]
        print(random.choice(print_list)) #chooses a random phrase and says it.
        if fight(pos) == True: #if True, means the player died.
            return True 
    
    #if they are in these positions, they have a 20% chance of dying (in the road, 20% chance of getting ran over.)    
    if pos in (5, 15, 25, 35, 45, 55):
        chance=random.randint(1,5) #gets a random number from 1 to 5
        if chance == 1: # if the number is 1, the player gets ran over.
            time.sleep(1)
            print("You were unlucky, and got ran over by a zombie-driven car.")
            global death
            death = True
            return death

    #if the key "items" exists for the new pos, and it is not empty,
    #print the items
    if "items" in map[pos] and map[pos]["items"]:
        print("There is: " + ', '.join(map[pos]["items"]))
        
    time.sleep(2)

    #prints the directions that the player can go
    if "directions" in map[pos]:
        new_directions = map[pos]["directions"]
        print(f"You can go {new_directions}.")
        time.sleep(1)

def fight(pos):
    """When the player encounters a zombie, this function will decide if they get to kill the zombie or die."""
    
    #then check if they have picked up a knife.
    if "KNIFE" in inventory: #if they have the knife, then they will be able to kill the zombie.
        #the key "zombie" turns false, meaning that there is no more zombie in that pos.
        map[pos]["zombie"] = False
        time.sleep(1.5)
        print("You used your knife to kill the zombie.")
        return False
            
    #if they don't have the knife, they have a 50% chance of dying.
    else:
        chance=random.randint(1,2) #chooses a random number out of 1 and 2
        #if the random number is 1, the player dies.
        if chance==1:
            global death
            death = True #change death variable to True
            time.sleep(2)
            print("You struggled with the zombie, but he was too strong. You died.")
            return death
        
        else: #they get to live, but the zombie stays there.
            time.sleep(2)
            print("Lucky! You managed to ward off the zombie. Try not to run into him again.")
            return False

def cantake(pos, item):
    """checks if the item that the user entered is actually there"""
    
    #checks if the pos has the key "items", and that it is not null.
    if "items" in map[pos] and map[pos]["items"]:

        #checks if the item that the user entered matches the one that is there.
        if item in map[pos]["items"]:
            return True
        else:
            return False
        
    #if there's no items in that pos, then return False
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
            
#functions to check the player's input-----------------------------------------------------------------------
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
        command = re.split("\s+",string)[0]
        noun = re.split("\s+",string)[1]

        return command, noun
    
    else: #else return false
        return False 
 
#---------main loop-------------------------------------

#main loop for the gameplay
def main_loop():
    """Main loop for the game"""
    
    #starting description of the game
    pos=STARTING_POS 
    print("You wake up in your room. You look outside, and you see... zombies?")
    time.sleep(2)
    print("""Huh, it's a
                        _     _                         
    _______   _ __ ___ | |__ (_) ___                    
    |_  / _ \| '_ ` _ \| '_ \| |/ _ \                    
    / / (_)  | | | | | | |_) | |  __/                    
    /___\___/|_| |_| |_|_.__/|_|\___| """)
    time.sleep(1)
    print("""     __ _ _ __   ___   ___ __ _| |_   _ _ __  ___  ___   
    / _` | '_ \ / _ \ / __/ _` | | | | | '_ \/ __|/ _ \  
   | (_| | |_) | (_) | (_| (_| | | |_| | |_) \__ \  __/ 
    \__,_| .__/ \___/ \___\__,_|_|\__, | .__/|___/\___|
        |_|                      |___/|_|             
    """)
    time.sleep(2)
    print("Get out of your house and find your way to safety.")
    print("You can go EAST (E).")
    time.sleep(2)
    print("\nIf you are stuck, type \"HELP\" to get some help on how to navigate the game. \nAlphanumeric coordinates (A1, B7, etc.) are provided for easier navigation.")
    time.sleep(2)
    
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
    Type "go [direction]" to go a direction. You can type "N" or "North" to go north.
    Type "take" [item] to pick up an item.
    Type "inv" to show your inventory.
    Type "exit" to quit the game.""")
            time.sleep(1)
            continue

#-----------input for doing things---------------------------

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

#----------------winning/losing conditions, special conditions---------------------

        #if they have the key, then they can go inside the school;
        #   WHEN (!!) they pick up the key, I add another available direction to pos=32 so they are able to go north into the school; 
        if "KEY" in inventory:
            map[32]["directions"]="N/S/E/W"
            #then I change the description of the pos=32 square so that it says they used the key to unlock the door.
            #this will show when they arrive there with the key.
            map[32]["desc"]="D3. You are at the entrance of the school, to the north. \nYou used your key to open the gate."
        
        #if they have the key and they get to pos = 32, then the key will be removed from their inventory
        #so that they "use" the key to unlock the gate.
        if "KEY" in inventory and pos == 32:
            inventory.remove("KEY")   
                      
        #if they go into these pos, they die instantly (certain places inside the school where there are zombies.)  
        if pos in (11, 21, 23) or death == True:
            time.sleep(3)
            print(""" _______  _______  _______  _______    _______           _______  _______ 
(  ____ \(  ___  )(       )(  ____ \  (  ___  )|\     /|(  ____ \(  ____ )
| (    \/| (   ) || () () || (    \/  | (   ) || )   ( || (    \/| (    )|
| |      | (___) || || || || (__      | |   | || |   | || (__    | (____)|
| | ____ |  ___  || |(_)| ||  __)     | |   | |( (   ) )|  __)   |     __)
| | \_  )| (   ) || |   | || (        | |   | | \ \_/ / | (      | (\ (   
| (___) || )   ( || )   ( || (____/\  | (___) |  \   /  | (____/\| ) \ \__
(_______)|/     \||/     \|(_______/  (_______)   \_/   (_______/|/   \__/""")
            time.sleep(2)
            print("\nThank you for playing this game!")
            break 
            
        #if they make it to the winning pos, they win!
        if pos == 13:
            time.sleep(0.5)
            print("You run up the stairs, with zombies chasing at your feet, and you manage to get to the roof of the building, shutting them out.")
            time.sleep(1)
            print("You stay there for what seems like an eternity, when finally, a helicopter comes and saves you.")
            time.sleep(2)
            print("""                         _       _______   __   __
   __  ______  __  __   | |     / /  _/ | / /  / /
  / / / / __ \/ / / /   | | /| / // //  |/ /  / / 
 / /_/ / /_/ / /_/ /    | |/ |/ // // /|  /  /_/  
 \__, /\____/\__,_/     |__/|__/___/_/ |_/  (_)   
/____/                                            """) 
            time.sleep(2)
            print("\nThank you for playing this game!")
            break          
    
main_loop()
