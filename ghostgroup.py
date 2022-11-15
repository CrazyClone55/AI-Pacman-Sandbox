from blinky import Blinky
from pinky import Pinky
from inky import Inky
from clyde import Clyde



class GhostGroup(object):
    def __init__(self, node, nodes, pacman):
        self.blinky = Blinky(node,nodes, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman)
        self.clyde = Clyde(node,nodes,pacman)
        #self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        self.ghosts = []
        
    def __iter__(self):
        return iter(self.ghosts)
    
    def update(self, dt):
        for ghost in self:
            ghost.update(dt)
            
    def startFright(self):
        for ghost in self:
            ghost.startFright()
        self.resetPoints()
    
    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)
            
    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2
            
    def resetPoints(self):
        for ghost in self:
            ghost.points = 200
            
    def reset(self):
        for ghost in self:
            ghost.reset()
        
    def hide(self):
        for ghost in self:
            ghost.visible = False
    
    def show(self):
        for ghost in self:
            ghost.visible = True
        
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)