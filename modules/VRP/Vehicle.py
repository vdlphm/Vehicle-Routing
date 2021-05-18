class Vehicle:
    def __init__(self, cap):
        self.capacity = cap

    def __str__(self):
        return "Vehicle [capacity=" + str(self.capacity) + "]"

if __name__ == "__main__":
    v = Vehicle(100)
    print(v)