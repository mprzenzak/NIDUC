import copy

crc16CoddedMessage = []  # chyba do usuniecia
polynomial = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
crcList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
rest = []


# [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0] result
# [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1] polynomial
# [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1] result 2
#             [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]


class CRCCoder:
    def __init__(self, message):
        self.crc16CoddedMessage = copy.deepcopy(message)
        # self.crc16CoddedMessage = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]

        self.crc16CoddedMessage += crcList

    def code_bits(self):
        xorResult = self.crc16CoddedMessage
        xorResultNew = []
        a = 0

        zerosCounter = 0
        while zerosCounter <= 15:
            a += 1
            start = False

            for i in range(len(polynomial)):
                if xorResult[i] != polynomial[i]:
                    xorResultNew.append(1)
                    start = True
                elif xorResult[i] == polynomial[i] and start:
                    xorResultNew.append(0)
            for i in range(len(polynomial) - len(xorResultNew)):
                zerosCounter += 1
                if zerosCounter <= 15:
                    xorResultNew.append(0)

            # print("xorResultNEEEEEEEEEEEEEEEEWWWWWW")
            # print(xorResultNew)
            xorResult = xorResultNew
            xorResultNew = []
        return xorResult
