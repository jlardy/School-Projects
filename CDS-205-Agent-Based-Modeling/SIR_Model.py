import random
import math
import matplotlib
import matplotlib.pyplot as plt
import pandas

# Basic idea of this program is to show a disease spreading across a random social network 
# Creates a random social network from the graph class, then spreads a disease across that
# netowrk. The disease is given a specific probability of spreading. On each period of the 
# model running, each agent has that probabilty of spreading the disease to one of the 
# connections on their social network. The model runs until there are no longer any sick
# agents on the social network. 

class agent:
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]
        self.edges = []
    
    # checks the probabilty that each edge will break and re-connect to another agent
    def checkLinks(self, p, agentsArray):
        for i in range(len(self.edges)):
            if random.random() < p:
                self.edges[i] = agentsArray[random.randint(0, len(agentsArray)-1)]

class graph:
    # To use this class pass in N, Deg, Prob and it will create a random network (based on the prob) of veritces and edges
    # stored in agents array. The program loops through N agents and tests the Prob that each of agents edges(Deg)
    # will break and attach to another agent. This can be iterated if you pass in an integer 
    # to the iterations parameter of the graph class. Optional parameters include plot and 
    # plotOriginal, and randAllign. If set to True, plot will plot all the agents as a blue dot and draw their 
    # edges after the model has been run and edges reattached to other random agents. plotOriginal 
    # shows the origial lattice that is created before the model is run. If randAllign is set to true,
    # the agents will have random x and y coordinates, otherwise they will be plotted in a circle.
    def __init__(self, n, deg, prob, iterations=1, plot=False, plotOriginal=False, randomAlign=False):
        self.agents = []

        # agents will be plotted in a circle unless otherwise specified
        if randomAlign:
            self.createRandomAllignAgents(n)
        else:
            self.createCircleAgents(n)

        # connect all the edges of each agent 
        self.connectEdges(deg)
        
        if plotOriginal:
            self.showLattice('Before Running')
        
        # iterate if specified 
        for _ in range(iterations):
            # check the edges of each agent
            for agent in self.agents:
                agent.checkLinks(prob, self.agents)
        
        if plot:
            self.showLattice('After Running')
        
        if plot or plotOriginal:
            plt.show()

    def createCircleAgents(self, numAgents):
        # creates numAgents amount of agent objects with an x, y centered around 50,50 with a radius of 50
        # after it creates the agents it also ties together the number of edges defined by deg
        centerX = 50
        centerY = 50
        radius = 50
        s = 2 * math.pi / numAgents
        for i in range(numAgents):
            angle = s * i
            newX = int(centerX + radius * math.cos(angle))
            newY = int(centerY + radius * math.sin(angle))
            self.agents.append(agent((newX, newY))) 
    
    def createRandomAllignAgents(self, numAgents):
        # creates n randomly alligned agents and sorts the array based off of the x coord to connect edges later
        for _ in range(numAgents):
            self.agents.append(agent((random.randint(0,100), random.randint(0,100))))
        self.agents.sort(key=lambda x:x.x)

    def connectEdges(self, deg):
        # logic for creating edges to the left and right of current, 
        # if there is an odd degree input 
        # the extra edge will always go to the right
        # check if odd 
        remain_deg = deg % 2
        for i in range(len(self.agents)):
            outer = 0
            for j in range(1, int((deg - remain_deg)/2)+1):
                outer = j
                self.agents[i].edges.append(self.agents[i-j])
                self.agents[i].edges.append(self.agents[(i+j)%len(self.agents)])
            
            # if the degree is odd, always go to the right for the remainder
            if remain_deg:
                self.agents[i].edges.append(self.agents[(i+outer+1)%len(self.agents)])
    
    def showLattice(self, titleTxt):
        # function to plot the vertices and edges of the graph, pass in a title 
        fig, ax = plt.subplots()
        for agent in self.agents:
            ax.plot(agent.x, agent.y, 'bo', markersize=6)
            for edge in agent.edges:
                x_vals = [edge.x, agent.x]
                y_vals = [edge.y, agent.y]
                ax.plot(x_vals, y_vals)

        ax.set(xlabel='X', ylabel='Y', title=titleTxt)
        ax.grid()

class disease: 
    # To use this class pass in the following variables to run:
    #  
    # numSick == the number of agents that start out on the graph designated as sick 
    # numVaccinated == the number of agents that are vaccinated and have no chance of getting sick or passing the disease
    # infectivity == the probabilty that the disease spreads from a sick agent to a healthy agent must be between 0 and 1
    # t == the amount of time that an agent is sick for 
    # n == number of agents to be placed on the network 
    # deg == the number of connections (edges) each agent has 
    # prob == the chance that when the graph is created that an edge will break and attach to another random agent
    # randAllign == if this is set to true the agents will be randomly alligned across with no forseeable meaning, otherwise they will be in a circle 
    # animatedPlot == this is a seperate mode for the program to run in. In this mode the program will show each interaction between every 
    # agent until the model converges at a state where there are no longer any sick agents.  
    #  
    #  
    # The model runs on the __init__ phase of the class and will produce a matplotlib line graph showing how many agents ended up in each state. 
    # The 4 states that are defined for agents are: H = healthy, S = infected/sick, R = recovered, V = vaccinated. The model will run until it reaches 
    # a state where there are no longer any sick people  

    def __init__(self, numSick, numVaccinated, infectivity, t, n, deg, prob, animatePlot=False, randAllign=False):
        self.network = graph(n, deg, prob, randomAlign=randAllign) 
        self.infectivity = infectivity 
        self.data = {'Sick':[numSick], 'Healthy':[n-numVaccinated-numSick], 'Recovered':[0], 'Vaccinated':[numVaccinated]}
        # all agents originally healthy
        for agent in self.network.agents:
            agent.state = 'H'
            agent.timer = t

        # holding values for which agents are assigned a certain value 
        tempValues = []
        position = None
        # create initial sick agents
        for _ in range(numSick):
            position = None
            while position in tempValues or position == None:
                position = random.randint(0, len(self.network.agents)-1)
            tempValues.append(position)
            self.network.agents[position].state = 'S'
        # create vaccinated agents
        for _ in range(numVaccinated):
            position = None
            while position in tempValues or position == None:
                position = random.randint(0, len(self.network.agents)-1)
            tempValues.append(position)
            self.network.agents[position].state = 'V'
        
        if animatePlot:
            # This mode steps the model forward one iteration each clock tick. Every clock tick there is one agent being compared
            # to another with a red line drawn between the two. 
            # Clock speed is based off of cpu power, if you hit enter the program will use all of your cpu power to animate.
            try:
                speed = int(input('Enter a clock speed for pygame to run: '))
                print('Clock speed:', speed)
            except:
                speed = 0
                print('Clock speed: Full')
            self.livePlot(speed)
        else:
            self.spread() 
            self.plotData(n, numSick, numVaccinated, infectivity, t)              

    def interact(self):
        # Interacting stage of the model, each agent interacts with one of its connections. If the agent is sick or the agent it interacts with is sick
        # based off the probabilty input into the infectivity of the model either agent will become sick.
        for agent in self.network.agents:
            # choose one of the edges of current agent at random
            interactAgent = agent.edges[random.randint(0, len(agent.edges)-1)]
            
            # if current agent is healthy and interacts with a sick agent
            if agent.state == 'H' and interactAgent.state == 'S':
                if random.random() < self.infectivity:
                    agent.state = 'S'

            # see if the agent heals before interacting with another
            if agent.state == 'S':
                agent.timer -= 1
                if agent.timer == 0:
                    agent.state = 'R'
                                
            # if the current agent is sick and interacts with a healthy agent
            if agent.state == 'S' and interactAgent.state == 'H':
                if random.random() < self.infectivity:
                    interactAgent.state = 'S'
    
    def plotData(self, n, numSick, numVaccinated, infectivity, t, plotNetwork=False):
        # Uses the data from each run of the model that is stored in a dictionary to create a pandas dataframe and uses matplotlib to blot a line
        # graph of all of the data.
        df = pandas.DataFrame(self.data)
        df.plot(kind='line')
        plt.title('N = ' + str(n) + ', S = ' + str(numSick) + ', V = ' + str(numVaccinated) + ', I = ' + str(infectivity) + ', T = ' + str(t))
        plt.ylabel('Total of Population')
        plt.xlabel('Time (ticks)')
        
        if plotNetwork:
            self.network.showLattice('Original Network')
        plt.show()
          
    def spread(self):
        # Method that calls the interact method until the model converges at a state where there are no longer any sick agents
        # For every iteration, it stores the number of agents in each state in the varible called data
        S = None
        H = None
        R = None
        V = None
        while True:
            if S == 0:
                print('Healthy:', H, 'Sick:', S, 'Recovered:', R, 'Vaccinated:', V)
                break
            S = 0
            H = 0
            R = 0
            V = 0
            self.interact()
            for agent in self.network.agents:
                if agent.state == 'S':
                    S += 1
                if agent.state == 'R':
                    R += 1
                if agent.state == 'H':
                    H += 1 
                if agent.state == 'V':
                    V += 1
            self.data['Sick'].append(S)
            self.data['Healthy'].append(H)
            self.data['Recovered'].append(R)
            self.data['Vaccinated'].append(V)
    
    def livePlot(self, speed):
        # pylint: disable=no-member
        # This method shows the idea of the interact and spread methods
        import pygame as pg
        pg.init()
        screen = pg.display.set_mode([750, 750])
        width = 600
        height = 600
        clock = pg.time.Clock()
        running = True
        index = -1
        end = len(self.network.agents)-1

        while running:
            clock.tick(speed)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False           
            sick = 0
            screen.fill((255, 255, 255))
            # assign the color for each agent and count sick agents
            for agent in self.network.agents:
                if agent.state == 'S':
                    agent.color = (255, 0, 0)
                    sick += 1
                if agent.state == 'R':
                   agent.color = (0,255,0)
                if agent.state == 'H':
                    agent.color = (0,0,255) 
                if agent.state == 'V':
                    agent.color = (0,0,0)
            # draw edges at the bottom level 
            for agent in self.network.agents:
                for edge in agent.edges:
                    pg.draw.line(screen, (0,0,0), (int(((agent.x+10) / 100) * width), int(height - (((agent.y-10) / 100) * height))), (int(((edge.x+10) / 100) * width), int(height - (((edge.y-10) / 100) * height))))

            # draw vertices on top of lines
            for agent in self.network.agents:
                pg.draw.circle(screen, agent.color, (int(((agent.x+10) / 100) * width), int(height - (((agent.y-10) / 100) * height))), 4)
            # used to loop through for the interact phase
            if index == end:
                index = 0
            else:
                index += 1
            # only animate the interaction phase if there are still sick agents
            if sick != 0:
                # interaction phase
                agent = self.network.agents[index]
                # choose one of the edges of current agent at random
                interactAgent = agent.edges[random.randint(0, len(agent.edges)-1)]
                # if current agent is healthy and interacts with a sick agent
                if agent.state == 'H' and interactAgent.state == 'S':
                    if random.random() < self.infectivity:
                        agent.state = 'S'
                # see if the agent heals before interacting with another
                if agent.state == 'S':
                    agent.timer -= 1
                    if agent.timer == 0:
                        agent.state = 'R'
                # if the current agent is sick and interacts with a healthy agent
                if agent.state == 'S' and interactAgent.state == 'H':
                    if random.random() < self.infectivity:
                        interactAgent.state = 'S'
                # draw the line of the agent interacting in red
                pg.draw.line(screen, (255,0,0), (int(((agent.x+10) / 100) * width), int(height - (((agent.y-10) / 100) * height))), (int(((interactAgent.x+10) / 100) * width), int(height - (((interactAgent.y-10) / 100) * height))), 3)
            
            pg.display.flip()
        pg.quit()

# Runs the model with different scenarios where there are either vaccinated agents or not with two different 
# diseases. 
# ===========================================================================================================
# no vaccinated on a lattice
model = disease(numSick=5, numVaccinated=0, infectivity=.3, t=4, n=100, deg=2, prob=0, animatePlot=False)
model = disease(numSick=5, numVaccinated=0, infectivity=.6, t=8, n=100, deg=2, prob=0, animatePlot=False)
# vaccinated on a lattice
model = disease(numSick=5, numVaccinated=5, infectivity=.3, t=4, n=100, deg=2, prob=0, animatePlot=False)
model = disease(numSick=5, numVaccinated=10, infectivity=.6, t=8, n=100, deg=2, prob=0, animatePlot=False)

# ===========================================================================================================
# no vaccinated on a semi lattice
model = disease(numSick=5, numVaccinated=0, infectivity=.3, t=4, n=100, deg=2, prob=.5, animatePlot=False)
model = disease(numSick=5, numVaccinated=0, infectivity=.6, t=8, n=100, deg=2, prob=.5, animatePlot=False)
# vaccinated on a semi lattice
model = disease(numSick=5, numVaccinated=5, infectivity=.3, t=4, n=100, deg=2, prob=.5, animatePlot=False)
model = disease(numSick=5, numVaccinated=30, infectivity=.6, t=8, n=100, deg=2, prob=.5, animatePlot=False)

# ===========================================================================================================
# no vaccinated on a small world graph 
model = disease(numSick=5, numVaccinated=0, infectivity=.3, t=4, n=100, deg=2, prob=1, animatePlot=False)
model = disease(numSick=5, numVaccinated=0, infectivity=.6, t=8, n=100, deg=2, prob=1, animatePlot=False)
# vaccinated on a small world graph 
model = disease(numSick=5, numVaccinated=5, infectivity=.3, t=4, n=100, deg=2, prob=1, animatePlot=False)
model = disease(numSick=5, numVaccinated=60, infectivity=.6, t=8, n=100, deg=2, prob=1, animatePlot=False)
# ===========================================================================================================