from pacman import Pacman
from constants import *
from vector import Vector2
from math import e, sqrt
from random import choice, uniform, shuffle
from sys import exit
import itertools

class AnneallingPacman(Pacman):
    def __init__(self, node, nodegroup, pelletGroup):
        self.nodeGroup = nodegroup
        self.pelletGroup = pelletGroup
        Pacman.__init__(self, node)
        self.run()
    
    def run(self):
        self.queue = self.simulatedAnnealling()
        

    def simulatedAnnealling(self):
        #create nodeList
        self.targetNodes = []
        for pellet in self.pelletGroup.pelletList:
            self.targetNodes.append(self.nodeGroup.getNodeFromPixels(pellet.position.x, pellet.position.y))
        
        self.LUT = {}    
        #generate all possible 2 node paths
        self.LUT = self.generateLUT()
        
        # -- create StartSpace
        startSpace = [0,1,2,3,4,5,6,7,8,9]
        shuffle(startSpace)
        
        # -- create solution variables
        currentSpace = startSpace
        currentCost = self.generateSolutionCost(currentSpace)
        testSpace = []
        testCost = 0
        spacesTested = 0
        
        # -- pick inputs
        self.temp = 3628800/100
        alpha = 1
        finalTemp = 0
        iterationPerTemp = 10
        
        print("starting loop")
        
        # -- main While
        while(not self.isTerminationCriteriaMet(finalTemp)):
            for i in range(iterationPerTemp):
                neighbors = self.generateSpaces(currentSpace)
                #neighbors = list(itertools.permutations(currentSpace))
                #print("testing")
                testSpace = choice(neighbors)
                testCost = self.generateSolutionCost(testSpace)
                deltaCost = currentCost - testCost
                
                probability = self.getProbability(deltaCost)
                
                
                
                if deltaCost >= 0:
                    currentSpace = testSpace
                    currentCost = testCost
                    #print("Test Space Won")
                elif uniform(0,1) < probability:
                    #print("swapping")
                    currentSpace = testSpace
                    currentCost = testCost
                    
                #spacesTested = spacesTested+1
                
            self.temp = self.tempReduction(alpha)
            if self.temp % 10000 == 0:
                print(self.temp)
        
        
        
        print("winning space: " + str(currentSpace))
        print("winning weight: "+ str(currentCost))
        return self.convertSpaceToPath(currentSpace)
    
    def convertSpaceToPath(self, space):
        queue = []
        queue.extend(self.LUT[(self.node, self.targetNodes[space[0]])])
        for i in range(len(space)-1):
            startNode = self.targetNodes[space[i]]
            stopNode = self.targetNodes[space[i+1]]
            queue.extend(self.LUT[(startNode, stopNode)])        
        return queue
            
    def isTerminationCriteriaMet(self, finalTemp):
        return self.temp <= finalTemp
        
    def getProbability(self, deltaC):
        power = deltaC/self.temp
        power = power
        return e ** (power)
        
    def tempReduction(self, alpha):
        return self.temp - alpha
        #return self.temp * self.alpha
        #return temp/(1+3*temp) 
        
        
    def generateSolutionCost(self, space):
        cost = len(self.LUT[(self.node, self.targetNodes[space[0]])])
        for i in range(len(space)-1):
            startNode = self.targetNodes[space[i]]
            stopNode = self.targetNodes[space[i+1]]
            cost = cost + len(self.LUT[(startNode, stopNode)])        
        return cost
    
    def generateSpaces(self, givenSpace):
        spaces = []
        temp=[]
        
        for i in range(len(givenSpace)):
            for j in range(len(givenSpace)):
                if i != j:
                    tempSpace = givenSpace.copy()
                    tempSpace[i], tempSpace[j] = tempSpace[j], tempSpace[i]
                    spaces.append(tempSpace)
                    
        for x in spaces:
            if x not in temp:
                temp.append(x)
   
        return temp
      
    def generateLUT(self):
        tempLUT = {}
        smth = self.node
        for node in self.targetNodes:
            tempLUT[(smth, node)] = self.aStar(smth, node)
            for nodeDestination in self.targetNodes:
                if node is not nodeDestination:
                    tempLUT[(node, nodeDestination)] = self.aStar(node, nodeDestination)
        
        return tempLUT
    
    
    
    
    
    
    
    
    
    
    
    
        
    def aStar(self,startNode, goalNode):
        aStarQueue = self.graphSearcher(startNode,goalNode)
        if aStarQueue is None:
            print("error, cound not find path")
            exit()
        aStarQueue.pop(0)
        return aStarQueue
    
    def graphSearcher(self, startNode, goalNode):
        queue = []
        weights = []
        self.explored = []
        self.parents = {}
        queue.append(startNode)
        weights.append(0)
        while queue:
            node = None
            while node is None:
                node = queue.pop(weights.index(min(weights)))
            weights.pop(weights.index(min(weights)))
            if node is goalNode:
                return self.givePath(startNode, goalNode)
            self.explored.append(node)
            
            for v in node.neighbors.values():
                if node.neighbors[PORTAL] is not None and node.neighbors[PORTAL] not in self.explored:
                    v = node.neighbors[PORTAL]
                if v not in queue and v not in self.explored and v is not None:
                    queue.append(v)
                    weight = self.getWeight(node, v, goalNode)
                    weights.append(weight)
                    self.parents[v] = node
                if v in queue:
                    weight = self.getWeight(node, v, goalNode)
                    if weights[queue.index(v)] > weight:
                        indexOfInterest = queue.index(v)
                        queue[indexOfInterest] = v
                        weights[indexOfInterest] = weight
        
        return None
                    
    def getWeight(self, node, v, goalNode):
        return sum(Vector2.asInt(node.position-v.position)) + self.getDistance(node, goalNode)
    
    def getDistance(self, node, v):
        vec = node.position - v.position
        return sqrt(vec.magnitudeSquared())

    def givePath(self, start, finish):
        stack = []
        if len(self.parents) < 1:
            return []
        
        first, last = finish, self.parents[finish]
        while last is not start:
            stack.append(first)
            first, last = last, self.parents[last]
        stack.append(first)
        stack.append(last)
        
        queue = []
        while stack:
            queue.append(stack.pop())
        return queue      

    def getDirection(self):
        directionIndex = list(self.node.neighbors.values()).index(self.target)
        direction = list(self.node.neighbors.keys())[directionIndex]
        return direction


    def update(self, dt):	
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.direction
        
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
               
            if self.queue:
                self.target = self.queue.pop(0)
            else:
                self.target = self.node
            print(self.target.position/16)
            
            if self.target is not self.node:
                # get the direction of the target
                self.direction = self.getDirection()

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()



    