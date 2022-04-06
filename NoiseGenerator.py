import copy

import numpy
from numpy import random

originalMessage = []
messageWithNoise = []
distortionLevel = 0


class NoiseGenerator:
    def __init__(self, originalMessage, numberOfBitsAffected):
        self.originalMessage = copy.deepcopy(originalMessage)
        self.messageWithNoise = copy.deepcopy(originalMessage)
        self.numberOfBitsAffected = numberOfBitsAffected

    def add_noise(self):
        bitsToChange = numpy.random.randint(0, len(self.originalMessage), self.numberOfBitsAffected)

        for i in range(len(self.originalMessage)):
            for bitIndex in bitsToChange:
                if i == bitIndex:
                    if self.originalMessage[i] == 0:
                        self.messageWithNoise[i] = 1
                    else:
                        self.messageWithNoise[i] = 0
        return self.messageWithNoise
