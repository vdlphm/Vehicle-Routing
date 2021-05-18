from modules.PSO.Optimizer import Optimizer
from modules.VRP.DistributionModel import DistributionModel
from modules.PSO.Particle import Particle
import sys


class Swarm:
    def __init__(self, noOfParticles, dm):
        self.distanceMatrix = dm.distanceMatrix
        solutionLength = dm.noOfStore
        self.possibleSolution = []
        for i in range(solutionLength):
            self.possibleSolution.append(i + 1)
        self.particles = []

        for i in range(noOfParticles):
            Optimizer.shuffleArray(self.possibleSolution)
            self.particles.append(Particle(self.possibleSolution))
            self.particles[i].xFitnessValue = self.generateFitnessValue(self.particles[i].xSolution)
            self.particles[i].pBestValue = self.generateFitnessValue(self.particles[i].pBest)
        self.gBest = []
        self.gBestVelocity = []
        self.gFitnessValue = sys.float_info.max
        self.findGlobalBest()

    def generateFitnessValue(self, currentSolution):
        prevStore = 0
        fitnessSum = 0
        for i in range(len(currentSolution)):
            v = int(round(currentSolution[i]))
            fitnessSum += self.distanceMatrix[prevStore][v]
            prevStore = v
        fitnessSum += self.distanceMatrix[prevStore][0]

        return fitnessSum

    def findGlobalBest(self):
        for p in self.particles:
            if p.xFitnessValue < self.gFitnessValue:
                self.gFitnessValue = p.xFitnessValue
                self.gBest = p.pBest
                self.gBestVelocity = p.pBestVelocity

    def optimizeSolution(self):
        i = 0
        for p in self.particles:
            p = self.__updateVelocity(p)
            p = self.__updateSolution(p)

            p.xFitnessValue = self.generateFitnessValue(p.xSolution)

            if p.xFitnessValue < p.pBestValue:
                p.pBest = p.xSolution
                p.pBestValue = p.xFitnessValue
                p.pBestVelocity = p.pVelocity
            self.particles[i] = p

            self.findGlobalBest()
            i += 1

    def __updateVelocity(self, p):
        w = 0.6
        o1 = 0.2
        b1 = 0.3
        o2 = 0.2
        b2 = 0.5

        newV = []

        for i in range(len(p.pVelocity)):
            newV.append(w * p.pVelocity[i] + (o1 * b1 * (p.pBest[i] - p.xSolution[i])) + (
                        o2 * b2 * (self.gBest[i] - p.xSolution[i])))
        p.pVelocity = newV
        return p

    def __updateSolution(self, p):
        for i in range(len(p.xSolution)):
            if (p.xSolution[i] + p.pVelocity[i] > len(p.xSolution)):
                p.xSolution[i] = len(p.xSolution)
            else:
                p.xSolution[i] = (p.xSolution[i] + p.pVelocity[i])
        return p

    def decodeOptimalSolution(self):
        print('gFitnessValue: {}'.format(self.gFitnessValue))
        print('gBest: {}'.format(self.gBest))

        indicies = dict()

        for i in range(len(self.gBest)):
            if not (self.gBest[i] in indicies):
                indicies[self.gBest[i]] = []
            indicies[self.gBest[i]].append(i)

        self.gBest.sort()
        optimalRoute = []
        i = 0
        while i < len(self.gBest):
            if len(indicies[self.gBest[i]]) > 1:
                ii = i
                for k in range(len(indicies[self.gBest[ii]])):
                    optimalRoute.append(indicies[self.gBest[ii]][k] + 1)
                    i += 1
            else:
                optimalRoute.append(indicies[self.gBest[i]][0] + 1)
            i += 1
        return optimalRoute

    def printSwarmDetail(self):
        print(f'No of Particles: {len(self.particles)}')
        for p in self.particles:
            print(p)
        print(f'Global    [gBest="{str(self.gBest)}", gFitnessValue="{str(self.gFitnessValue)}"]')

    def printIterationResults(self, t, particleProgress):
        pno = 1
        s = "{:<12d}".format(t)
        for p in self.particles:
            index = "p" + str(pno)
            if not(index in particleProgress.keys()):
                particleProgress[index] = dict()
            particleProgress[index][float(t)] = p.pBestValue
            s += "{}\t{}\t\t".format(p.xFitnessValue, p.pBestValue)
            pno += 1
        s += str(self.gFitnessValue)
        print(s)
        return particleProgress
