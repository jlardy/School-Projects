import random
import math
import pandas
import sys

# The idea of this program is to simulate at a most basic level agents living on a landscape and harvesting
# some sort of resource from that landscape. Agents are given a vision and have the ability to move to a 
# new location on the landscape that is within their vision. 


def query_yes_no(question, default="yes"):
    # Ask a yes/no question via raw_input() and return their answer.

    # "question" is a string that is presented to the user.
    # "default" is the presumed answer if the user just hits <Enter>.
    #     It must be "yes" (the default), "no" or None (meaning
    #     an answer is required of the user).

    # The "answer" return value is True for "yes" or False for "no".
    
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def checkInt(message):
    # function to check if an input from a user is an integer and is above 0.
    while True:
        iterations = input(message.strip() + ' ')
        try: 
            num = int(iterations)
            if num > 0:
                return num
            else:
                print('Integer must be larger than 0.')
        except:
            print('Please enter an integer.')
  
class latticeNode:
    # This class is used to create a node that contains a random amount of sugar between 0 and 4. Coords is a tuple that represents (x,y) and is only
    # used for the visualization. 
    def __init__(self, coords):
        self.sugar = random.randint(0, 4)
        self.coords = coords
    def decrement(self):
        self.sugar = 0      
    def regrow(self):
        # increase by one
        if self.sugar < 4:
            self.sugar += 1

class lattice:
    # This class is used to create a landscape of nodes each containing a random amount of sugar. The nodes are created with coords centered around 
    # (50,50).
    def __init__(self, n):
        self.lattice = []
        self.createCircleNodes(n)
    def regrow(self):
        # regrows all of the nodes that are in the lattice
        for node in self.lattice:
            node.regrow()
    def createCircleNodes(self, n):
        # creates n amount of node objects with an x, y centered around 50,50 with a radius of 50
        centerX = 50
        centerY = 50
        radius = 50
        s = 2 * math.pi / n
        for i in range(n):
            angle = s * i
            newX = int(centerX + radius * math.cos(angle))
            newY = int(centerY + radius * math.sin(angle))
            self.lattice.append(latticeNode((newX, newY))) 

class agent:
    # Represents an agent that will be placed on a landscape. They are created with an initial vision that they can see on the landscape 
    # and a position on the landscape. 
    def __init__(self, pos):
        self.pos = pos
        self.vision = random.randint(15, 30)

class model:
    # Model class creates n(numSites) latticsNode objects for a landscape stored in self.landscape and creates n(numAgents) agent objects stored in
    # self.agentArray. After an instance of the model class is initiated, the user will be prompted if they would like to have contiguous agents. If 
    # the user responds yes, then all of the agents will be created in one contiguous line on the landscape. If the user answers no, the agents will 
    # be intitated at random locations on the landscape. The user will then be asked if they would like to use visualization, if they answer yes, 
    # the model will create a pygame window and show an animation of the agents after each movement phase of the model. If the user choses no 
    # visualization, the model will then ask the user for a number of iterations to run the model for. The model will then run, calculating the amount
    # of sugar in each node of the landscape and moving agents to the location on the landscape with the highest sugar value. After each moement phase, 
    # the model prints to the screen all of the groups of contiguous agents. After reaching the number of iterations input by the user, the model will 
    # then print to the screen the average number of groups, the average group size, and the largest group that was formed throughout the entire run. 
    #     
    def __init__(self, numSites, numAgents, iterations=0, contig=False, vis=False):
        # store a lattice object in the models landscape 
        self.landscape = lattice(numSites)
        self.agentArray = []

        contig = query_yes_no('Would you contiguous agents?')
        vis = query_yes_no('Would you like to use the visualization?')

        if contig:
            # if user wants all agents initiated next to each other the flag contig is set to true
            for i in range(numAgents):
                self.agentArray.append(agent(i))
        else:
            # generate random positions along the length of the lanscape, then store them in agentArray 
            tempPositions = []
            for _ in range(numAgents):
                position = None
                while position in tempPositions or position == None:
                    position = random.randint(0, numSites-1)
                tempPositions.append(position)
                self.agentArray.append(agent(position))
        # calculate the landscape after it was initiated 
        self.calculateSugar()

        if vis:
            self.visualization()
        else:    
            iterations = checkInt('How many iterations would you like?')
            self.run(iterations)

    def moveAgents(self):
        # method moves agents forward to a new position within their vision that is not already occupied and has a higher sugar value than the 
        # currently occupied lanscape node. If all of the sites within an agents vision are occupied or do not have a higher sugar value, the agent
        # will stay in the same spot  

        # create a list the length of the agents and shuffle it to loop through the agents at random 
        r = list(range(len(self.agentArray)))
        random.shuffle(r)
        for i in r:
            # outer loop is for each agent in the array
            currentAgent = self.agentArray[i]
            newPos = currentAgent.pos
            # currently occupied positions
            occupied = self.getCurrentPositions()
            for j in range(currentAgent.vision):
                # inner loop is for all of the sites within the current agents vision 
                nextPos = (currentAgent.pos + (j+1)) % len(self.landscape.lattice)
                # if the next position has more sugar and it's not already occupied, then set the new position to the next postion
                if self.landscape.lattice[newPos].sugar < self.landscape.lattice[nextPos].sugar and nextPos not in occupied:
                    newPos = nextPos
            # assign the agent it's new postion
            currentAgent.pos = newPos

    def getCurrentPositions(self):
        # returns a list of occupied sites
        occupied = []
        for agent in self.agentArray:
            occupied.append(agent.pos)
        return occupied

    def calculateSugar(self):
        # regrow all the sites not occupied by agents and set the sugar of occupied sites to 0
        self.landscape.regrow()
        for agent in self.agentArray:
            self.landscape.lattice[agent.pos].decrement()
        
    def calculateGroups(self, prt=False):
        # method returns a list of groups 

        # get the positions of the agents 
        endPositions = self.getCurrentPositions()
        # initialize a list of 0's the size of the landscape 
        endLanscape = [0 for i in range(len(self.landscape.lattice))]
        # set all occupied sites equal to one 
        for pos in endPositions:
            endLanscape[pos] = 1
        groups = []
        counter = 0
        # if the landscape has an agent at the begining and end of the list, set the loops variabel to true
        if endLanscape[0] and endLanscape[-1]:
            loops = True
        else:
            loops = False

        for i in range(len(endLanscape)):
            if i == len(endLanscape)-1 and loops:
                # if the lanscape has an agent at the beginning and end, add the group from the end to the first group 
                counter += 1
                groups[0] += counter

            if endLanscape[i] and endLanscape[(i+1)%len(endLanscape)]:
                # if the current position and the next position are occupied, add one to the counter 
                counter += 1
            elif endLanscape[i] and not endLanscape[(i+1)%len(endLanscape)]:
                # if the current position is occupied and the next one is not, add one to the counter, append the group to groups,
                # and reset the counter
                counter += 1
                groups.append(counter)
                counter = 0
        if prt:
            # for debugging, shows what the current lanscape looks like by printing the agent locations on the landscape, the sugar amounts
            # the landscape, and how many agents are in each group. 
            print('Sugar Amounts')
            self.printSugarAmounts()
            print('\n')
            print('Agent Locations')
            print(endLanscape)
            print('\n')
            print('Groups')        
            print(groups)
            print('\n')
            print('='*100)
        return groups

    def run(self, runs):
        # method runs the model by calling the calculateSugar and moveAgents methods for an input number of iterations. 
        # On the last iteration, the method prints to the screen where teh agents are located on the lanscape, the sugar 
        # ammounts for each position on the landscape, the average number of groups throughout the run of the model, the biggest 
        # group that was formed, and the average group size. 
        averageNumGroups = 0
        maxGroup = 0
        avgGroupSize = 0

        for _ in range(runs-1):
            # iterate the number of times input - 1
            # update the sugar amounts on the landscape
            self.calculateSugar()
            # move agents forward
            self.moveAgents()
            # get the group sizes
            data = self.calculateGroups()
            # print all the groups for each run
            print(data)
            if max(data) > maxGroup:
                # update the max value
                maxGroup = max(data)
            # update the averages 
            avgGroupSize += sum(data)/len(data)
            averageNumGroups += len(data)
        
        # run the model one more time and print the averages, where the agents are located on the landscape and the sugar amounts
        # for each node on the landscape
        self.calculateSugar()
        self.moveAgents()
        data = self.calculateGroups(prt=True)
        if max(data) > maxGroup:
            maxGroup = max(data)
        avgGroupSize += sum(data)/len(data)
        averageNumGroups += len(data)

        print('Average Number of Groups:', averageNumGroups/runs)
        print('Average Group Size:', avgGroupSize/runs)
        print('Maximum Group Formed:', maxGroup)

    def printSugarAmounts(self):
        # method just prints a list of the numer of sugar in each location of the landscape
        data = []
        for node in self.landscape.lattice:
            data.append(node.sugar)
        print(data)

    def visualization(self):
        # using pygame to create a visualization for the model. Draws the landscape in a ring shape and shows the location of the agents on 
        # the landscape and the amount of sugar that is stored in each node. Also shows the current largest group, the number of groups and  
        # the average vision of all of the agents. 

        # pylint: disable=no-member

        # calculate the average vision of the agents
        avgVision = 0
        for agent in self.agentArray:
            avgVision += agent.vision
        avgVision = avgVision / len(self.agentArray)

        import pygame as pg
        # pygame setup 
        pg.init()
        screen = pg.display.set_mode([750, 750])
        width = 600
        height = 600
        counter = 0
        clock = pg.time.Clock()
        running = True
        # colors for the landscap nodes
        white = (255,255,255)
        c1 = (178,255,102)
        c2 = (128,255,0)
        c3 = (76,153,0)
        c4 = (25,51,0)
        font = pg.font.SysFont("comicsansms", 24)
        agentVis = font.render("Average Agent Vision:" + str(avgVision), True, (0, 128, 0))
        while running:
            clock.tick(1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False           

            screen.fill(white)
            data = self.calculateGroups()
            # show the current information about the model 
            maxGroup = font.render("Current Largest Group:" + str(max(data)), True, (0, 128, 0))
            numGroups = font.render("Number of Groups:" + str(len(data)), True, (0, 128, 0))
            iteration = font.render("Current Iteration:" + str(counter), True, (0, 128, 0))
            screen.blit(agentVis, (350 - agentVis.get_width() // 2, 410 - agentVis.get_height() // 2))
            screen.blit(maxGroup, (350 - maxGroup.get_width() // 2, 375 - maxGroup.get_height() // 2))
            screen.blit(numGroups, (350 - numGroups.get_width() // 2, 340 - numGroups.get_height() // 2))
            screen.blit(iteration, (350 - iteration.get_width() // 2, 450 - iteration.get_height() // 2))

            # assign the of each node based on sugar status. Red denotes an agent
            for node in self.landscape.lattice:
                if node.sugar == 0:
                    node.color = (255,0,0)
                elif node.sugar == 1:
                    node.color = c1
                elif node.sugar == 2:
                    node.color = c2
                elif node.sugar == 3:
                    node.color = c3
                else:
                    node.color = c4

            # draw all of the nodes of the landscape based on their color and position. 
            for node in self.landscape.lattice:
                pg.draw.circle(screen, node.color, (int(((node.coords[0]+10) / 100) * width), int(height - (((node.coords[1]-10) / 100) * height))), 4)
            
            # step the model forward
            self.calculateSugar()
            self.moveAgents()
            pg.display.flip()
            counter += 1
        pg.quit()


runModel = model(numSites=150, numAgents=40)
