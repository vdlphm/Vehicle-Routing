from modules.VRP.DistributionModel import DistributionModel
from modules.PSO.Swarm import Swarm

S = 3
Q = [40]
K = 1

MSD = 10
MSR = 5

N = 3
T = 12
print('Store')
dm = DistributionModel(S,Q,K,MSD,MSR)

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
"""print("\ndrop-off only\n------------------------------------------")
distNoPick = dm.analyzeOptimalRoute(optimalRoute)
for e in distNoPick.keys():
    print("{} -> {}".format(e, distNoPick[e]))"""
print("\npickup and drop-off\n------------------------------------------")
distPick = dm.analyzeOptimalRouteSimultaneous(optimalRoute)
for e in distPick.keys():
    print("{} -> {}".format(e, distPick[e]))