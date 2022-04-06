import copy


class ParityBitDecoder:
    parityDecodedMessage = []

    def __init__(self, messageWithNoise):
        self.parityDecodedMessage = copy.deepcopy(messageWithNoise)  # kopiuje obiekt zamiast tworzyć referencje

    def code_bits(self):
        positiveBits = 0
        print("DUPAL")
        print(self.parityDecodedMessage)
        for i in range(len(self.parityDecodedMessage) - 1):
            if self.parityDecodedMessage[i] == 1:
                positiveBits += 1
        parityBit = self.parityDecodedMessage[-1]

        return self.parityDecodedMessage, parityBit
