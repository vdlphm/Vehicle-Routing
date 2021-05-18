from canh.modules.VRP.Store import Store
from canh.modules.VRP.Vehicle import Vehicle
import numpy as np
from random import randint
class DistributionModel:
    def __init__(self, storeCount, vehicleCapacity, vehicleCount, msd, msr):
        self.noOfStore = storeCount
        self.noOfVehicle = vehicleCount
        self.distanceMatrix = np.zeros((self.noOfStore + 1, self.noOfStore + 1))
        self.stores = []
        self.vehicles = []
        for i in range(self.noOfStore + 1):
            for j in range(i, self.noOfStore + 1):
                if i == j:
                    self.distanceMatrix[i][j] = 0
                else:
                    val = self.getRandomValue(50)
                    self.distanceMatrix[i][j] = val
                    self.distanceMatrix[j][i] = val
                    
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
        for i in range(self.noOfVehicle):
            self.vehicles.append(Vehicle(vehicleCapacity[i]))
            
    def analyzeOptimalRoute(self, optimalRoute):
        distribution = dict()
        for v in range(self.noOfVehicle):
            route = [0]
            tripsCount = 0
            totalDistance = 0
            availableCapacity = self.vehicles[v].capacity
            i = 0
            while i < len(optimalRoute):
                storeCapacity = self.stores[optimalRoute[i] - 1].demand
                if availableCapacity - storeCapacity >= 0:
                    route.append(optimalRoute[i])
                    totalDistance += self.distanceMatrix[route[route.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                    availableCapacity -= storeCapacity
                else:
                    tripsCount += 1
                    availableCapacity = self.vehicles[v].capacity
                    route.append(0)
                    totalDistance += self.distanceMatrix[optimalRoute[i-1]][0]
                    i -= 1
                i += 1
            route.append(0)
            tripsCount += 1
            key = 'VehicleCap:' + str(self.vehicles[v].capacity) + ',Trips:' + str(tripsCount) + ',TotalDistance:' + str(totalDistance)
            distribution[key] = route

        return distribution

    def analyzeOptimalRouteSimultaneous(self, optimalRoute):
        distribution = dict()
        for v in range(self.noOfVehicle):
            route = [0]
            tripsCount = 0
            totalDistance = 0
            availableCapacity = self.vehicles[v].capacity
            availableRecyclables = 0
            i = 0
            while i < len(optimalRoute):
                storeCapacity = self.stores[optimalRoute[i]-1].demand
                storeRecycle = self.stores[optimalRoute[i]-1].recylables
                if (storeRecycle + availableCapacity - storeCapacity) < self.vehicles[v].capacity\
                    and storeCapacity < availableCapacity:
                    availableCapacity = availableCapacity - storeCapacity
                    availableRecyclables += storeRecycle
                    route.append(optimalRoute[i])
                    totalDistance += self.distanceMatrix[route[route.index(optimalRoute[i]) - 1]][optimalRoute[i]]
                else:
                    tripsCount += 1
                    availableCapacity = self.vehicles[v].capacity
                    availableRecyclables = 0
                    route.append(0)
                    totalDistance += self.distanceMatrix[optimalRoute[i-1]][0]
                    i -= 1
                i += 1
            route.append(0)
            tripsCount += 1
            key = 'VehicleCap:' + str(self.vehicles[v].capacity) + ',Trips:' + str(tripsCount) + ',TotalDistance:' + str(totalDistance)
            distribution[key] = route
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

    def getRandomValue(self, maxVal):
        return randint(0, maxVal) + 1


if __name__ == "__main__":
    dm = DistributionModel(5, [10, 12, 15], 3, 2, 2)
    dm.modelSummary()