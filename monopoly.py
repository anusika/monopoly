import time
import numpy as np
import random as rd
import pylab
import math


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
    def __init__(self, name, location, colour = "null", buy = "null", rent="null", hits = 0):
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

go = Property( 'Go', 0)
mediterranean = Property('Mediterranean Avenue', 1, 'brown', 60, 2)
chest1 = Property('Coummunity Chest 1', 2, 'surprise')
baltic = Property('Baltic Avenue',3, 'brown', 60, 4)
income = Property('Income', 4, 'tax')
reading = Property('Reading Railroad', 5, 'station', 200, 25)
oriental = Property('Oriental Avenue', 6, 'lightblue', 100, 6)
chance1 = Property('Chance 1', 7, 'surprise')
vermont= Property('Vermont Avenue',8, 'lightblue', 100, 6)
connecticut = Property('Connecticut Avenue', 9, 'lightblue', 120, 8)
jail = Property('Jail/Just Visting', 10)
charles = Property('St.Charles Place', 11, 'pink', 140, 10)
electric = Property('Electric Company', 12, 'utility', 150, 'roll')
states = Property('States Avenue', 13, 'pink', 140, 10)
virginia = Property('Virginia Avenue', 14, 'pink', 160, 12)
penn_railroad = Property('Pennsylvania Railroad', 15, 'station', 200, 25)
james = Property('St.James Place',16, 'orange', 180, 14)
chest2 = Property('Chest 2', 17, 'surprise')
tennessee = Property('Tennessee Avenue',18, 'orange', 180, 14)
york = Property('New York Avenue', 19, 'orange', 200, 16)
free = Property('Free Parking', 20)
kentucky = Property('Kentucky Avenue', 21, 'red', 220, 18)
chance2 = Property('Chance 2', 22, 'surprise')
indiana = Property('Indiana Avenue', 23, 'red', 220, 18)
illinois = Property('Illinois Avenue', 24, 'red', 240, 20)
bo = Property('B and O Railroad', 25, 'station', 200, 25)
atlantic = Property('Atlantic Avenue', 26, 'yellow', 260, 22)
ventnor = Property('Strand Avenue', 27, 'yellow', 260, 22)
water = Property('Water Works', 28, 'utility', 150, 'roll')
marvin = Property('Marvin Gardens', 29, 'yellow', 280, 24)
gojail = Property('Go To Jail', 30, 'jail')
pacific = Property('Pacific Avenue', 31, 'green', 300, 26)
carolina = Property('North Carolina Avenue', 32, 'green', 300, 26)
chest3 = Property('Community Chest 3', 33, 'surprise')
pennsylvania= Property('Pennsylvania Avenue', 34, 'green', 320, 28)
shortline = Property('Short Line', 35, 'station', 200, 25)
chance3 = Property('Chance 3', 36, 'surprise')
park = Property('Park Place', 37, 'blue', 350, 35)
tax = Property('Tax', 38, 'tax')
boardwalk = Property('BoardWalk', 39, 'blue', 400, 50)

chance_options = [0, 10, 24, 5, 'back', 'thouse', 'tstreet', 'tschool', 'tcharge', 'tspeeding',
                  'rbuilding', 'rcrossword', 'rbank']
chest_options = [0, 19, 10, 'thospital', 'tdoctor', 'tinsurance', 'rerror',
                 'rannuity', 'rinherit', 'rstock', 'rinterest', 'rincome',
                 'rsecond', 'birthday',]



def RollDice():
    doubles = 0
    total = 0
    while doubles < 3:
        dice1 = rd.randint(1,6)
        dice2 = rd.randint(1,6)
        roll = dice1 + dice2
        #print(dice1, dice2, roll)
        if dice1 == dice2:
            doubles += 1
            total += roll
            #print("doubles total:", total)
        else:
            total += roll
            #print('total:', total)
            return total
    if doubles == 3:
        return 'jail'

        
        

    
def simple_simulation(numgames, numturns):
    properties_list = Property.properties
    games_completed = 0
    railroads = []
    utilities = []
    for place in properties_list:
        if place.colour == 'station':
            railroads.append(place)
        elif place.colour == 'utility':
            utilities.append(place)
    railroads_location = [railroad.location for railroad in railroads]
    utilities_location = [utility.location for utility in utilities]

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

            while turns < numturns:
                roll = RollDice()
                                    
                if isinstance(roll, str):
                    print('going to jail')
                    player.position = 10
                    
                else:
                    player.position = (player.position + roll)%40

                    if player.position == 30:
                        print('going to jail')
                        player.position = 10


                    elif player.position in [2, 17, 33]:
                        chest_played = current_chest.pop(0)
                        if len(current_chest)==0:
                            current_chest = [i for i in chest_options]
                            rd.shuffle(current_chest)
                        print(chest_played)

                        if isinstance(chest_played, int):
                            player.position = chest_played
                            
                    elif player.position in [7, 22, 36]:
                        chance_played = current_chance.pop(0)
                        if len(current_chance)==0:
                            current_chance = [i for i in chance_options]
                            rd.shuffle(current_chance)
                        print(chance_played)

                        if isinstance(chance_played, int):
                            player.position = chance_played
                            
                        elif chance_played == 'back':
                            print('moving back')
                            player.position = player.position-3 #don't need to %40 bc there's no chance spot on the board that's 3 away from go

                        elif chance_played == 'ultility':
                            print('moving to utility')
                            while player.position not in utilities_locations:
                                player.position = (player.position + 1)%40
                                

                        elif chance_played == 'railroad':
                            print('moving to raildroad')
                            while player.position not in railroads_locations:
                                player.position = (player.position + 1)%40
                            
                        else:
                            pass

                properties_list[player.position].hits += 1
                print("Name:", properties_list[player.position].name, "times hit:", properties_list[player.position].hits)
                if player.position == 10:
                    player.jail = 1
                        
                turns += 1
            games_completed += 1
            print("game",games_completed, "finished")

            
simple_simulation(1, 100)






    
        

    

