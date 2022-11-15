from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Ghost(Entity):
    def __init__(self, node, pacman = None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node
        
    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)
    
    def scatter(self):
        self.goal = Vector2()
        
    def chase(self):
        self.goal = self.pacman.node
        
    def startFright(self):
        self.mode.setFrightMode()
        if self.mode.current is FRIGHT:
            self.setSpeed(50)
            self.currentDirectionMethod = self.randomDirection
    
    def normalMode(self):
        self.setSpeed(100)
        self.currentDirectionMethod = self.directionMethod
        
    def spawn(self):
        self.goal = self.spawnNode
        
    def setSpawnNode(self, node):
        self.spawnNode = node
    
    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current is SPAWN:
            self.setSpeed(150)
            self.currentDirectionMethod = self.directionMethod
            self.spawn()
            
    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.currentDirectionMethod = self.directionMethod