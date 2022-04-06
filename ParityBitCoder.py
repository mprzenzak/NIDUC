import copy


class ParityBitCoder:
    parityCoddedMessage = []

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
        else:
            self.parityCoddedMessage.append(1)
        return self.parityCoddedMessage
