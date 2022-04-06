import copy


class ParityBitCoder:
    parityCoddedMessage = []
    # numberOfFrames = 0
    # frameSize = 0
    # framesCounter = 0

    def __init__(self, message):
        self.parityCoddedMessage = copy.deepcopy(message)  # kopiuje obiekt zamiast tworzyć referencje
    def code_bits(self):
        positiveBits = 0
        for bit in self.parityCoddedMessage:
            if bit == 1:
                positiveBits += 1
        # dodawanie bitu parzystości
        if positiveBits % 2 == 0:
             self.parityCoddedMessage.append(0)
            #numpy.append(self.message, 0)
        else:
             self.parityCoddedMessage.append(1)
            #Snumpy.append(self.message, 1)
        return self.parityCoddedMessage
