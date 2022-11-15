from astarghost import AStarGhost
from constants import *
from vector import Vector2

class Clyde(AStarGhost): #A*Search Pacman Goal
    def __init__(self, node, pacman=None, blinky=None):
        AStarGhost.__init__(self, node,pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.directionMethod = self.aStar
        self.currentDirectionMethod = self.directionMethod
        
    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*ROWS)
        
    def chase(self):
        self.goal=self.pacman.node
        
    #def chase(self):
        #d = self.pacman.position - self.position
        #ds = d.magnitudeSquared()
        #if ds <= (TILEWIDTH*8)**2:
        #    self.scatter()
        #else:
        #    self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4