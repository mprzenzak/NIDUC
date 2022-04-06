import random


class Generator:
    def __init__(self, size):
        self.message = []
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def generate(self):
        for x in range(self._size):
            self.message.append(random.randint(0, 1))
        return self.message
