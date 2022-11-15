from ghost import Ghost
from constants import *
from vector import Vector2

class Inky(Ghost): #Greedy 4 spaces behind TODO Change goal to the node
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node ,pacman, blinky)       
        self.name = INKY
        self.color = TEAL
        self.directionMethod = self.greedyAlgorithm
        self.currentDirectionMethod = self.directionMethod
        
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*COLS, TILEHEIGHT*ROWS)
        
    def chase(self):
        if self.pacman.direction is STOP:
            self.goal = self.pacman.node
            return
            
        self.goal = self.pacman.node
        for x in range(4):
            if self.goal.neighbors[-1*self.pacman.direction] is not None:
               self.goal = self.goal.neighbors[-1*self.pacman.direction]
            else:
                break
    
#    def chase(self):
#        vec1  =self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH*2
#        vec2 = (vec1 - self.blinky.position) *2
#        self.goal = self.blinky.position + vec2
