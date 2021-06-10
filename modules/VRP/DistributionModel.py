from modules.VRP.Node import Node
from modules.VRP.Vehicle import Vehicle
import numpy as np
from random import randint

count = 0

class DistributionModel:
    def __init__(self, nodeCount, vehicleCapacity, vehicleCount, distanceMatrix, timeMatrix, nodeDelivery, nodePickup, nodeOpen, nodeClose):
        self.noOfNode = nodeCount
        self.noOfVehicle = vehicleCount
        self.distanceMatrix = distanceMatrix
        self.nodes = []
        self.vehicles = []
        self.timeMatrix = timeMatrix

        # set up Nodes
        for i in range(self.noOfNode):
            delivery = nodeDelivery[i + 1]
            pickup = nodePickup[i + 1]
            self.nodes.append(Node([nodeOpen[i + 1], nodeClose[i + 1]], delivery, pickup))


        # set up vehicles
        for i in range(self.noOfVehicle):
            self.vehicles.append(Vehicle(vehicleCapacity[i]))

    def routeDist(self, route):
        totalDist = 0
        for i in range(1, len(route)):
            totalDist += self.distanceMatrix[route[i]][route[i - 1]]
        return totalDist

    def routeCapacity(self, route):
        totalCap = 0
        for i in route:
            totalCap += self.nodes[i - 1].delivery
        return totalCap

    def analyzeOptimalRouteSimultaneous(self, optimalRoute, nodeName):
        distribution = dict()
        for v in range(self.noOfVehicle):
            r = [0]
            tripsCount = 0
            #totalDistance = 0
            availableCapacity = self.routeCapacity(optimalRoute)
            availablePickup = 0
            i = 0
            time = 8
            node_visited = [False] * self.noOfNode
            while i < len(optimalRoute): # possible modification
                nodeCapacity = self.nodes[optimalRoute[i] - 1].delivery
                nodeRecycle = self.nodes[optimalRoute[i] - 1].pickup
                if (nodeRecycle + availableCapacity - nodeCapacity + availablePickup) < self.vehicles[v].capacity \
                        and nodeCapacity <= availableCapacity:
                    r.append(optimalRoute[i])
                    temp_time = time + self.timeMatrix[r[r.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                    node_tw = self.nodes[optimalRoute[i] - 1].tw
                    if temp_time > 24:
                        temp_time = node_tw[0]
                    if node_tw[0] <= temp_time <= node_tw[1]:
                        time = temp_time
                        availableCapacity -= nodeCapacity
                        availablePickup += nodeRecycle
                        #r.append(optimalRoute[i])
                        #totalDistance += self.distanceMatrix[r[r.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                        node_visited[optimalRoute[i] - 1] = True
                    else:
                        r.remove(optimalRoute[i])
                else:
                    tripsCount += 1
                    availableCapacity = self.vehicles[v].capacity
                    availablePickup = 0
                    r.append(0)
                    #totalDistance += self.distanceMatrix[optimalRoute[i - 1]][0]
                    i -= 1
                i += 1

            i = 0
            #time = 7
            while i < len(optimalRoute):  # possible modification
                if not node_visited[optimalRoute[i] - 1]:
                    nodeCapacity = self.nodes[optimalRoute[i] - 1].delivery
                    nodeRecycle = self.nodes[optimalRoute[i] - 1].pickup
                    if (nodeRecycle + availableCapacity - nodeCapacity + availablePickup) < self.vehicles[v].capacity \
                            and nodeCapacity <= availableCapacity:
                        r.append(optimalRoute[i])
                        availableCapacity = availableCapacity - nodeCapacity
                        availablePickup += nodeRecycle
                        #totalDistance += self.distanceMatrix[r[r.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                        node_visited[optimalRoute[i] - 1] = True
                    else:
                        tripsCount += 1
                        availableCapacity = self.vehicles[v].capacity
                        availablePickup = 0
                        r.append(0)
                        #totalDistance += self.distanceMatrix[optimalRoute[i - 1]][0]
                        i -= 1
                i += 1

            for i in range(len(r) - 2):
                if r[i] == r[i + 1] == 0:
                    r.pop(i + 1)
            r.append(0)
            tripsCount += 1
            key = 'VehicleCap:' + str(self.vehicles[v].capacity) + ',Trips:' + str(
                tripsCount) + ',TotalDistance:' + str(self.routeDist(r))
            s = ''
            for n in r:
                if len(s) > 0:
                    s += '--->'
                node = self.nodes[n - 1]
                if n != 0:
                    s += '({}, D: {}, P: {}, tw = {})'.format(nodeName[n], node.delivery, node.pickup, node.tw)
                else:
                    s += '({})'.format(nodeName[n])
            distribution[key] = s

        return distribution

    def modelSummary(self):
        print(f'No of node: {self.noOfNode}')
        print('node details: ')
        for s in self.nodes:
            print(s)
        print()
        print(f'No of Vehicle: {self.noOfVehicle}')
        print('Vehicle details: ')
        for v in self.vehicles:
            print(v)
        print('\nDistance matrix: ')
        s = '{:>4s}'.format("")
        for k in range(len(self.nodes)):
            s += '{:>8d}'.format(k + 1)
        print(s)
        for i in range(len(self.distanceMatrix)):
            s = "Node{}\t".format(i)
            for j in range(len(self.distanceMatrix)):
                s += '{:4.1f}\t'.format(self.distanceMatrix[i][j])
            print(s)

        print('\nTime matrix: ')
        s = '{:>4s}'.format("")
        for k in range(len(self.nodes)):
            s += '{:>8d}'.format(k + 1)
        print(s)
        for i in range(len(self.timeMatrix)):
            s = "node{}\t".format(i)
            for j in range(len(self.timeMatrix)):
                s += '{:4.1f}\t'.format(self.timeMatrix[i][j])
            print(s)

    def getRandomValue(self, maxVal):
        return randint(0, maxVal) + 1


if __name__ == "__main__":
    dm = DistributionModel(2, [10, 12, 15], 3, 2, 2)
    dm.modelSummary()
