from random import randint

class Optimizer:
    @classmethod
    def shuffleArray(cls, ar):
        for i in range(len(ar) - 1, 0, -1):
            index = randint(0, i)
            temp = ar[i]
            ar[i] = ar[index]
            ar[index] = temp
        return ar

    @classmethod
    def copyFromArray(cls, source):
        dest = []
        for i in range(len(source)):
            dest.append(float(source[i]))
        return dest