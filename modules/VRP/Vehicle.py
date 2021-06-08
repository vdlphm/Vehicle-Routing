class Vehicle:
    def __init__(self, cap):
        self.capacity = cap

    def __str__(self):
        return "Vehicle [capacity=" + str(self.capacity) + "]"
