from py import process
from ghost import Ghost
from constants import *
from vector import Vector2
from nodes import NodeGroup

class UCSGhost(Ghost):
    def __init__(self, node, nodes, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.direction = STOP
        self.nodes = nodes
        self.queue = []
        
    def uniformCostSearch(self,startNode, goalNode):
        self.queue = self.graphSearcher(startNode,goalNode)
        if len(self.queue) < 1:
            directions = self.validDirections()
            self.queue.append(self.node.neighbors[self.randomDirection(directions)])
        else:
            self.queue.pop(0)
            self.target = self.queue.pop(0)
            self.direction = self.getDirection()
    
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
                    weight = self.getWeight(node, v)
                    weights.append(weight)
                    self.parents[v] = node
                if v in queue:
                    weight = self.getWeight(node, v)
                    if weights[queue.index(v)] > weight:
                        indexOfInterest = queue.index(v)
                        queue[indexOfInterest] = v
                        weights[indexOfInterest] = weight
        
        return None
                    
    def getWeight(self, node, v):
        #weight = random.uniform(0,10)
        #with open('output.txt', 'a') as f:
        #    f.write(str(Vector2.asInt(node.position)) + " to ")
        #    f.write(str(Vector2.asInt(v.position)) + ": ")
        #    f.write(str(weight) + "\n")
        #return weight
        return sum(Vector2.asInt(node.position-v.position)) #generate random weights - keep track of weights in log file
                
                
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
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()

        self.uniformCostSearch(self.node, self.goal)
        
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
            #print(self.target.position/16)
            
            if self.target is not self.node:
                # get the direction of the target
                self.direction = self.getDirection()

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()