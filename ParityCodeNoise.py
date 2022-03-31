import copy
from math import floor
import numpy

originalMessage = []
messageWithNoise = []
distortionLevel = 0

# test
# 1000100010010001

class ParityCodeNoise():
    def __init__(self, originalMessage, distortionLevel):
        self.originalMessage = originalMessage
        self.messageWithNoise = copy.deepcopy(originalMessage)
        self.distortionLevel = distortionLevel

    def add_noise(self):
        numberOfAffectedBits = floor(self.distortionLevel / 100 * len(self.originalMessage))
        bitsToChange = numpy.random.randint(0, len(self.originalMessage), numberOfAffectedBits)

        for i in range(len(self.originalMessage)):
            for bitIndex in bitsToChange:
                if i == bitIndex:
                    if self.originalMessage[i] == 0:
                        self.messageWithNoise[i] = 1
                    else:
                        self.messageWithNoise[i] = 0
        return self.messageWithNoise
