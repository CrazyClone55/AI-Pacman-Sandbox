from controller import Controller
from Simulation.GA import Simulation

if __name__ == "__main__":
    simulation = Simulation()
    simulation.startGame()
    while simulation.checkStop() is False:
        simulation.update()
    goodPath = Simulation.getWinner()
    
    game = Controller()
    game.startGame()
    while True:
        game.update()