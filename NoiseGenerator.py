import copy

import numpy
from numpy import random

originalMessage = []
messageWithNoise = []
distortionLevel = 0


class NoiseGenerator:
    def __init__(self, originalMessage, numberOfBitsAffected):
        self.message = copy.deepcopy(originalMessage)
        self.numberOfBitsAffected = numberOfBitsAffected

    def add_noise(self):
        bitsToChange = numpy.random.randint(0, len(self.message), self.numberOfBitsAffected)
        templateList = []
        for i in range(len(self.message)):
            if i in bitsToChange:
                templateList.append(1)
            else:
                templateList.append(0)

        for i in range(len(self.message)):
            if self.message[i] != templateList[i]:
                self.message[i] = 1
            else:
                self.message[i] = 0
        return self.message
