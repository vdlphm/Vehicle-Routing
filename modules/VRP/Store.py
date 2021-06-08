from random import randint
class Store:
    def __init__(self, demand, recylables=0):
        self.demand = demand
        self.recylables = recylables
        self.tw = self.generateTimeWindow()

    def generateTimeWindow(self):
        start = randint(0, 24)
        end = randint(start, 24)
        while end == start:
            end = randint(start, 24)
        return [start, end]
    def __str__(self):
        return "Store {demand=" + str(self.demand) + ", recyclables=" + str(self.recylables) + ", time window=" + str(self.tw) + "}"
