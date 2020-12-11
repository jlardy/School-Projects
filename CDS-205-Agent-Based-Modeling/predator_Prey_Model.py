import random
import math
import pandas as pd
import matplotlib.pyplot as plt
  
class landscapeNode:
    # This class is used to create a node that contains a random amount of sugar between 0 and 4. Coords is a tuple that represents (x,y) and is only
    # used for the visualization. 
    def __init__(self):
        self.sugar = random.randint(0, 4)
    def regrow(self):
        # increase by one to a cap of 4
        if self.sugar < 4:
            self.sugar += 1

class landscape:
    # This class is used to hold all of the landscape nodes, thus creating the environment that agents act upon
    def __init__(self, n):
        self.lattice = []
        # create n landscape nodes
        for _ in range(n):
            self.lattice.append(landscapeNode())
    def regrow(self):
        # regrows all of the nodes that are in the lattice
        for node in self.lattice:
            node.regrow()

class agent:
    # This class is used to create an agent. The type of the agent defines whether they are a predator ('w' = wolf) or prey ('r' = rabbit). 
    def __init__(self, pos, index, anType):
        self.pos = pos # position on landscape
        self.index = index # position in agent array
        self.anType = anType #type of animal 
        self.hunger = random.randint(1, 4) # endowed with a random amount of hunger
        
        # if the animal is a rabbit, they are given a higher vision allowing them to move further each iteration
        if self.anType == 'r':
            self.vision = random.randint(15, 30) # how far the agent can see
        else:
            self.vision = random.randint(1,10) # how far the agent can see

    def feed(self, food):
        # feeds to a max hunger of 4
        self.hunger += food
        if self.anType == 'r':
            if self.hunger > 4:
                self.hunger = 4 
        else:
            if self.hunger > 4:
                self.hunger = 4

class model:
    def __init__(self, numSites, numRabbits, numWolfs, iterations=0, contig=False, vis=False):
        # store a lattice object in the models landscape 
        self.landscape = landscape(numSites)
        self.agentArray = []
        self.numSites = numSites

        # generate random positions along the length of the lanscape, then store them in agentArray 
        agentPositions = random.sample(range(0, len(self.landscape.lattice)-1), numRabbits+numWolfs)
        
        # generate rabbits and wolves at random locations on the landscape
        for i, pos in enumerate(agentPositions):
            if i < numRabbits:
                self.agentArray.append(agent(pos, i, 'r'))
            else: 
                self.agentArray.append(agent(pos, i, 'w'))

    def moveAgents(self):
        # holding for killed rabits
        toKill = []
        
        # regow sugar before moving agents
        self.landscape.regrow()

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
                
                if currentAgent.anType == 'r':
                    # if the next position has more sugar and it's not already occupied, then set the new position to the next postion
                    if self.landscape.lattice[newPos].sugar < self.landscape.lattice[nextPos].sugar and nextPos not in occupied:
                        newPos = nextPos
                
                elif currentAgent.anType == 'w':
                    # if the next position is an occupied spot by a rabbit 
                    if nextPos in occupied and self.agentArray[occupied.index(nextPos)].anType == 'r' and occupied.index(nextPos) not in toKill:
                        newPos = nextPos

            if currentAgent.anType == 'r':
                # assign the agent it's new postion
                currentAgent.pos = newPos
                # set the sugar of the new position = to 0 and add the sugar to the agents hunger
                currentAgent.feed(self.landscape.lattice[newPos].sugar) 
                self.landscape.lattice[newPos].sugar = 0
            else:
                # if the agent didn't select a new position, go to the next agent
                if currentAgent.pos == newPos:
                    continue
                # get the index of the agent that will be killed and move the current agent there
                index = occupied.index(newPos)
                currentAgent.pos = newPos
                # add the agent to be killed list to the toKill list and feed the current agent to max hunger
                toKill.append(index)
                currentAgent.feed(4)
        # kill all of the agents that were eaten 
        self.killAgents(toKill)

    def checkAgents(self):
        # CALL THIS BEFORE MOVING AGENTS 

        # only go into the reproductive phase if the agent array is less than the total landscape 
        if len(self.agentArray) < self.numSites:
            # each agent has a certain probability to reproduce each cycle 
            # NOTE: typically the rabbits need to be a 3:1 or 4:1 reproductive cycle for the model to be stable
            # When rabbits reproduce too quickly, it makes the wolf population increase too sharply thus killing the majority 
            # of the rabbits out and kills off the wolf population. 


            for agent in self.agentArray:
                # check the probabilty that a rabbit reproduces and that its hunger is above 2
                if agent.anType == 'r' and random.random() < .6 and agent.hunger > 2:
                    self.reproduce(agent)
                # check the probabilty that a wolf reproduces and that its hunger is above 2
                if agent.anType == 'w' and random.random() < .2 and agent.hunger > 2:
                    self.reproduce(agent)

                
        # decrement hunger by two, build a list of agents to be killed if they starve out 
        toKill = []
        # make sure the index of the agents are current
        for i, agent in enumerate(self.agentArray):
            agent.index = i

        # decrement each agents hunger 
        for agent in self.agentArray:
            if agent.anType == 'r':
                agent.hunger -= 2
            else:
                agent.hunger -= 1
            # check if the agent starves
            if agent.hunger <= 0:
                toKill.append(agent.index)
        
        # kill the agents that starved 
        self.killAgents(toKill)


    def reproduce(self, inAgent):
        # check if the landscape is full or not
        if len(self.agentArray) < self.numSites:
            
            # cost of reproduction for the agent that is reproducing
            inAgent.hunger -= 1
            
            # routine for spawning a new agent on an unoccupied space
            occupied = self.getCurrentPositions()
            newpos = None
            while newpos is None or newpos in occupied:
                newpos = random.randint(0, len(self.landscape.lattice)-1)
            self.agentArray.append(agent(newpos, len(self.agentArray), inAgent.anType))
        
    def killAgents(self, agentList):
        # sort the kill list in reverse order and remove them one by one from the agent array
        agentList.sort(reverse=True)
        for i in agentList:
            self.agentArray.pop(i)
        # update indexes of agents
        for i, agent in enumerate(self.agentArray):
            agent.index = i

    def getCurrentPositions(self):
        # returns a list of occupied sites
        occupied = []
        for agent in self.agentArray:
            occupied.append(agent.pos)
        return occupied

    def getCounts(self, data, sugar=False):
        # updates data, needs to be a dictionary passed in with at least two columns 'r' and 'w'
        counts = [0,0,0]
        # count the number of wolves and bunnies in the array 
        for agent in self.agentArray:
            if agent.anType == 'r':
                counts[0] += 1
            else:
                counts[1] += 1
        # if sugar is true, you must pass in a dictionary with a 
        if sugar:
            for node in self.landscape.lattice:
                counts[2] += node.sugar
            counts[2] = counts[2]/4
            data['Grass'].append(counts[2])
        
        data['Rabbits'].append(counts[0])
        data['Wolves'].append(counts[1])
        return data
        
    def run(self, iterations, sugar=False):
        # sugar is set to true to collect data on the landscapes sugar amounts
        if sugar:
            data = {'Rabbits':[], 'Wolves':[], 'Grass':[]}
        else:
            data = {'Rabbits':[], 'Wolves':[]}
     
        self.getCounts(data, sugar=sugar)

        # check agents states, move them and collect data 
        for _ in range(iterations):
            self.checkAgents()
            self.moveAgents()
            self.getCounts(data, sugar=sugar)
        return data


def averageRun(numRuns, numRabbits, numWolves, landscapeSize, time, sugar=False):
# Helper function for the model, creates an average of the number of runs with model criteria, shows a line plot of the data 
    dfList = []
    for _ in range(numRuns):
        test = model(landscapeSize, numRabbits, numWolves)
        dfList.append(pd.DataFrame(data=test.run(time, sugar=sugar)))

    # concatenate all the dataframes and averages them
    out = pd.concat(dfList).groupby(level=0).mean()
    out['Average Rabbits: ' + str(round(out['Rabbits'].mean()))] = out['Rabbits'].mean()
    out['Average Wolves: ' + str(round(out['Wolves'].mean()))] = out['Wolves'].mean()
    ax = out.plot(kind='line', ylim=(0,test.numSites))
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Sites')
    plt.show()  



averageRun(numRuns=1, numRabbits=100, numWolves=50, landscapeSize=2000, time=200, sugar=True)