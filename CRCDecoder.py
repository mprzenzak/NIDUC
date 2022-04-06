import copy


class CRCDecoder:
    polynomial = []
    polynomial4 = [1, 1, 1, 1, 1]
    polynomial8 = [1, 0, 0, 0, 0, 0, 1, 1, 1]
    polynomial16 = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    polynomial32 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]

    crcList = []
    crcList4 = [0, 0, 0, 0]
    crcList8 = [0, 0, 0, 0, 0, 0, 0, 0]
    crcList16 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    crcList32 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, crcType, crcCodeWithNoise, originalRest):
        self.crcType = crcType
        self.crcCodeWithNoise = copy.deepcopy(crcCodeWithNoise)
        self.originalRest = copy.deepcopy(originalRest)
        self.newRest = []

        if self.crcType == 4:
            self.polynomial = self.polynomial4
            self.crcList = self.crcList4
        elif self.crcType == 8:
            self.polynomial = self.polynomial8
            self.crcList = self.crcList8
        elif self.crcType == 16:
            self.polynomial = self.polynomial16
            self.crcList = self.crcList16
        elif self.crcType == 32:
            self.polynomial = self.polynomial32
            self.crcList = self.crcList32

        self.bitDifference = len(self.crcCodeWithNoise) + len(self.polynomial)

        for i in range(len(self.crcList) - len(self.originalRest)):
            self.newRest.append(0)
        self.newRest += self.originalRest
        self.bitDifference -= len(self.polynomial)

    def code_bits(self):
        correctMessageReceived = False
        xorResult = self.crcCodeWithNoise
        for bit in self.newRest:
            xorResult.append(bit)
        self.bitsToRewrite = self.crcCodeWithNoise[len(self.polynomial):]  # + self.newRest

        xorResultNew = []
        restIndex = 0
        bitsCounter = 0
        bitsUsed = len(self.polynomial)
        continueXor = True
        while continueXor:
            start = False

            for i in range(len(self.polynomial)):
                if xorResult[i] != self.polynomial[i]:
                    xorResultNew.append(1)
                    start = True
                elif xorResult[i] == self.polynomial[i] and start:
                    xorResultNew.append(0)
            for i in range(len(self.polynomial) - len(xorResultNew)):
                bitsCounter += 1
                if bitsCounter <= self.crcType + self.bitDifference:
                    xorResultNew.append(self.bitsToRewrite[restIndex])
                    restIndex += 1
                    bitsUsed += 1
                    if restIndex > len(self.bitsToRewrite) - 1:
                        continueXor = False
                        break
            xorResult = xorResultNew
            xorResultNew = []
            if len(xorResult) < len(self.polynomial):
                continueXor = False
            if xorResult == self.polynomial:
                continueXor = False
                correctMessageReceived = True
        return correctMessageReceived
