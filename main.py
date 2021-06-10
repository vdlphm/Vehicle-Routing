from modules.VRP.DistributionModel import DistributionModel
from modules.PSO.Swarm import Swarm
import csv
import numpy as np

Q = [2500]
K = 1
for file_index in range(1, 4):
    file_name = "File" + str(file_index) + ".csv"
    print("--------------------{:10s}--------------------".format(file_name))
    S = 0

    distanceMatrix = None
    timeMatrix = None
    nodeName = []
    nodeDelivery = []
    nodePickup = []
    nodeOpen = []
    nodeClose = []

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                S = len(row) - 1
                distanceMatrix = np.zeros((S, S))
                timeMatrix = np.zeros((S, S))
            elif 0 < line_count <= S:
                nodeName.append(row[0])
                for i in range(1, S + 1):
                    distanceMatrix[line_count - 1][i - 1] = float(row[i])
            elif S + 2 < line_count <= 2 * S + 2:
                for i in range(1, S + 1):
                    timeMatrix[line_count - S - 3][i - 1] = float(row[i])
            elif line_count == 2 * S + 5:
                for i in range(1, S + 1):
                    nodeDelivery.append(int(row[i]))
            elif line_count == 2 * S + 8:
                for i in range(1, S + 1):
                    nodePickup.append(int(row[i]))
            elif line_count == 2 * S + 11:
                nodeOpen.append(0)
                for i in range(2, S + 1):
                    nodeOpen.append(int(row[i]))
            elif line_count == 2 * S + 13:
                nodeClose.append(23)
                for i in range(2, S + 1):
                    nodeClose.append(int(row[i]))
            line_count += 1

    N = 10
    T = 40
    #print('Store')
    dm = DistributionModel(S - 1, Q, K, distanceMatrix, timeMatrix, nodeDelivery, nodePickup, nodeOpen, nodeClose)

    #dm.modelSummary()
    #print('-----------------------------------------\nSwarm model\n-----------------------------------------')
    swarm = Swarm(N, dm)
    #swarm.printSwarmDetail()

    #print('-----------------------------------------\nIteration Details\n-----------------------------------------')
    particleProgress = dict()
    s = "Iteration\t"
    i = 0
    while i < len(swarm.particles):
        s += "f(x" + str(i + 1) + ") f(pBest:" + str(i + 1) + ")\t"
        i += 1
    s += "f(gBest)"
    #print(s)
    particleProgress = swarm.printIterationResults(0, particleProgress)
    for i in range(1, T):
        swarm.optimizeSolution()
        particleProgress = swarm.printIterationResults(i, particleProgress)
    #print("Decode gBest Solution\n------------------------------------------")
    optimalRoute = swarm.decodeOptimalSolution()
    optimalRouteConvert = []
    for i in optimalRoute:
        optimalRouteConvert.append(int(nodeName[i]))
    print("Optimal Route: " + str(optimalRouteConvert))
    """print("\ndrop-off only\n------------------------------------------")
    distNoPick = dm.analyzeOptimalRoute(optimalRoute)
    for e in distNoPick.keys():
        print("{} -> {}".format(e, distNoPick[e]))"""
    print("\npickup and drop-off\n------------------------------------------")
    distPick = dm.analyzeOptimalRouteSimultaneous(optimalRoute, nodeName)
    for e in distPick.keys():
        print("{} \n-> {}".format(e, distPick[e]))
    print("\n")
#print(nodeName)
