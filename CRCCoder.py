import copy


class CRCCoder:
    polynomial = []
    polynomial4 = [1, 1, 1, 1, 1]
    polynomial8 = [1, 0, 0, 0, 0, 0, 1, 1, 1]
    polynomial16 = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    polynomial32 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]
    # sprawdzic dla wielomianu x+1 - wielomian 1 1
    # ------------------------------------------ciagi bitow dluzzsze od sumy kontrolnej------------------------------------------
    # ------------------------------------------opwinno byc tak, ze generuje gdzie jest blad, na ktorym bicie. Zamieniam w liscie zer na tych miejscach na jedynki i robie xora z cala wiadomoscia
    # requestowanie powtorzen
    # szum reszty
    # nie pamietam co bylo z zamiana 0 i 1 w bicie parzystosci
    crcList = []
    crcList4 = [0, 0, 0, 0]
    crcList8 = [0, 0, 0, 0, 0, 0, 0, 0]
    crcList16 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    crcList32 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, crcType, message):
        self.crcType = crcType
        self.crcCoddedMessage = copy.deepcopy(message)

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

        self.bitDifference = len(self.crcCoddedMessage)
        self.bitsToRewrite = self.crcCoddedMessage[len(self.polynomial):] + self.crcList
        self.crcCoddedMessage += self.crcList
        self.bitDifference -= len(self.polynomial)

    def code_bits(self):
        xorResult = self.crcCoddedMessage
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
            xorResult = xorResultNew
            xorResultNew = []
            if len(xorResult) < len(self.polynomial):
                continueXor = False
        return xorResult
