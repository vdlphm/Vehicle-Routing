class Store:
    def __init__(self, demand, recylables=0):
        self.demand = demand
        self.recylables = recylables

    def __str__(self):
        return "Store [demand=" + str(self.demand) + ", recyclables=" + str(self.recylables) + "]"