import random
import math
import matplotlib
import matplotlib.pyplot as plt
import pandas

# To use this program, create an instance of the graph class and pass in N, Deg, Prob
# The program loops through N agents and tests the Prob that each of agents edges(Deg)
# will break and attach to another agent. This can be iterated if you pass in an integer 
# to the iterations parameter of the graph class. Optional parameters include plot and 
# plotOriginal, and randAllign. If set to True, plot will plot all the agents as a blue dot and draw their 
# edges after the model has been run and edges reattached to other random agents. plotOriginal 
# shows the origial lattice that is created before the model is run. If randAllign is set to true,
# the agents will have random x and y coordinates, otherwise they will be plotted in a circle.

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
        # creates numAgents amount of agent objects with an x, y centered around 0,0 with a radius of 100
        # after it creates the agents it also ties together the number of edges defined by deg
        centerX = 0
        centerY = 0
        radius = 100
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

test = graph(100, 2, .2, plot=True)
