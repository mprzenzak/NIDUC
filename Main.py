from math import floor

import CRCCoder
import CRCDecoder
import ParityBitDecoder
from Generator import *
from ParityBitCoder import ParityBitCoder
import NoiseGenerator
import random

ifNoiseNotDetected = 0
undetectedFramesList = []


def initialize():
    numberOfTests = 100  # int(input("Ile testów chcesz przeprowadzić? "))
    mode = 3  # int(input(
    # "Wybierz rodzaj zabezpieczenia używany podczas kontroli poprawności wysłanego pakietu: \n 1 - Brak zabezpieczenia\n "
    # "2 - Bit parzystości\n 3 - Cykliczny kod nadmiarowy\n\tWybór: "))
    frameAmount = 1  # int(input("Ile ramek danych chcesz przesłać? "))
    distortionLevel = 100  # int(input("Podaj jaki procent ramek ma zostać zaszumionych: "))
    bitsNoised = 0  # int(input("Ile bitów ma zostać zaszumionych? "))
    requestRepetitions = 2  # int(
    # input("Czy chcesz wysyłać ponownie niepoprawnie zdekodowane ramki? \n 1 - Tak\n 2 - Nie\n"))
    # messageLength = int(input("Podaj długość przesyłanego ciągu bitów: "))
    messageLengthValues = [4, 10, 25, 100, 200, 300, 500, 800, 1000]
    crcType = 0
    for i in messageLengthValues:
        open("UndetectedNoise_" + str(i) + '.txt', 'w').close()
    open('Results.txt', 'w').close()

    if mode == 3:
        crcType = int(input("Podaj typ kodu CRC, który chcesz użyć dla wszystkich ramek: \n - 4\n - 8\n - 16\n - 32\n"))

    for messageLength in messageLengthValues:
        global undetectedFramesList
        undetectedFramesList = []
        outputFile = "UndetectedNoise_" + str(messageLength)
        bitsNoised = floor(0.25 * messageLength)
        for configuration in range(numberOfTests):
            global ifNoiseNotDetected
            ifNoiseNotDetected = 0
            test(mode, frameAmount, distortionLevel, requestRepetitions, crcType, messageLength, outputFile,
                 numberOfTests, bitsNoised)

    print("Niewykryte ramek w poszczególnych iteracjach:")
    print(undetectedFramesList)


def test(mode, frameAmount, distortionLevel, requestRepetitions, crcType, messageLength, outputFile, numberOfTests,
         bitsNoised):
    framesTab = []

    for i in range(frameAmount):
        framesTab.append(0)

    counter = floor(distortionLevel / 100 * frameAmount)
    affectedFramesIndexes = random.sample(range(frameAmount), counter)

    # Bit parzystości
    if mode == 2:
        for frameIndex in range(frameAmount):
            print("Ramka " + str(frameIndex + 1) + ":")
            # Tworzy listę wypełnioną w losowy sposób zerami i jedynkami o długości równej bitChainLength
            message = Generator(messageLength)
            parityCode = ParityBitCoder(message.generate())
            print("Ciąg bitów bez kodowania:")
            originalCode = parityCode.parityCoddedMessage
            print(originalCode)
            print("Ciąg bitów z dodanym bitem parzystości:")
            parityCodeWithParityBit = parityCode.code_bits()
            print(parityCodeWithParityBit)
            sendParityBitCodedMessage(frameIndex, affectedFramesIndexes, messageLength, parityCodeWithParityBit,
                                      requestRepetitions, bitsNoised)


    # Kod CRC
    elif mode == 3:
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
                                requestRepetitions, bitsNoised)

    print("Czy nie wykryto ramki:")
    print(ifNoiseNotDetected)
    print()
    undetectedFramesList.append(ifNoiseNotDetected)
    f = open(outputFile + ".txt", "a")
    f.write(str(ifNoiseNotDetected).replace(".", ",") + "\n")
    if len(undetectedFramesList) == numberOfTests:
        f.write("\nSrednia:\n")
        f.write(str(sum(undetectedFramesList) / len(undetectedFramesList)).replace(".", ",") + "\n")
        resultsFile = open("Results.txt", "a")
        resultsFile.write(str(sum(undetectedFramesList) / len(undetectedFramesList)).replace(".", ",") + "\n")
    f.close()


def sendParityBitCodedMessage(frameIndex, affectedFramesIndexes, bitChainLength, parityCodeWithParityBit,
                              requestRepetitions, bitsNoised):
    if frameIndex in affectedFramesIndexes:
        numberOfMessageBitsAffected = random.randint(1, bitChainLength)
    else:
        numberOfMessageBitsAffected = 0
    if bitsNoised != 0:
        numberOfMessageBitsAffected = bitsNoised
    parityCodeWithNoise = NoiseGenerator.NoiseGenerator(parityCodeWithParityBit,
                                                        numberOfMessageBitsAffected).add_noise()

    print("Ciąg bitów z nałożonym szumem:")
    print(parityCodeWithNoise)

    print("Ciąg bitów po zdekodowaniu:")
    parityCodeDecoded = ParityBitDecoder.ParityBitDecoder(parityCodeWithNoise).code_bits()
    print(parityCodeDecoded[0])

    if parityCodeDecoded[1] == parityCodeWithParityBit[-1]:
        print("Ramka została przesłana i odczytana poprawnie")
        global ifNoiseNotDetected
        ifNoiseNotDetected += 1
    else:
        print("Podczas przesyłania ramki wystąpił błąd")
        if requestRepetitions == 1:
            print("\nPonowne przesyłanie ramki...")
            sendParityBitCodedMessage(frameIndex, affectedFramesIndexes, bitChainLength, parityCodeWithParityBit,
                                      requestRepetitions)
    print()


def sendCRCCodedMessage(frameIndex, affectedFramesIndexes, crcType, messageLength, originalCode, originalRest,
                        requestRepetitions, bitsNoised):
    if frameIndex in affectedFramesIndexes:
        numberOfMessageBitsAffected = random.randint(1, messageLength)
        if len(originalRest) != 0:
            numberOfRestBitsAffected = random.randint(1, len(originalRest))
        else:
            numberOfRestBitsAffected = 0
    else:
        numberOfMessageBitsAffected = 0
        numberOfRestBitsAffected = 0
    if bitsNoised != 0:
        numberOfMessageBitsAffected = bitsNoised
    messageToBeNoised = originalCode + originalRest
    crcCodeWithNoise = NoiseGenerator.NoiseGenerator(messageToBeNoised, numberOfMessageBitsAffected).add_noise()
    # restWithNoise = NoiseGenerator.NoiseGenerator(originalRest, numberOfRestBitsAffected).add_noise()
    print("Ciąg bitów z nałożonym szumem:")
    print(crcCodeWithNoise)
    # print("Reszta z nałożonym szumem:")
    # print(restWithNoise)
    print("Dekodowanie przesłanej ramki...")
    # correctMessageReceived = CRCDecoder.CRCDecoder(crcType, crcCodeWithNoise, restWithNoise).code_bits()
    correctMessageReceived = CRCDecoder.CRCDecoder(crcType, crcCodeWithNoise[0:len(originalCode)],
                                                   crcCodeWithNoise[len(originalCode):]).code_bits()
    if correctMessageReceived:
        print("Ramka została przesłana i odczytana poprawnie")
        global ifNoiseNotDetected
        ifNoiseNotDetected += 1
    else:
        print("Podczas przesyłania ramki wystąpił błąd.")
        if requestRepetitions == 1:
            print("\nPonowne przesyłanie ramki...")
            sendCRCCodedMessage(frameIndex, affectedFramesIndexes, crcType, messageLength, originalCode, originalRest,
                                requestRepetitions)


if __name__ == "__main__":
    initialize()
