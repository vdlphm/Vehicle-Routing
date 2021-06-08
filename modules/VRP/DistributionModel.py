from modules.VRP.Store import Store
from modules.VRP.Vehicle import Vehicle
import numpy as np
from random import randint

count = 0

class DistributionModel:
    def __init__(self, storeCount, vehicleCapacity, vehicleCount, msd, msr):
        self.noOfStore = storeCount
        self.noOfVehicle = vehicleCount
        self.distanceMatrix = np.zeros((self.noOfStore + 1, self.noOfStore + 1))
        self.stores = []
        self.vehicles = []
        self.timeMatrix = np.zeros((self.noOfStore + 1, self.noOfStore + 1))

        # set up distance matrix between stores
        for i in range(self.noOfStore + 1):
            for j in range(i, self.noOfStore + 1):
                if i == j:
                    self.distanceMatrix[i][j] = 0
                else:
                    dist = self.getRandomValue(50)
                    self.distanceMatrix[i][j] = dist
                    self.distanceMatrix[j][i] = dist
                    time = self.getRandomValue(3)
                    self.timeMatrix[i][j] = time
                    self.timeMatrix[j][i] = time

        # set up stores
        for i in range(self.noOfStore):
            demand = self.getRandomValue(msd)
            rec = self.getRandomValue(msr)
            if rec > demand:
                temp = demand
                demand = rec
                rec = temp
            elif rec == demand:
                rec -= 1
            self.stores.append(Store(demand, rec))

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
            totalCap += self.stores[i - 1].demand
        return totalCap

    def analyzeOptimalRouteSimultaneous(self, optimalRoute):
        distribution = dict()
        for v in range(self.noOfVehicle):
            r = [0]
            tripsCount = 0
            #totalDistance = 0
            availableCapacity = self.routeCapacity(optimalRoute)
            availableRecyclables = 0
            i = 0
            time = 7
            store_visited = [False] * self.noOfStore
            while i < len(optimalRoute): # possible modification
                storeCapacity = self.stores[optimalRoute[i] - 1].demand
                storeRecycle = self.stores[optimalRoute[i] - 1].recylables
                if (storeRecycle + availableCapacity - storeCapacity + availableRecyclables) < self.vehicles[v].capacity \
                        and storeCapacity <= availableCapacity:
                    r.append(optimalRoute[i])
                    temp_time = time + self.timeMatrix[r[r.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                    store_tw = self.stores[optimalRoute[i] - 1].tw
                    if temp_time > 24:
                        temp_time = store_tw[0]
                    if store_tw[0] <= temp_time <= store_tw[1]:
                        time = temp_time
                        availableCapacity = availableCapacity - storeCapacity
                        availableRecyclables += storeRecycle
                        #r.append(optimalRoute[i])
                        #totalDistance += self.distanceMatrix[r[r.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                        store_visited[optimalRoute[i] - 1] = True
                    else:
                        r.remove(optimalRoute[i])
                else:
                    tripsCount += 1
                    availableCapacity = self.vehicles[v].capacity
                    availableRecyclables = 0
                    r.append(0)
                    #totalDistance += self.distanceMatrix[optimalRoute[i - 1]][0]
                    i -= 1
                i += 1

            i = 0
            #time = 7
            while i < len(optimalRoute):  # possible modification
                if not store_visited[optimalRoute[i] - 1]:
                    storeCapacity = self.stores[optimalRoute[i] - 1].demand
                    storeRecycle = self.stores[optimalRoute[i] - 1].recylables
                    if (storeRecycle + availableCapacity - storeCapacity + availableRecyclables) < self.vehicles[v].capacity \
                            and storeCapacity <= availableCapacity:
                        r.append(optimalRoute[i])
                        availableCapacity = availableCapacity - storeCapacity
                        availableRecyclables += storeRecycle
                        #totalDistance += self.distanceMatrix[r[r.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                        store_visited[optimalRoute[i] - 1] = True
                    else:
                        tripsCount += 1
                        availableCapacity = self.vehicles[v].capacity
                        availableRecyclables = 0
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
            for store in r:
                if len(s) > 0:
                    s += '--->'
                node = self.stores[store - 1]
                if store != 0:
                    s += '({}, delivery: {}, pickup: {}, tw = {})'.format(store, node.demand, node.recylables, node.tw)
                else:
                    s += '({}, tw = {})'.format(store, node.tw)
            distribution[key] = s

        return distribution

    def modelSummary(self):
        print(f'No of Store: {self.noOfStore}')
        print('Store details: ')
        for s in self.stores:
            print(s)
        print()
        print(f'No of Vehicle: {self.noOfVehicle}')
        print('Vehicle details: ')
        for v in self.vehicles:
            print(v)
        print('\nDistance matrix: ')
        s = '{:>12s}'.format("Depot")
        for k in range(len(self.stores)):
            s += '{:>8d}'.format(k + 1)
        print(s)
        for i in range(len(self.distanceMatrix)):
            if i == 0:
                s = "Depot\t"
            else:
                s = "Store{}\t".format(i)
            for j in range(len(self.distanceMatrix)):
                s += '{:4.1f}\t'.format(self.distanceMatrix[i][j])
            print(s)

        print('\nTime matrix: ')
        s = '{:>12s}'.format("Depot")
        for k in range(len(self.stores)):
            s += '{:>8d}'.format(k + 1)
        print(s)
        for i in range(len(self.timeMatrix)):
            if i == 0:
                s = "Depot\t"
            else:
                s = "Store{}\t".format(i)
            for j in range(len(self.timeMatrix)):
                s += '{:4.1f}\t'.format(self.timeMatrix[i][j])
            print(s)

    def getRandomValue(self, maxVal):
        return randint(0, maxVal) + 1


if __name__ == "__main__":
    dm = DistributionModel(2, [10, 12, 15], 3, 2, 2)
    dm.modelSummary()
