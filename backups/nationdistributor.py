from random import shuffle

def main():
    
    #First define the lists of nations
    ea_nations = ["Arcoscephale", "Ermor", "Ulm", "Marverni", "Sauromatia", "T'ien Ch'i", "Machaka", "Mictlan", "Absyia", "Caelum", "C'tis", "Pangaea", "Agartha", "Tir na n'Og", "Fomoria", "Vanheim", "Helheim", "Niefelheim", "Rus", "Kailasa", "Lanka", "Yomi", "Hinnom", "Berytos", "Ur", "Xibalba", "Mekone", "Ubar", "Atlantis", "R'lyeh", "Pelagia", "Oceania", "Therodos"]
    
    ma_nations = ["Arcoscephale", "Ermor", "Sceleria", "Pythium", "Man", "Eriu", "Ulm", "Marignon", "Mictlan", "T'ien Ch'i", "Machaka", "Agartha", "Abysia", "Caelum", "C'tis", "Pangaea", "Asphodel", "Vanheim", "Jotunheim", "Vanheim", "Jotunheim", "Vanarus", "Bandar Log", "Shinuyama", "Ashdod", "Uruk", "Nazca", "Xibalba", "Phlegra", "Phaeacia", "Ind", "Na'Ba", "Atlantis", "R'lyeh", "Pelagia", "Oceania", "Ys"]
    
    la_nations = ["Arcoscephale", "Pythium", "Lemuria", "Man", "Ulm", "Marignon", "Mictlan", "T'ien Ch'i", "Jomon", "Agartha", "Abysia", "Caelum", "C'tis", "Pangaea", "Midgard", "Utgard", "Bogarus", "Patala", "Gath", "Ragha", "Xibalba", "Phlegra", "Vaettiheim", "Atlantis", "R'lyeh", "Erythia"]
    
    nation_list = []
    #Define a group of the usual suspects to speed things up
    usual_players = ["Geld", "Whind", "Pico", "Goat", "Wookie", "Blazier", "Angus", "Bobolot"]
    player_list = []
    
    #Get the age of the game to decide available nations
    age_input = input("What age? ('EA', 'MA', 'LA'): ")
    if age_input.upper() == "EA":
        nation_list = ea_nations
    elif age_input.upper() == "MA":
        nation_list = ma_nations
    elif age_input.upper() == "LA":
        nation_list = la_nations
    else:
        print("Input not recognised. Terminating.")
    
    #Get the list of players
    print("Choose from the following:")
    print("Type a number to distribute among an anonymous list of given number of players.")
    print("Type 0 to use the usual group of players (Angus, Bobolot, Blazier, Geld, Goat, Pico, Whind, Wookie).")
    print("Or start typing a list of names, pressing enter each time, with a final enter after.")
    player_input = input("Your input: ")
    
    if is_integer(player_input):
        if int(player_input) == 0:
            player_list = usual_players
        else:
            for i in range(1, int(player_input) + 1):
                player_list.append("Player " + str(i))
    else:
        while player_input != "":
            player_list.append(player_input)
            print("Players so far: ")
            print(player_list)
            player_input = input("Next player: ")
            
    #Generate a list of tuples containing player name and nations
    #Nations are randomly distributed with an even number if possible
    #But if there are extra nations, they are also distributed randomly
    #There is no bias in who gets extra choices
    
    shuffle(player_list)
    result_list = [(p,) for p in player_list]
    shuffle(nation_list)
    
    while len(nation_list) > 0:
        for i, p in enumerate(result_list):
            result_list[i] = result_list[i] + (nation_list.pop(),)
            if len(nation_list) == 0:
                break
    
    print("="*20)
    print("All {0} nations divided among {1} players:".format(age_input.upper(), len(player_list)))
    print("="*20)
    
    #put the list back in order (to an extent)
    result_list.sort()
    for r in result_list:
        print(r)
        
    print("="*20)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

        
main()
