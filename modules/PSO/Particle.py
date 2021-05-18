from random import random
from modules.PSO.Optimizer import Optimizer
class Particle:
    def __init__(self, x):
        self.xSolution = Optimizer.copyFromArray(x)
        self.pBest = self.xSolution
        self.pVelocity = self.setRandomVelocities(len(self.xSolution))
        self.pBestVelocity = self.pVelocity
        self.xFitnessValue = 0.0
        self.pBestValue = 0.0

    
    def setRandomVelocities(self, n):
        pVelocity = []
        for i in range(n):
            pVelocity.append(self.getRandomVelocity(n))

        return pVelocity

    def getRandomVelocity(self, upper):
        return random() * upper

    def __str__(self):
        s = "Paticle [xSolution=" + str(self.xSolution) + ", xFitnessValue="\
            + str(self.xFitnessValue) + ", pBest=" + str(self.pBest)\
            + ", pVelocity=" + str(self.pVelocity) + "]"
        return s