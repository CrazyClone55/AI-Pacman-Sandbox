
from ghost import Ghost
from constants import *
from vector import Vector2

class Pinky(Ghost): #Greedy 4 spaces ahead TODO Change goal to the node
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node,pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.directionMethod = self.greedyAlgorithm
        self.currentDirectionMethod = self.directionMethod
    
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*COLS, 0)
        
    def chase(self):
        if self.pacman.direction is STOP:
            self.goal = self.pacman.node
            return
        
        self.goal = self.pacman.node
        for x in range(4):
            if self.goal.neighbors[self.pacman.direction] is not None:
               self.goal = self.goal.neighbors[self.pacman.direction]
            else:
                break