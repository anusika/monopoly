import time
import numpy as np
import random as rd
import matplotlib.pyplot as mpl
import math
from itertools import groupby
from operator import attrgetter


class Player(object):
    def __init__(self, number, position, locations, risky, money= 1500, jail = 0):
        self.number = number
        self.position = position
        self.money = money
        self.locations = locations
        self.risky = risky
        self.jail = jail

class Property(object):
    properties = []
    def __init__(self, name, location, colour = "Null", buy = "null", rent="null", hits = 0):
        Property.properties.append(self)
        self.location = location
        self.colour = colour
        self.name = name
        self.buy = buy
        self.rent = rent
        self.hits = hits
        
    def __str__(self):
        return "Name: {} || Location: {} || Colour: {} || Buy: {} || Rent: {}".format(self.name,
                                                self.location, self.colour,self.buy,self.rent)

##seen = set()
##colours = [obj.colour for obj in simulation if obj.colour not in seen and not seen.add(obj.colour)]
##hits = [location.hits for location in simulation]    


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

chance_options = [0, 10, 24, 5, 'back', 'thouse', 'tstreet', 'tschool', 'tcharge', 'tspeeding',
                  'rbuilding', 'rcrossword', 'rbank']
chest_options = [0, 19, 10, 'thospital', 'tdoctor', 'tinsurance', 'rerror',
                 'rannuity', 'rinherit', 'rstock', 'rinterest', 'rincome',
               'rsecond', 'birthday',]



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
            if player.jail == 1 and jail:
                #print(doubles)
                #print("out of jail!")
                player.jail == 0
                return [total, player.jail]
        else:
            if player.jail == 1 and jail:
                #print('still in jail')
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
                          'n', 'n', 'n', 'n', 'n', 'n']
        current_chance = [i for i in chance_options]
        rd.shuffle(current_chance)

        turns = 0
        jail_time = 0
        
        while turns < numturns:
            
            roll = RollDice(player, jail)

            if player.jail == 1 and jail_time == 3 and jail:
                #print('must leave jail')
                player.jail = 0
                jail_time = 0
                turns -= 1
                continue
                
            elif isinstance(roll, list):
                #print('math to get out of jail')
                #print(roll[0])
                player.jail = 0
                roll = roll[0]
                jail_time = 0
                turns -= 1
                continue
             
            if isinstance(roll, str):
                #print('going to jail')
                player.position = 10
                
            else:
                player.position = (player.position + roll)%40

                if player.position == 30:
                    #print('going to jail')
                    player.position = 10


                elif player.position in [2, 17, 33]:
                    chest_played = current_chest.pop(0)
                    if len(current_chest)==0:
                        current_chest = [i for i in chest_options]
                        rd.shuffle(current_chest)
                    #print(chest_played)

                    if isinstance(chest_played, int):
                        player.position = chest_played
                        
                elif player.position in [7, 22, 36]:
                    chance_played = current_chance.pop(0)
                    if len(current_chance)==0:
                        current_chance = [i for i in chance_options]
                        rd.shuffle(current_chance)
                    #print(chance_played)

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

            
            if player.position == 10 and jail:
                player.jail = 1
                jail_time += 1
                #print("player is in jail")

                
            turns += 1
        games_completed += 1
        if games_completed%1000 == 0:
            print("game",games_completed, "finished")
    return properties_list



def calc_time(games, numturns):
    simulation = simple_simulation(games, numturns, jail=True)
    names =[location.name for location in simulation]
    numbers = [location.location for location in simulation]
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
    locations =[location.name for location in simulation]
    numbers = [location.location for location in simulation]
    hits = [location.hits for location in simulation]
    hits_percentage= [(hit/(games*numturns))*100 for hit in hits]
    fig, ax = mpl.subplots()
    rects = ax.bar(numbers, hits_percentage, color = 'r')
    ax.set_ylabel('Percentage Chance of Hitting Space')
    ax.set_title('Percentage Chance of Hitting Each Space ({} Games at {} Turns/Game)'.format(games, numturns))
    ax.set_xticks(numbers)
    ax.set_xticklabels(locations, rotation = 90)
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
        if y_value < 0:
            space *= -1
            va = 'top'
        label = "{:.2f}".format(y_value)
        mpl.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va=va)
        
##
##def clac_hit_colors(simulation, games=1, numturns=1):
##    seen = set()
##    colours = [obj.colour for obj in simulation if obj.colour not in seen and not seen.add(obj.colour)]
##    answer = []
##    for colour in colours:
##        newlist = []
##        for thing in simulation:
##            if thing.colour == colour:
##                newlist.append(thing)
##        answer.append(newlist)
##    hits = [location.hits for location in simulation]    
##    hits_percentage= [(hit/(games*numturns))*100 for hit in hits]
##    

def compare_hits_time(games, numturns):
    hits = calc_hit(games, numturns)
    turns = calc_time(games, numturns)
    locations = [location.name for location in Property.properties]
    fig, ax = mpl.subplots()
    numbers = np.arange(40)
    width= 0.35
    rects = ax.bar(numbers, hits, width, color = 'r')
    rects2 = ax.bar(numbers + width, turns, width, color = 'y')
    ax.set_ylabel('Percentage')
    ax.set_title('Comparison Between Percentage of Time Spent and Percentage Chance of Hitting Each Square ({} Games at {} Turns/Game)'.format(games, numturns))
    ax.set_xticks(numbers + width / 2)
    ax.set_xticklabels(locations, rotation = 90)
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50)
    ax.legend((rects[0], rects2[0]), ('Hits', 'Turns'))
    mpl.tight_layout()

compare_hits_time(100,100)                 





mpl.show()    


        

    

