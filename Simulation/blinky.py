from UCSGhost import UCSGhost
from constants import *

class Blinky(UCSGhost): #UCS 2 spaces ahead 2 spaces up
    def __init__(self,node, pacman = None, blinky = None):
        UCSGhost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.directionMethod = self.uniformCostSearch
        self.currentDirectionMethod = self.directionMethod
        
    def chase(self):
        if self.pacman.direction is STOP:
            self.goal = self.pacman.node
        elif self.pacman.direction is LEFT or RIGHT:
            self.goal = self.pacman.node
            for x in range(2):
                if self.goal.neighbors[self.pacman.direction] is not None:
                    self.goal = self.goal.neighbors[self.pacman.direction]
                else:
                    break
            
            for x in range(2):
                if self.goal.neighbors[UP] is not None:
                    self.goal = self.goal.neighbors[UP]
            
        elif self.pacman.direction is UP or DOWN:
            self.goal = self.pacman.node
            for x in range(2):
                if self.goal.neighbors[self.pacman.direction] is not None:
                    self.goal = self.goal.neighbors[self.pacman.direction]
                else:
                    break
            for x in range(2):
                if self.goal.neighbors[LEFT] is not None:
                    self.goal = self.goal.neighbors[LEFT]
                else:
                    break