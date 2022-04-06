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

    framesTab = []

    for i in range(frameAmount):
        framesTab.append(0)

    affectedFramesIndexes = []
    counter = floor(distortionLevel / 100 * frameAmount)
    for i in range(counter):
        randomIndex = random.randint(0, frameAmount)
        if randomIndex in affectedFramesIndexes:
            counter += 1
        else:
            affectedFramesIndexes.append(randomIndex)

    # Bit parzystości
    if mode == 2:
        bitChainLength = int(input("Podaj długość ciągu bitów, który zostanie losowo wygenerowany dla każdej ramki: "))
        dataSize = frameAmount * bitChainLength
        # Tworzy listę wypełnioną w losowy sposób zerami i jedynkami o długości równej dataSize
        message = Generator(dataSize)
        parityCode = ParityBitCoder(message.generate())
        print("Ciąg bitów bez kodowania:")
        print(str(parityCode.parityCoddedMessage))
        print("Ciąg bitów z dodanym bitem parzystości:")
        print(parityCode.code_bits())

        parityCodeWithNoise = NoiseGenerator.NoiseGenerator(parityCode.parityCoddedMessage, distortionLevel)
        print("Ciąg bitów z nałożonym szumem:")
        print(parityCodeWithNoise.add_noise())

        print("Ciąg bitów po zdekodowaniu:")
        parityCodeDecoded = ParityBitDecoder.ParityBitDecoder(parityCodeWithNoise.messageWithNoise).code_bits()
        # print("SIUUUUUUP")
        # print(parityCodeDecoded)
        # parity_decoded = pbd.ParityBitDecoder(parity.coded_arr)
        # parity_decoded.decoding()
        # print("Parzystoćś bitów z szumem - zdekodowana: ")
        # print(parity_decoded.returnArray())

    # Kod CRC
    elif mode == 3:
        crcType = int(input("Podaj typ kodu CRC, który chcesz użyć dla wszystkich ramek:\n - 4\n - 8\n - 16\n - 32\n"))
        for frameIndex in range(frameAmount):
            print("Ramka " + str(frameIndex+1) + ":")
            message = Generator(crcType).generate()
            originalCode = message
            crcCode = CRCCoder.CRCCoder(crcType, message)
            originalRest = crcCode.code_bits()
            print("Ciąg bitów bez kodowania:")
            print(originalCode)
            # print(CRCCoder.CRCCoder.crcCoddedMessage)
            print("Reszta z dzielenia w CRC " + str(crcType) + ":")
            print(originalRest)
            if frameIndex in affectedFramesIndexes:
                numberOfBitsAffected = random.randint(1, crcType)
            else:
                numberOfBitsAffected = 0
            crcCodeWithNoise = NoiseGenerator.NoiseGenerator(originalCode, numberOfBitsAffected).add_noise()
            print("Ciąg bitów z nałożonym szumem:")
            print(crcCodeWithNoise)
            print("Dekodowanie przesłanej ramki...")
            # Jeżeli kod będzie poprawny, to zostanie zwrócona pusta lista
            correctMessageReceived = CRCDecoder.CRCDecoder(crcType, crcCodeWithNoise, originalRest).code_bits()
            # restCheck = CRCDecoder.CRCDecoder(crcType, [1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1], originalRest).code_bits()
            if correctMessageReceived:
                print("Ramka została przesłana i odczytana poprawnie")
            else:
                print("Podczas przesyłania ramki wystąpił błąd")
            print()

if __name__ == "__main__":
    initialize()
