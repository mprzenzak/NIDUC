from math import floor

import CRCCoder
import CRCDecoder
import ParityBitDecoder
from Generator import *
from ParityBitCoder import ParityBitCoder
import NoiseGenerator
import random


def initialize():
    mode = int(input(
        "Wybierz rodzaj zabezpieczenia używany podczas kontroli poprawności wysłanego pakietu:\n 1 - Brak zabezpieczenia\n "
        "2 - Bit parzystości\n 3 - Cykliczny kod nadmiarowy\n\tWybór: "))
    frameAmount = int(input("Ile ramek danych chcesz przesłać? "))
    distortionLevel = int(input("Podaj jaki procent ramek ma zostać zaszumionych: "))
    requestRepetitions = int(input("Czy chcesz wysyłać ponownie niepoprawnie zdekodowane ramki?\n 1 - Tak\n 2 - Nie\n"))
    framesTab = []

    for i in range(frameAmount):
        framesTab.append(0)

    counter = floor(distortionLevel / 100 * frameAmount)
    affectedFramesIndexes = random.sample(range(frameAmount), counter)

    # Bit parzystości
    if mode == 2:
        bitChainLength = int(
            input("Podaj długość ciągu bitów, który zostanie losowo wygenerowany dla każdej ramki: "))
        for frameIndex in range(frameAmount):
            print("Ramka " + str(frameIndex + 1) + ":")
            # Tworzy listę wypełnioną w losowy sposób zerami i jedynkami o długości równej bitChainLength
            message = Generator(bitChainLength)
            parityCode = ParityBitCoder(message.generate())
            print("Ciąg bitów bez kodowania:")
            originalCode = parityCode.parityCoddedMessage
            print(originalCode)
            print("Ciąg bitów z dodanym bitem parzystości:")
            parityCodeWithParityBit = parityCode.code_bits()
            print(parityCodeWithParityBit)
            sendParityBitCodedMessage(frameIndex, affectedFramesIndexes, bitChainLength, parityCodeWithParityBit,
                                      requestRepetitions)


    # Kod CRC
    elif mode == 3:
        crcType = int(input("Podaj typ kodu CRC, który chcesz użyć dla wszystkich ramek:\n - 4\n - 8\n - 16\n - 32\n"))
        messageLength = int(input("Podaj długość przesyłanego ciągu bitów:"))
        for frameIndex in range(frameAmount):
            print("Ramka " + str(frameIndex + 1) + ":")
            message = Generator(messageLength).generate()
            originalCode = message
            crcCode = CRCCoder.CRCCoder(crcType, message)
            originalRest = crcCode.code_bits()
            print("Ciąg bitów bez kodowania:")
            print(originalCode)
            print("Reszta z dzielenia w CRC " + str(crcType) + ":")
            print(originalRest)
            sendCRCCodedMessage(frameIndex, affectedFramesIndexes, crcType, messageLength, originalCode, originalRest,
                                requestRepetitions)


def sendParityBitCodedMessage(frameIndex, affectedFramesIndexes, bitChainLength, parityCodeWithParityBit,
                              requestRepetitions):
    if frameIndex in affectedFramesIndexes:
        numberOfMessageBitsAffected = random.randint(1, bitChainLength)
    else:
        numberOfMessageBitsAffected = 0
    parityCodeWithNoise = NoiseGenerator.NoiseGenerator(parityCodeWithParityBit,
                                                        numberOfMessageBitsAffected).add_noise()

    print("Ciąg bitów z nałożonym szumem:")
    print(parityCodeWithNoise)

    print("Ciąg bitów po zdekodowaniu:")
    parityCodeDecoded = ParityBitDecoder.ParityBitDecoder(parityCodeWithNoise).code_bits()
    print(parityCodeDecoded[0])

    if parityCodeDecoded[1] == parityCodeWithParityBit[-1]:
        print("Ramka została przesłana i odczytana poprawnie")
    else:
        print("Podczas przesyłania ramki wystąpił błąd")
        if requestRepetitions == 1:
            print("\nPonowne przesyłanie ramki...")
            sendParityBitCodedMessage(frameIndex, affectedFramesIndexes, bitChainLength, parityCodeWithParityBit,
                                      requestRepetitions)
    print()


def sendCRCCodedMessage(frameIndex, affectedFramesIndexes, crcType, messageLength, originalCode, originalRest,
                        requestRepetitions):
    if frameIndex in affectedFramesIndexes:
        numberOfMessageBitsAffected = random.randint(1, messageLength)
        numberOfRestBitsAffected = random.randint(1, len(originalRest))
    else:
        numberOfMessageBitsAffected = 0
        numberOfRestBitsAffected = 0
    crcCodeWithNoise = NoiseGenerator.NoiseGenerator(originalCode, numberOfMessageBitsAffected).add_noise()
    restWithNoise = NoiseGenerator.NoiseGenerator(originalRest, numberOfRestBitsAffected).add_noise()
    print("Ciąg bitów z nałożonym szumem:")
    print(crcCodeWithNoise)
    print("Reszta z nałożonym szumem:")
    print(restWithNoise)
    print("Dekodowanie przesłanej ramki...")
    # Jeżeli kod będzie poprawny, to zostanie zwrócona pusta lista
    correctMessageReceived = CRCDecoder.CRCDecoder(crcType, crcCodeWithNoise, restWithNoise).code_bits()
    if correctMessageReceived:
        print("Ramka została przesłana i odczytana poprawnie")
    else:
        print("Podczas przesyłania ramki wystąpił błąd.")
        if requestRepetitions == 1:
            print("\nPonowne przesyłanie ramki...")
            sendCRCCodedMessage(frameIndex, affectedFramesIndexes, crcType, messageLength, originalCode, originalRest,
                                requestRepetitions)
    print()


if __name__ == "__main__":
    initialize()
