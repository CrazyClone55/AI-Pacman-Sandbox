import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.setSpeed(100)
        
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)
    
    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius) **2
        if dSquared <= rSquared:
            return True
        return False

    def update(self, dt):	
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getKeyPress()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()        
        
    def getKeyPress(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[K_DOWN]:
            return DOWN
        if keyPressed[K_RIGHT]:
            return RIGHT
        if keyPressed[K_LEFT]:
            return LEFT
        if keyPressed[K_UP]:
            return UP
        return STOP
    
    def render(self, screen):
        pos = self.position.asInt()
        pygame.draw.circle(screen, self.color, pos, self.radius)


