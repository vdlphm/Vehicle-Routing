from canh.modules.VRP.DistributionModel import DistributionModel
from canh.modules.PSO.Swarm import Swarm
from canh.modules.VRP.Store import Store
import numpy as np


S = 5
Q = [12, 15, 20]
K = 3

MSD = 10
MSR = 5

N = 3
T = 12
print('Store')
dm = DistributionModel(S,Q,K,MSD,MSR)
"""dm.distanceMatrix = np.array([[0.0, 37.0, 11.0, 32.0, 29.0, 35.0],
                              [37.0, 0.0, 9.0, 42.0, 35.0, 21.0],
                              [11.0, 9.0, 0.0, 25.0, 18.0, 5.0],
                              [32.0, 42.0, 25.0, 0.0, 31.0, 14.0],
                              [29.0, 35.0, 18.0, 31.0, 0.0, 35.0],
                              [35.0, 21.0, 25.0, 14.0, 35.0, 0.0]
                              ])
s = []
for i in [[3, 1], [5, 3], [4, 2], [4, 3], [1, 0]]:
    s.append(Store(i[0], i[1]))
dm.stores = s"""

dm.modelSummary()
print('-----------------------------------------\nSwarm model\n-----------------------------------------')
swarm = Swarm(N, dm)
swarm.printSwarmDetail()

print('-----------------------------------------\nIteration Details\n-----------------------------------------')
particleProgress = dict()
s = "Iteration\t"
i = 0
while i < len(swarm.particles):
    s += "f(x" + str(i + 1) + ") f(pBest:" + str(i + 1) + ")\t"
    i += 1
s += "f(gBest)"
print(s)
particleProgress = swarm.printIterationResults(0, particleProgress)
for i in range(1, T):
    swarm.optimizeSolution()
    particleProgress = swarm.printIterationResults(i, particleProgress)
print("Decode gBest Solution\n------------------------------------------")
optimalRoute = swarm.decodeOptimalSolution()
print("Optimal Route: " + str(optimalRoute))
print("\ndropoff only\n------------------------------------------")
distNoPick = dm.analyzeOptimalRoute(optimalRoute)
for e in distNoPick.keys():
    print("{} -> {}".format(e, distNoPick[e]))
print("\npickup and dropoff\n------------------------------------------")
distPick = dm.analyzeOptimalRouteSimultaneous(optimalRoute)
for e in distPick.keys():
    print("{} -> {}".format(e, distPick[e]))