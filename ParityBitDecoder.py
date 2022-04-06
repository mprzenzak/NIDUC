import copy


class ParityBitDecoder:
    def __init__(self, messageWithNoise):
        self.parityDecodedMessage = copy.deepcopy(messageWithNoise)  # kopiuje obiekt zamiast tworzyć referencje

    def code_bits(self):
        positiveBits = 0

        for i in range(len(self.parityDecodedMessage) - 1):
            if self.parityDecodedMessage[i] == 1:
                positiveBits += 1
        # dodawanie bitu parzystości
        if positiveBits % 2 == 0:
            self.parityDecodedMessage[-1] = 0
        else:
            self.parityDecodedMessage[-1] = 1
        return self.parityDecodedMessage, self.parityDecodedMessage[-1]
