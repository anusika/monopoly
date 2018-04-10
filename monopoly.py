import numpy as np
import random as rd
import matplotlib.pyplot as mpl




class Player(object):
    def __init__(self, number, risky, locations, monies, wins = 0, position = 0, money= 1500, jail = False, jail_time = 0, turn = False, turns = 0):
        self.position = position
        self.number = number
        self.money = money
        self.locations = locations
        self.risky = risky/100
        self.jail = jail
        self.jail_time = jail_time
        self.turn = turn
        self.wins = 0
        self.monies = monies
        self.turns = turns
    def want(self, location):
        testing = rd.random()
        if player.money < location.buy:
            return False
        elif testing <= self.risky:
            return True
        else:
            return False
    

class Property(object):
    properties = []
    def __init__(self, name, location, colour = "Null", buy = "null", rent="null", hits = 0, owned = False):
        Property.properties.append(self)
        self.location = location
        self.colour = colour
        self.name = name
        self.buy = buy
        self.rent = rent
        self.hits = hits
        self.owned = owned
        
    def __str__(self):
        return "Name: {} || Location: {} || Colour: {} || Buy: {} || Rent: {}".format(self.name,
                                                self.location, self.colour,self.buy,self.rent)


go = Property( 'Go', 0)
mediterranean = Property('Mediterranean Avenue', 1, 'Brown', 60, 2)
chest1 = Property('Coummunity Chest 1', 2, 'Surprise')
baltic = Property('Baltic Avenue',3, 'Brown', 60, 4)
income = Property('Income Tax', 4, 'Tax')
reading = Property('Reading Railroad', 5, 'Station', 200, 25)
oriental = Property('Oriental Avenue', 6, 'Light Blue', 100, 6)
chance1 = Property('Chance 1', 7, 'Surprise')
vermont= Property('Vermont Avenue',8, 'Light Blue', 100, 6)
connecticut = Property('Connecticut Avenue', 9, 'Light Blue', 120, 8)
jail = Property('Jail/Just Visting', 10)
charles = Property('St.Charles Place', 11, 'Pink', 140, 10)
electric = Property('Electric Company', 12, 'Utility', 150, 'roll')
states = Property('States Avenue', 13, 'Pink', 140, 10)
virginia = Property('Virginia Avenue', 14, 'Pink', 160, 12)
penn_railroad = Property('Pennsylvania Railroad', 15, 'Station', 200, 25)
james = Property('St.James Place',16, 'Orange', 180, 14)
chest2 = Property('Chest 2', 17, 'Surprise')
tennessee = Property('Tennessee Avenue',18, 'Orange', 180, 14)
york = Property('New York Avenue', 19, 'Orange', 200, 16)
free = Property('Free Parking', 20)
kentucky = Property('Kentucky Avenue', 21, 'Red', 220, 18)
chance2 = Property('Chance 2', 22, 'Surprise')
indiana = Property('Indiana Avenue', 23, 'Red', 220, 18)
illinois = Property('Illinois Avenue', 24, 'Red', 240, 20)
bo = Property('B and O Railroad', 25, 'Station', 200, 25)
atlantic = Property('Atlantic Avenue', 26, 'Yellow', 260, 22)
ventnor = Property('Strand Avenue', 27, 'Yellow', 260, 22)
water = Property('Water Works', 28, 'Utility', 150, 'roll')
marvin = Property('Marvin Gardens', 29, 'Yellow', 280, 24)
gojail = Property('Go To Jail', 30)
pacific = Property('Pacific Avenue', 31, 'Green', 300, 26)
carolina = Property('North Carolina Avenue', 32, 'Green', 300, 26)
chest3 = Property('Community Chest 3', 33, 'Surprise')
pennsylvania= Property('Pennsylvania Avenue', 34, 'Green', 320, 28)
shortline = Property('Short Line', 35, 'Station', 200, 25)
chance3 = Property('Chance 3', 36, 'Surprise')
park = Property('Park Place', 37, 'Blue', 350, 35)
tax = Property('Super Tax', 38, 'Tax')
boardwalk = Property('BoardWalk', 39, 'Blue', 400, 50)


def RollDice(player,jail):
    doubles = 0
    total = 0    
    while doubles < 3:
        dice1 = rd.randint(1,6)
        dice2 = rd.randint(1,6)
        roll = dice1 + dice2
        if dice1 == dice2:
            doubles += 1
            total += roll
            if player.jail and jail:
                #print(doubles)
                #print("out of jail!")
                player.jail = False
                return [total, player.jail]
        else:
            if player.jail and jail:
                #print("Player", player.number, 'still in jail')
                return "jail"
            else:
                total += roll
                return total
    if doubles == 3:
        return 'jail'

        
def simple_simulation(numgames, numturns, jail):
    properties_list = Property.properties
    railroads = []
    utilities = []
    for place in properties_list:
        if place.colour == 'Station':
            railroads.append(place)
        elif place.colour == 'Utility':
            utilities.append(place)
        
    railroads_location = [railroad.location for railroad in railroads]
    utilities_location = [utility.location for utility in utilities]

    games_completed = 0
    
    while games_completed < numgames:
            
        player = Player(1, 0, 'null', 'null')
        
        chest_options = [0, 10, 'n' 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                         'n', 'n', 'n', 'n', 'n', 'n']
        current_chest = [i for i in chest_options]
        rd.shuffle(current_chest)

        chance_options = [0, 24, 11, 10, 5, 39, 'back', 'ulility', 'railroad', 'n',
                          'n', 'n', 'n', 'n', 'n', 'n', 'n']
        current_chance = [i for i in chance_options]
        rd.shuffle(current_chance)

        turns = 0
        jail_time = 0

        
        while turns < numturns:
            
            roll = RollDice(player, jail)

            if player.jail and jail_time == 3 and jail:
                #print('must leave jail')
                player.jail = False
                jail_time = 0
                turns -= 1
                player.turns -=1
                
                continue
                
            elif isinstance(roll, list):
                #print('math to get out of jail')
                #print(roll[0])
                player.jail = False
                roll = roll[0]
                jail_time = 0
                turns -= 1
                player.turns -=1
                
                continue
             
            if isinstance(roll, str):
                #print('going to jail')
                player.position = 10
                if jail:
                    player.jail = True
                    jail_time += 1
                    #print('player sent to jail')
                
            else:
                player.position = (player.position + roll)%40

                if player.position == 30:
                    #print('going to jail')
                    player.position = 10
                    if jail:
                        player.jail = True
                        jail_time += 1
                        #print('player sent to jail')
        

                elif player.position in [2, 17, 33]:
                    chest_played = current_chest.pop(0)
                    if len(current_chest)==0:
                        current_chest = [i for i in chest_options]
                        rd.shuffle(current_chest)
                    #print(chest_played)

                    if chest_played == 10:
                        player.postion = 10
                        if jail:
                            player.jail = True
                            jail_time += 1


                    elif isinstance(chest_played, int):
                        player.position = chest_played
                        
                elif player.position in [7, 22, 36]:
                    chance_played = current_chance.pop(0)
                    if len(current_chance)==0:
                        current_chance = [i for i in chance_options]
                        rd.shuffle(current_chance)
                    #print(chance_played)

                    if chance_played == 10:
                        player.postion = 10
                        if jail:
                            player.jail = True
                            jail_time += 1
                            #print('player sent to jail')

                    if isinstance(chance_played, int):
                        player.position = chance_played
                        
                    elif chance_played == 'back':
                        #print('moving back')
                        player.position = player.position-3 #don't need to %40 bc there's no chance spot on the board that's 3 away from go

                    elif chance_played == 'ultility':
                        #print('moving to utility')
                        while player.position not in utilities_location:
                            player.position = (player.position + 1)%40
                            

                    elif chance_played == 'railroad':
                        #print('moving to raildroad')
                        while player.position not in railroads_location:
                            player.position = (player.position + 1)%40
                        
                    else:
                        pass

            properties_list[player.position].hits += 1
            #print("Turn:", turns, "Name:", properties_list[player.position].name, "times hit:", properties_list[player.position].hits)

            

            player.turns += 1
                #print("player:", player.number, "money left:", player.money)
                
            if player.turns-1 != turns:
                print('error')
                
            #print("player", player.number, "turns", player.turns)

                
            turns += 1
        games_completed += 1
        if games_completed%1000 == 0:
            print("game",games_completed, "finished")
    return properties_list

#simple_simulation(1, 20, True)

def calc_time(games, numturns):
    simulation = simple_simulation(games, numturns, jail=True)
    turns = [location.hits for location in simulation]
    turns_percentage= [(turn/(games*numturns))*100 for turn in turns]
    fig, ax = mpl.subplots()
    rects = ax.bar(numbers, turns_percentage, color = 'y')
    ax.set_ylabel('Percentage of Turns Spent')
    ax.set_title('Percentage of Turns Spent at Each Space ({} Games at {} Turns/Game)'.format(games, numturns))
    ax.set_xticks(numbers)
    ax.set_xticklabels(names, rotation = 90)
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50)
    rects = ax.patches
    label_bars(rects)
    mpl.tight_layout()
    return turns_percentage


def calc_hit(games, numturns):
    simulation = simple_simulation(games, numturns, jail=False)
    hits = [location.hits for location in simulation]
    hits_percentage= [(hit/(games*numturns))*100 for hit in hits]
    fig, ax = mpl.subplots()
    rects = ax.bar(numbers, hits_percentage, color = 'r')
    ax.set_ylabel('Percentage Chance of Hitting Space')
    ax.set_title('Percentage Chance of Hitting Each Space ({} Games at {} Turns/Game)'.format(games, numturns))
    ax.set_xticks(numbers)
    ax.set_xticklabels(names, rotation = 90)
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50)
    rects = ax.patches
    label_bars(rects)
    mpl.tight_layout()
    return hits_percentage

def label_bars(bars):
    for rect in bars:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        space = 5
        va = 'bottom'
        label = "{:.2f}".format(y_value)
        mpl.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va=va)
        
def compare_hits_time(games, numturns):
    hits = calc_hit(games, numturns)
    turns = calc_time(games, numturns)
    fig, ax = mpl.subplots()
    width= 0.35
    rects = ax.bar(numbers, hits, width, color = 'r')
    rects2 = ax.bar(numbers + width, turns, width, color = 'y')
    ax.set_ylabel('Percentage')
    ax.set_title('Comparison Between Percentage of Time Spent and Percentage Chance of Hitting Each Square ({} Games at {} Turns/Game)'.format(games, numturns+1))
    ax.set_xticks(numbers + width / 2)
    ax.set_xticklabels(names, rotation = 90)
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50)
    ax.legend((rects[0], rects2[0]), ('Chance of Hit Percentage', 'Turns Spent Percentage'))
    mpl.tight_layout()
    
names = [location.name for location in Property.properties]
numbers = np.arange(40)
#compare_hits_time(100,100)                 

def complicated_simulation(games, numturns, players):   
    properties_list = Property.properties
    railroads = []
    utilities = []
    for place in properties_list:
        if place.colour == 'Station':
            railroads.append(place)
        elif place.colour == 'Utility':
            utilities.append(place)
        
    railroads_location = [railroad.location for railroad in railroads]
    utilities_location = [utility.location for utility in utilities]

    games_completed = 0

    opponents = len(players) -1

    while games_completed < games:
        

        chest_options = [0, 10, 'rerror', 'tdoctor', 'ropera','rfund', 'thospital',
                             'rinsurance',  'rincome', 'rbirthday','tschool', 'rconsult',
                             'rinherit', 'rsecond',  'n', 'n', 'n']
        current_chest = [i for i in chest_options]
        rd.shuffle(current_chest)

        chance_options = [0, 24, 11, 10, 5, 39, 'back', 'ulility', 'railroad', 'rbank',
                          'tpoor', 'tplayer', 'rloans', 'rcrossword', 'n', 'n', 'n']
        current_chance = [i for i in chance_options]
        rd.shuffle(current_chance)

        turns = 0
        


        while turns < numturns:
            
            for player in players:
                
                player.turn = True
                #print('\n')
                #print('Player', player.number)
                #print('Player', player.number, 'owns', len(player.locations))
                #for location in player.locations:
                    #print(location.name)
                roll = RollDice(player, jail = True)
                #print("Player", player.number, "rolled", roll)
                #print(player.jail)
                #print(player.jail_time)
                if player.jail and player.jail_time == 3:
                    #print('must leave jail')
                    #print('turns', player.turns)
                    player.jail = False
                    player.jail_time = 0
                    player.money -= 50
                    player.turns += 1
                    player.monies.append(player.money)
                    properties_list[10].hits += 1
                    continue

                    
                elif isinstance(roll, list):
                    #print('math to get out of jail')
                    #print(roll[0])
                    player.jail = False
                    #roll = roll[0]
                    player.jail_time = 0
                    #print('turns', player.turns)
                    player.turns += 1
                    player.monies.append(player.money)
                    properties_list[10].hits += 1
                    continue

                elif isinstance(roll, str):
                    #print('going to jail')
                    player.position = 10
                    
                else:
                    player.position = (player.position + roll)%40

                    if player.position == 30:
                        #print('going to jail')
                        player.position = 10
                        

                    elif player.position in [2, 17, 33]:
                        chest_played = current_chest.pop(0)
                        #print('chest played:', chest_played)
                        if len(current_chest)==0:
                            current_chest = [i for i in chest_options]
                            rd.shuffle(current_chest)
                        

                        if isinstance(chest_played, int):
                            player.position = chest_played

                        elif chest_played == 'rerror':
                            player.money += 200

                        elif chest_played == 'tdoctor':
                            player.money -= 50

                        elif chest_played == 'ropera':
                            player.money += 50

                        elif chest_played == 'rfund' or chest_played == 'rinherit' or chest_played == 'rinsurance':
                            player.money += 100

                        elif chest_played == 'rincome':
                            player.money += 20

                        elif chest_played == 'rbirthday':
                            for opponent in players:
                                if opponent.turn == False:
                                    opponent.money += 10
                                    player.money-= 10
                                    #print('player', player.number, 'lost money')
                                    #print('player', opponent.number, 'got money')

                        elif chest_played == 'thospital':
                            player.money -= 100

                        elif chest_played == 'tschool':
                            player.money -= 150

                        elif chest_played == 'rconsult':
                            player.money += 25

                        elif chest_played == 'rsecond':
                            player.money += 10

                        else:
                            pass
                        
                    elif player.position in [7, 22, 36]:
                        chance_played = current_chance.pop(0)
                        #print('chance played:', chance_played)
                        if len(current_chance)==0:
                            current_chance = [i for i in chance_options]
                            rd.shuffle(current_chance)

                        if isinstance(chance_played, int):
                            player.position = chance_played
                            if player.position in [24, 11, 5, 39]:
                                player.money += 200
                            
                        elif chance_played == 'back':
                            #print('moving back')
                            player.position = player.position-3 #don't need to %40 bc there's no chance spot on the board that's 3 away from go

                        elif chance_played == 'ultility':
                            #print('moving to utility')
                            while player.position not in utilities_location:
                                player.position = (player.position + 1)%40
                                

                        elif chance_played == 'railroad':
                            #print('moving to raildroad')
                            while player.position not in railroads_location:
                                player.position = (player.position + 1)%40
                                
                        elif chance_played == 'rbank':
                            player.money += 50
                                
                        elif chance_played == 'tpoor':
                            player.money -= 15

                        elif chance_played == 'tplayer':
                            for opponent in players:
                                if opponent.turn == False:
                                    opponent.money += 50
                                    player.money-= 50
                                    #print('player', player.number, 'lost money')
                                    #print('player', opponent.number, 'got money')

                        elif chance_played == 'rloans':
                            player.money += 150

                        elif chance_played == 'rcrossword':
                            player.money += 100
                            
                        else:
                            pass
                current = properties_list[player.position]
                current.hits += 1
                #print("Turn:", turns, "Player", player.number, "Name:", properties_list[player.position].name, "times hit:", current.hits)
                
                if current.owned == False and current.buy != 'null':
            
                    if player.want(properties_list[player.position]):
                        #print('want')
                        #print('money spent:' ,properties_list[player.position].buy)
                        player.money -= current.buy
                        current.owned = True
                        #print(properties_list[player.position].owned)
                        player.locations.append(current)
                        #print('Player:', player.number, 'owns', len(player.locations))
                    #else:
                        #print('does not want')

                if properties_list[player.position].owned == True and properties_list[player.position] not in player.locations:
                    current = properties_list[player.position]
                    
                    if current.colour == "Utility":
                        #print('paying rent for utility')
                        #print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                        owned_utilities = 0
                        for opp in players:
                            if current in opp.locations:
                                for location in opp.locations:
                                    if location in utilities:
                                        owned_utilities +=1
                                    else:
                                        pass
                            if owned_utilities == 1:
                                player.money -= (4*roll)
                                opp.money += (4*roll)
                            elif owned_utilities == 2:
                                player.money -= (10*roll)
                                opp.money += (10*roll)
                        #else:
                            #print("how did we get here", owned_utilities)
                        #print('owned utility', owned_utilities)
                        #print('player', opp.number, 'got payed')
                            
                    elif current.colour == "Station":
                        #print('paying rent for railroads')
                        #print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                        owned_stations = 0
                        for opp in players:
                            if current in opp.locations:
                                for location in opp.locations:
                                    if location in railroads:
                                        owned_stations +=1
                                    else:
                                        pass
                            if owned_stations == 1:
                                player.money -= 25
                                opp.money +=25
                            elif owned_stations == 2:
                                player.money -= 50
                                opp.money +=50
                            elif owned_stations == 3:
                                player.money -= 100
                                opp.money +=100
                            elif owned_stations == 4:
                                player.money -= 200
                                opp.money +=200
                        #else:
                            #print("how did we get here", owned_stations)
                        #print('owned stations', owned_stations)
                        #print('player', opp.number, 'got payed')
                                  
                    else:      
                        player.money -= current.rent
                        #print('paying rent Player:', player.number)
                        for opponenet in players:
                            if current in opponenet.locations:
                                opponenet.money += current.rent
                                #print("I got payed Player:", opponenet.number)
                            else:
                                pass
                        
                
                #print("active player", player.number)
                            
                if player.position == 0:
                    player.money += 200


                    #print("player is in jail")
                if player.position == 10:
                    player.jail = True
                    player.jail_time += 1
                    
                player.monies.append(player.money)    
                player.turn = False
                player.turns += 1
                #print("player:", player.number, "money left:", player.money)
                
                #if player.turns-1 != turns:
                    #print('error')
                
                #print("player", player.number, "turns", player.turns)

                
            turns += 1
            
        money = [player.money for player in players]
        for player in players:
            if player.money == max(money):
                player.wins += 1
                
        #print(turns)        
        games_completed += 1
        if games_completed%100 == 0:
            print("game",games_completed, "finished")
    for player in players:
        print('player:', player.number, 'wins', player.wins, 'turns:',player.turns)
    #print(games_completed)
    #print(len(players))
    return properties_list, players

#print(players)
#complicated_simulation(1, 100, players)

def calc_time_complicated(games, numturns):
    numbers = np.arange(40)
    names = [location.name for location in Property.properties]
    simulation = complicated_simulation(games, numturns, players)
    turns = [location.hits for location in simulation[0]]
    #print(turns)
    turns_percentage= [(turn/(games*numturns*len(players)))*100 for turn in turns]
    #print(turns_percentage)
    fig, ax = mpl.subplots()
    rects = ax.bar(numbers, turns_percentage, color = 'y')
    ax.set_ylabel('Percentage of Turns Spent')
    ax.set_title('Percentage of Turns Spent at Each Space ({} Games at {} Turns/Game with {} players)'.format(games, numturns, len(players)))
    ax.set_xticks(numbers)
    ax.set_xticklabels(names, rotation = 90)
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50)
    rects = ax.patches
    label_bars(rects)
    mpl.tight_layout()




player = Player(1, 70, [], [])
player2 = Player(2, 50, [], [])
player3 = Player(3, 30, [], [])
player4 = Player(4, 20, [], [])
players = [player, player2, player3, player4]
                       
#sample = complicated_simulation(1, 30, players)
#calc_time_complicated(100, 100)
#for player in sample[1]:
    #print(player.monies)
    #print(len(player.monies))
                

def calc_monies(numturns):
    simulation = complicated_simulation(1, numturns, players)
    monies = simulation[1]
    n = np.arange(numturns)
    for player in monies:
        mpl.plot(n, player.monies)


#calc_monies(100)

mpl.show()

