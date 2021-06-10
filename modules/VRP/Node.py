from random import randint
class Node:
    def __init__(self, timewindow, delivery,pickup=0):
        self.delivery = delivery
        self.pickup = pickup
        self.tw = timewindow

    def generateTimeWindow(self):
        start = randint(0, 24)
        end = randint(start, 24)
        while end == start:
            end = randint(start, 24)
        return [start, end]

    def __str__(self):
        return "Node {delivery=" + str(self.delivery) + ", pickup=" + str(self.pickup) + ", time window=" + str(self.tw) + "}"
