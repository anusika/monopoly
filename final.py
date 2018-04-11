import numpy as np #used to generate lists for matplotlib axis labeling
import random as rd #used to generate random numbers for dice rolling and player's chance of buying property
import matplotlib.pyplot as mpl #used to generate graphs from data
from statistics import mean #used to average out list of lists when analyzing how much money player has made in a game

#set up Player class and various attributes
class Player(object):
    def __init__(self, number, risky, locations, monies, completed, wins = 0, position = 0, money = 1500,
                 jail = False, jail_time = 0, turn = False, turns = 0 ):
        self.number = number #for complex simulation it is easier to undestand who's turn it is by having player numbers
        self.position = position #track where player is on the board, initally set to 0 which is Go
        self.money = money #for complex simulation, track how much money the player currently has
        self.locations = locations #for complex simulation, track which properties the player owns
        self.risky = risky/100 #for complex simulation, player has a risky factor such as 70% which
                                #is then converted into decimal (risky is the percentage chance of that player buying a spot)
        self.jail = jail #boolean that tracks if player is in jail
        self.jail_time = jail_time #tracks how long player is in jail
        self.turn = turn #for complex simulation, boolean that tracks if it is this player's turn
        self.wins = wins #for complex simulation, tracks how many games player has won
        self.monies = monies #for complex simulation, will be a list of lists, each list is one game's worth of tracking player's amount of money
        self.turns = turns #for complex simulation and debugging, tracks how many turns player has taken
        self.completed = completed #for complex simulation, will be a list of lists that contains all the player.monies lists generated in multiple games
    def want(self, location): #for complex simulation, see if player wants to buy this location
        testing = rd.random() #some random number between 0 and 1
        if self.money < location.buy: #if the player has less money than the price of the location i.e they cannot afford the location
            return False #they do not want to buy it
        elif testing <= self.risky: #if the random number is less than the risk factor of the player
            return True # they want to buy the property ex) if a player is 70% (they will buy 70% of properties) if the random number is less than 0.7 they want to buy it
        else: #if the random number is greater than the risky factor
            return False #the player does not want the property

#set up Property class and various attributes
class Property(object):
    properties = [] #creating master list of all properties
    def __init__(self, name, location, colour = 'Null', buy = 'null', rent = 'null', hits = 0, owned = False):
        Property.properties.append(self) #add property to master list of all properties
        self.name = name #stores full name of property as a string, makes graphs prettier to have full names of properties
        self.location = location #sets where the property is supposed to be on the board
        self.colour = colour #sets colour of property, 'null' is default value for spaces without colours,
                            #utilities and railroads have their own colour ('Utility' and 'Station' respectivly)
        self.buy = buy #for complex simulation, set price to buy property
        self.rent = rent #for complex simulation, set rent if other player lands on this spot
        self.hits = hits #tracks how many times a player has be on this spot
        self.owned = owned #for complex simulation, boolean that tracks if property is owned or not
    def __str__(self): #if I want to print this property I want this sentence to appear
        return "Name: {} || Location: {} || Colour: {} || Buy: {} || Rent: {}".format(self.name,
                                                self.location, self.colour,self.buy,self.rent)  #.format inserts the phrases related to this property into the {}


#creating all properties in Monopoly for all simulations-----------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#creating function for simulating dice rolls
def RollDice(player, jail):#takes in two arguments: the player and jail, if jail is true that means that the player will have to roll doubles to get out of jail
    doubles = 0 #if a player rolls 3 doubles they have to go to jail, so this tracks how many doubles have happened
    total = 0 #if a player rolls a double they get to roll again, so we need to track the sum of all their rolls
    while doubles < 3:
        dice1 = rd.randint(1,6) #choose a number between 1 and 6 (inclusive) to count as first dice
        dice2 = rd.randint(1,6) #because players roll two dice, we repeat the process
        roll = dice1 + dice2 #the current roll is the sum of the dice
        if dice1 == dice2: #if the roll is a double
            doubles += 1 #doubles count is increased by one
            total += roll #total sum is increased by roll
            if player.jail and jail: #if player is in jail and jail is active
                player.jail = False #the player is now out of jail
                return[total, player.jail] #return the total sum and the change in player.jail
        else:
            if player.jail and jail: #if player is in jail and jail is active
                return 'jail' #because the player did not roll doubles they are still stuck in jail
            else:
                total += roll #total sum is increased by roll
                return total #becuase they did not roll a double they cannot roll again, return the total sum
    if doubles == 3: #if a player has rolled doubles three times
        return 'jail' #the player must go to jail

#creating simple simulation; it's basically just one player moving around the board
def simple_simulation(numgames, numturns, jail): #takes in three arguments, the number of games, the number of turns per game, and if jail is acitve or not (boolean)
    properties_list = Property.properties #create list that includes all the properties we made earlier
    for place in properties_list: #when running the simulation multiple times I have to clear the hits for each spot
        place.hits = 0
    railroads = [] #create a empty list that will be filled by all properties that are railroads
    utilities = [] #create a empty list that will be filled by all properties that are utilites
    for place in properties_list: #cycle through all properties in properties_list
        if place.colour == 'Station': #if the property is a station
            railroads.append(place) #add it to the list of railroads
        elif place.colour == 'Utility': #if the property is a utility
            utilities.append(place) #add it to the list of utilities

    railroads_location = [railroad.location for railroad in railroads] #create a list of the numerical locations of each railroad
    utilities_location = [utility.location for utility in utilities] #create a list of the numerical locations of each utility

    games_completed = 0 #set inital amount of games completed to 0
    while games_completed < numgames: #while the amount of games completed is less than the amount of games asked for

        player = Player(1, 0, 'null', 'null', 'null') #create a new player, the player does not need any of the attributes set for complex simulations
                                            #the only used attributes will be player.position, player.turns, player.jail, player.jail_time

        #creating all the options for community chest cards, numbers are locations that the player can be sent to, becuase this is a simple simulation
        #the money cards are ignored and 'n' is used as a placeholder
        chest_options = [0, 10, 'n' 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
        current_chest = [card for card in chest_options] #create a chest that will be used for this game, as cards are removed from this game
                                                        #in case the chest becomes empty we need a master chest which is chest_options
        rd.shuffle(current_chest) #shuffle the chest

        # creating all the options  for chance cards, numbers are locations that the player can be sent to, 'back' is when the player is sent
        # back three spaces, 'utility' is when player is sent to nearest utility, 'railroad' is when player is sent to nearest railroad,
        # 'n' is again used as a placeholder for money related cards
        chance_options = [0, 24, 11, 10, 5, 39, 'back', 'utility', 'railroad', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
        current_chance = [card for card in chance_options]#create a chance cards bin that will be used for this game, as cards are removed from this game
                                                        #in case the bin becomes empty we need a master chest which is chest_options
        rd.shuffle(current_chance) #shuffle the chest

        turns_completed = 0 #set inital amount of turns completed to 0
    
        while turns_completed < numturns: #while the amount of turns completed is less than the amount of turns asked fo

            roll = RollDice(player, jail) #roll the dice at the beginning of the turn

            if player.jail and player.jail_time == 3 and jail: #if the player is in jail and they have been in jail for three turns and jail is active
                player.jail = False #the player must leave jail
                player.jail_time = 0 #the amount of time the player has spent in jail is reset to 0

            elif isinstance(roll, list): #if the RollDice function returns a list, is is only because the player has rolled doubles to get out of jail
                player.jail = False #the player gets to leave jail
                player.jail_time = 0 #the amount of time the player has spent in jail is reset to 0

            elif isinstance(roll, str): # if the RollDice function returns a string, it is only because the player either is being sent to jail or is continuing to be in jail
                player.position = 10 #send the player to jail which is at postion 10
                if jail: #if jail is active
                    player.jail = True #the player is now stuck in jail
                    player.jail_time += 1 #the amount of time the player has spent in jail has increased by 1

            else: #basically if the roll was just a normal int and the player was not in jail
                player.position = (player.position + roll)%40 #move the player forward by roll spaces the %40 means that if you end up with a number greater than 40
                                                            #for example at space 35, rolled a 6, take the remainder (1) and that is the player's new spot

                if player.position == 30: #if the player is on the spot 'Go to Jail'
                    player.position = 10 #send the player to jail
                    if jail: #if jail is active
                        player.jail = True #the player is now stuck in jail
                        player.jail_time += 1 #the amount of time the player has spent in jail has increased by 1

                elif player.position in [2, 17, 33]: #if the player is on a community chest spot
                    chest_played = current_chest.pop(0) #the chest card played is the first card in the current_chest and is removed from the chest
                    if len(current_chest) == 0: #if the chest is empty
                        current_chest = [card for card in chest_options] #refill the chest with the cards from the master chest
                        rd.shuffle(current_chest) #shuffle the refilled chest

                    if chest_played == 10: #if the chest card send the player to jail
                        player.position = 10 #move the player to the jail spot
                        if jail: #if jail is active
                            player.jail = True #the player is now stuck in jail
                            player.jail_time += 1 #the amount of time the player has spent in jail has increased by 1

                    elif isinstance(chest_played, int): #if the chest card played is an int
                        player.position = chest_played #move the player to that int

                    else:
                        pass #if the chest card was just 'n' move on

                elif player.position in [7, 22, 36]: #if the player is on a chance spot
                    chance_played = current_chance.pop(0) #the chance card played is the first card in the current_chance and is removed from the bin
                    if len(current_chance) == 0: #if the chest is empty
                        current_chance = [card for card in chance_options] #refill the bin with the cards from the master chance
                        rd.shuffle(current_chance) #shuffle the refilled bin

                    if chance_played == 10: #if the chance card send the player to jail
                        player.position = 10 #move the player to the jail spot
                        if jail: #if jail is active
                            player.jail = True #the player is now stuck in jail
                            player.jail_time += 1 #the amount of time the player has spent in jail has increased by 1

                    elif isinstance(chance_played, int): #if the chance card played is an int
                        player.position = chance_played #move the player to that int

                    elif chance_played == 'back': #chance card sends player back 3 places
                        player.position = player.position-3 #don't need to %40 bc there's no chance spot on the board that's 3 away from Go

                    elif chance_played == 'utility': #chance card sends player to nearest utility
                        while player.position not in utilities_location: #while the numerical location of the player does not match any of the locations in utilities_location
                            player.position = (player.position + 1)%40 #move the player forward one space
                            #repeat this process until the player is on a utility

                    elif chance_played == 'railroad':#chance card sends player to nearest railroad
                        while player.position not in railroads_location:#while the numerical location of the player does not match any of the locations in railroads_location
                            player.position = (player.position + 1)%40#move the player forward one space
                            #repeat this process until the player is on a railroad

                    else:
                        pass #if the chance card was just 'n' move on

            
            properties_list[player.position].hits += 1 #find the property that the player is on in the properties_list and increase the amount of hits it has by 1
            player.turns += 1 #increase player.turns by one
            turns_completed += 1 #increase completed turns by 1
            #test to make sure player is getting the right amount of turns
            if player.turns != turns_completed: #raises error is player.turns does not equal completed_turns
                print('error')

            
        games_completed += 1 #increase completed games by 1

        #keep track of games_completed when completing thousands of turns to get most accurate data
        if games_completed%1000 == 0: #for every one thousand games
            print('game', games_completed, 'finished')
    return properties_list #return properties_list which not contains all the properties with their updated amount of hits


#time to graph all the cool results we got!
#so in my report I talk about the difference between the chance of hitting any one spot and the amount of turns spent on that square (mostly speaking about the jail spot)

#these two lists are used in the graphs:
names = [location.name for location in Property.properties] #creates a list of the names of the properties which will be displayed as a label for their respective y-value
numbers = np.arange(40) #create a list that is 40 spots long for the x-axis

#this first function calculates how many turns are spent on each space
def calc_time(games, numturns):#takes in two arguments, how many games to run and how many turns per game
    simulation = simple_simulation(games, numturns, jail = True) #run a simple simulation with the specified amount of turns and games,
                                                                #jail is True so we can see the affect of spending turns spent in jail
    turns = [location.hits for location in simulation] #creating a list that contains how many turns were spent at each spot
    turns_percentage = [(turn/(games*numturns)*100) for turn in turns] #list that contains the percentage of turns spent in each spot
                                                                        #turns is amount of hits, (games*numturns) tells you the total amount of turns
    fig, ax = mpl.subplots() #start a plot for the data
    bars = ax.bar(numbers, turns_percentage, color = 'y') #plot each turn_percentage using numbers as the x-value, make the color of the bar yellow
    ax.set_ylabel('Percentage of Turns Spent') #label y-axis
    ax.set_title('Percentage of Turns Spent at Each Space ({} Games at {} Turns/Game)'.format(games, numturns)) #set title of graph formating the title with amount of games and turns
    ax.set_xticks(numbers) #make a vertical line at each x value
    ax.set_xticklabels(names, rotation = 90) #labels each bar with its name rotated vertically
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50) #label x-axis and move the label down
    bars = ax.patches #basically convert each bar into a rectangular shape to label
    label_bars(bars) #using the label_bars function label each bar
    return turns_percentage #when comparing data later I returned the turns_percentage list because I will use it in later graphs


#this function is label_bars which labels each individual bar in the bar graph
def label_bars(bars):
    for rect in bars: #for each bar
        y_value = rect.get_height() #get the height of the bar
        x_value = rect.get_x() + rect.get_width() / 2 #because we want the label centered, find the middle of the width of the bar
        space = 5 #move the label about 5 up
        va = 'bottom' #means that whenever the variable va is used, it will mean from the bottom
        label = "{:.2f}".format(y_value) #the label should take the y-value and print it to 2 decimal places
        mpl.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va=va) #creating the actual label using the specifications above



#this function calcuates the chance of hitting any one spot
def calc_hit(games, numturns): #takes in two arguments, how many games to run and how many turns per game
    simulation = simple_simulation(games, numturns, jail=False) #run a simple simulation with the specified amount of turns and games,
                                                                #jail is False so we can see only see the chance of a player being moved to this spot
    hits = [location.hits for location in simulation]#creating a list that contains how many times the player was sent to each spot
    hits_percentage= [(hit/(games*numturns))*100 for hit in hits] #list that contains the percentage of turns spent in each spot
                                                                        #hit is amount of hits, (games*numturns) tells you the total amount of turns
    fig, ax = mpl.subplots() #start a plot for the data
    bars = ax.bar(numbers, hits_percentage, color = 'r') #plot each hits_percentage using numbers as the x-value, make the color of the bar red
    ax.set_ylabel('Percentage Chance of Hitting Space') #label y-axis
    ax.set_title('Percentage Chance of Hitting Each Space ({} Games at {} Turns/Game)'.format(games, numturns)) #set title of graph formating the title with amount of games and turns
    ax.set_xticks(numbers)  #make a vertical line at each x value
    ax.set_xticklabels(names, rotation = 90) #labels each bar with its name rotated vertically
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50) #label x-axis and move the label down
    bars = ax.patches#basically convert each bar into a rectangular shape to label
    label_bars(bars) #using the label_bars function label each bar
    return hits_percentage #when comparing data later I returned the hits_percentage list because I will use it in later graphs

#this function graphs the hit_percentage against the turns_percentage so we can see the bars side by side
def compare_hits_time(games, numturns): #takes in two arguments, how many games to run and how many turns per game
    hits = calc_hit(games, numturns) #calculates hit_percentage
    turns = calc_time(games, numturns)#calcuates turns_percentage
    fig, ax = mpl.subplots() #start a plot for the data
    width= 0.35 #sets width of each bar
    bars_hits = ax.bar(numbers, hits, width, color = 'r') #plots hit_percentage with red bars
    bars_turns = ax.bar(numbers + width, turns, width, color = 'y') #plots turn_percentage with yellow bars beside the hit_percentage bars by adding the width
    ax.set_ylabel('Percentage') #label y-axis
    ax.set_title('Comparison Between Percentage of Time Spent and Percentage Chance of Hitting Each Square ({} Games at {} Turns/Game)'.format(games, numturns)) #set title of graph formating the title with amount of games and turns
    ax.set_xticks(numbers + width / 2) #make a vertical line at each x value inbetween the two bars for each space
    ax.set_xticklabels(names, rotation = 90)#labels each pair of bars with its spot name rotated vertically
    ax.set_xlabel('Spaces on Monopoly Board', labelpad=50) #label x-axis and move the label down
    ax.legend((bars_hits[0], bars_turns[0]), ('Chance of Hit Percentage', 'Turns Spent Percentage')) #create a legend for the two different bar types

def calc_colours(games, numturns):
    simulation = simple_simulation(games, numturns, jail=True)
    seen = set()
    unique = [obj.colour for obj in simulation if obj.colour not in seen and not seen.add(obj.colour)]
    colouring = []
    for colour in unique:
        colouring.append(0)
    for properties in simulation:
        position = unique.index(properties.colour)
        colouring[position] += properties.hits
    colouring = [colour/(games*numturns)*100 for colour in colouring]
    numbers = np.arange(len(unique))
    printing_colours = ['#cdc9c9', 'brown', '#cdc9c9', '#cdc9c9', '#cdc9c9', '#add8e6', 'pink', '#cdc9c9', 'orange', 'red', 'yellow', 'green', 'blue']
    fig, ax = mpl.subplots()
    bars = ax.bar(numbers, colouring, color = printing_colours) 
    ax.set_xticks(numbers)
    ax.set_xticklabels(unique)
    ax.set_ylabel('Percentage')
    ax.set_title(' Percentage Chance of Hitting Each Colour ({} Games at {} Turns/Game)'.format(games, numturns))
    ax.set_xlabel('Colours on Monopoly Board', labelpad=50)
    bars = ax.patches
    label_bars(bars)
    

calc_colours(10000, 100)
mpl.tight_layout()
mpl.show()    

#time for the complex simulation
#the main differences are that this one includes multiple players and the exchange of money
#however, it lacks adding houses and hotels, a goal I have made for my next assigments
#for this complex simulation I will only be commenting on the changes and improvements I have made compared to the simple simulation

def complicated_simulation(games, numturns, players): #still takes in 3 arguments however, becuase jail is always True I don't need to add it, players is a list of players
    properties_list = Property.properties
    for place in properties_list:
        place.hits = 0
        
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

    while games_completed < games:
        
        #for the community chest I have added the options for gaining and losing money, there are still 3 cards that are outside the scope of this project
        chest_options = [0, 10, 'rerror', 'tdoctor', 'ropera','rfund', 'thospital', 'rinsurance',  'rincome', 'rbirthday','tschool', 'rconsult','rinherit', 'rsecond',  'n', 'n', 'n']
        current_chest = [card for card in chest_options]
        rd.shuffle(current_chest)

        #for the chance carrds I have added the options for gaining and losing money, there are still 3 cards that are outside the scope of this project
        chance_options = [0, 24, 11, 10, 5, 39, 'back', 'ulility', 'railroad', 'rbank', 'tpoor', 'tplayer', 'rloans', 'rcrossword', 'n', 'n', 'n']
        current_chance = [card for card in chance_options]
        rd.shuffle(current_chance)

        completed_turns = 0

        for player in players: #like clearing the properties_list in the simple situtation I have to clear the player attributes as well
            player.monies = [] #creating a clean list to track player's money change for new game
            player.locations = [] #reset how many properties player has
            player.money = 1500 #reset amount of money player has at beginning of game
        
        while completed_turns < numturns:
            
            for player in players: #repeat the process for a turn for each player in the list of players
                
                player.turn = True #change the status of player.turn to True to state that this is the active player
 
                roll = RollDice(player, jail = True)

                if player.jail and player.jail_time == 3:
                    player.jail = False
                    player.jail_time = 0
                    player.money -= 50 #becuase this is the player's third turn in jail they must leave and lose $50

                    
                elif isinstance(roll, list):
                    player.jail = False
                    player.jail_time = 0


                elif isinstance(roll, str):
                    player.position = 10
                    player.jail = True
                    player.jail_time += 1
                    
                else:
                    player.position = (player.position + roll)%40

                    if player.position == 30:
                        player.position = 10
                        player.jail = True
                        player.jail_time += 1
                        

                    elif player.position in [2, 17, 33]:
                        chest_played = current_chest.pop(0)
                        if len(current_chest)==0:
                            current_chest = [card for card in chest_options]
                            rd.shuffle(current_chest)
                            
                        if chest_played == 10:
                            player.position = 10
                            player.jail = True 
                            player.jail_time += 1 
                        

                        elif isinstance(chest_played, int):
                            player.position = chest_played

                        #for the next cases based off the community chest card the player will either lose or gain a certain amount of money
                            
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

                        elif chest_played == 'rbirthday': #this is a special card where each opponent pays the active player $10 for their birthday
                            for opponent in players: #cycle through each player
                                if opponent.turn == False: #if they are not the active player
                                    opponent.money -= 10 #they lose $10
                                    player.money += 10 #the active player gains $10


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
                        if len(current_chance)==0:
                            current_chance = [i for i in chance_options]
                            rd.shuffle(current_chance)

                        if chance_played == 10:
                            player.position = 10
                            player.jail = True 
                            player.jail_time += 1 
                        
                        elif isinstance(chance_played, int):
                            player.position = chance_played
                            if player.position in [24, 11, 5, 39]:
                                player.money += 200 #because the player will pass go they will gain $200
                            
                        elif chance_played == 'back':
                            player.position = player.position-3 

                        elif chance_played == 'ultility':
                            while player.position not in utilities_location:
                                player.position = (player.position + 1)%40
                                

                        elif chance_played == 'railroad':
                            while player.position not in railroads_location:
                                player.position = (player.position + 1)%40

                        #for the next cases based off the chance card the player will either lose or gain a certain amount of money
                        elif chance_played == 'rbank':
                            player.money += 50
                                
                        elif chance_played == 'tpoor':
                            player.money -= 15

                        elif chance_played == 'tplayer': #in this case the active player has to pay each opponent $50
                            for opponent in players: #cycle through each player
                                if opponent.turn == False: # if they are not the active player
                                    opponent.money += 50 #they gain $50
                                    player.money-= 50 #the active player loses $50


                        elif chance_played == 'rloans':
                            player.money += 150

                        elif chance_played == 'rcrossword':
                            player.money += 100
                            
                        else:
                            pass


                #becuase I'll be using the term 'properties_list[player.position]' a lot I just assigned it to a variable
                current = properties_list[player.position]
                current.hits += 1 #increase the amount of hits on this spot by 1

                #this section involves buying property           
                if current.owned == False and current.buy != 'null': #if the spot in not currently owned and it does not have 'null' as it's price
                    if player.want(properties_list[player.position]): #see if the player wants the property
                        player.money -= current.buy #subtract the cost of the property from player.money
                        current.owned = True #change the status of the property to owned
                        player.locations.append(current) #add the property to the player's list of owned properties
                    else: #they don't want the property
                        pass #do nothing

                #this section involves paying rent
                    
                if properties_list[player.position].owned == True and properties_list[player.position] not in player.locations: #if the property is owned and it is not owned by the active player
    
                    #utilities have a seperate way of paying rent: 4*roll if one utility is owned and 10*roll if both are owned
                    if current.colour == "Utility": #check if the property is a utility
                        owned_utilities = 0 #set inital amount of owned utilities to 0
                        for opp in players: #cycle through players
                            if current in opp.locations: #if the current location is in their locations 
                                for location in opp.locations: #loop through all their owned properties
                                    if location in utilities: #if that property is in the list of utilities
                                        owned_utilities +=1 # increase the amount of owned utilties by 1
                                    else: #if not in utilties
                                        pass # do nothing
                                    
                                if owned_utilities == 1: #if the player only owns one utility
                                    player.money -= (4*roll) #the active player has to pay 4*roll (4 times their dice roll)
                                    opp.money += (4*roll) #the owning player gains that amount of money
                                elif owned_utilities == 2: #if the player owns both utilities
                                    player.money -= (10*roll) #the active player has to pay 10*roll (10 times their dice roll)
                                    opp.money += (10*roll) #the owning player gains that amount of money
                                else:
                                    pass

                                

                    #railroads have a seperate way of paying rent:  $25 if one is owned, $50 if two, $100 if three and $200 if all four 
                    elif current.colour == "Station": #check if the property is a station
                        owned_stations = 0 #set inital amount of owned stations to 0
                        for opp in players: #cycle through players
                            if current in opp.locations: #if the current location is in their locations 
                                for location in opp.locations: #loop through all their owned properites
                                    if location in railroads: #if that property is in the list of railroads
                                        owned_stations +=1 # increase the amount of owned railroads by 1
                                    else: #if not in utilties
                                        pass # do nothing
                                    
                                if owned_stations == 1: #if the player only owns one railroad
                                    player.money -= 25 #the active player loses $25
                                    opp.money +=25 #the owning player gains that amount of money
                                elif owned_stations == 2: #if the player only two railroad
                                    player.money -= 50 #the active player loses $50
                                    opp.money +=50 #the owning player gains that amount of money
                                elif owned_stations == 3: #if the player only three railroad
                                    player.money -= 100 #the active player loses $100
                                    opp.money +=100 #the owning player gains that amount of money
                                elif owned_stations == 4: #if the player only all four railroad
                                    player.money -= 200 #the active player loses $200
                                    opp.money +=200 #the owning player gains that amount of money


                                  
                    else: #if the property is not a utility or a railroad
                        player.money -= current.rent #the active player loses the rent amount of money

                        #find player to pay
                        for opp in players: #cycle through players
                            if current in opp.locations: #if the current location is in the player's list of locations
                                opp.money += current.rent #that player gains the rent amount of money
                            else: #the player does not own this property
                                pass # do nothing
                        
                # if player is on Go they get $200
                if player.position == 0:
                    player.money += 200


                   
                player.monies.append(player.money)  #see how much money the player has left at the end of their turn and add it to the list player.monies
                player.turn = False # the player is no longer the active player
                player.turns += 1 # the player has now completed one turn
                
            completed_turns += 1 # all players have completed one more turn
            
        money = [player.money for player in players] #at the end of the game create a list with the amount of money each player has left
        
        for player in players: #cycle through all players
            if player.money == max(money): #if that player has the maximum number of money in the list money this means they are the winner
                player.wins += 1 #their win count increases by 1
        
        games_completed += 1

        for player in players:
            player.completed.append(player.monies) #add list of tracking money to master list that contains all games worth of tracking 
            
        if games_completed%100 == 0:
            print("game",games_completed, "finished")

        
    
    #at the end of all the games      
    for player in players: #cycle through all the players
        print('player:', player.number, 'wins', player.wins, 'turns:',player.turns) #print their number and how many games they won

    return properties_list, players

player1 = Player(1, 70, [], [], [])
player2 = Player(2, 50, [], [], [])
player3 = Player(3, 100, [], [], [])
player4 = Player(4, 20, [], [], [])
player5 = Player(5, 50, [], [], [])
players = [player1, player2, player3, player4]
                     
def calc_monies(games, numturns, list_of_players):
    simulation = complicated_simulation(games, numturns, list_of_players)
    playered = simulation[1]
    n = np.arange(numturns)
    lines = []
    average = []
    for player in playered:
        averaged = [float(sum(col))/len(col) for col in zip(*player.completed)]
        average.append(averaged)
    for player in playered:
        mpl.plot(n,average[player.number-1], label = 'Player {} Risky: {}'.format(player.number, player.risky*100))
    mpl.legend()

def compare_win(games, numturns, list_of_players):
    simulation = complicated_simulation(games, numturns, list_of_players)
    wins = [player.wins for player in simulation[1]]
    players = ['Player {}'.format(player.number) for player in simulation[1]]
    number = np.arange(len(players))
    fig, ax = mpl.subplots() #start a plot for the data
    bars = ax.bar(number, wins, color = 'y') 
    ax.set_ylabel('Amount of Games Won') #label y-axis
    ax.set_title('Affect of turn order ({} Games at {} Turns/Game with {} Players, Each Having Same Risk Factor)'.format(games, numturns, len(players))) #set title of graph formating the title with amount of games and turns
    ax.set_xticks(number) #make a vertical line at each x value
    ax.set_xticklabels(players) 
    ax.set_xlabel('Player', labelpad=50) #label x-axis and move the label down
    bars = ax.patches #basically convert each bar into a rectangular shape to label
    label_bars(bars) #using the label_bars function label each bar

def compare_win_risky(games, numturns, list_of_players):
    simulation = complicated_simulation(games, numturns, list_of_players)
    wins = [player.wins for player in simulation[1]]
    players = ['Player {} Risky {}'.format(player.number, player.risky*100) for player in simulation[1]]
    number = np.arange(len(players))
    fig, ax = mpl.subplots() #start a plot for the data
    bars = ax.bar(number, wins, color = 'y') 
    ax.set_ylabel('Amount of Games Won') #label y-axis
    ax.set_title('Affect of turn order ({} Games at {} Turns/Game with {} Players, Each Having Different Risk Factor)'.format(games, numturns, len(players))) #set title of graph formating the title with amount of games and turns
    ax.set_xticks(number) #make a vertical line at each x value
    ax.set_xticklabels(players) 
    ax.set_xlabel('Player', labelpad=50) #label x-axis and move the label down
    bars = ax.patches #basically convert each bar into a rectangular shape to label
    label_bars(bars) #using the label_bars function label each bar



