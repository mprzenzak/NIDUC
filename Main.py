import copy

import CRCCoder
from Generator import *
from ParityBitCoder import ParityBitCoder
import ParityCodeNoise


def initialize():
    mode = int(input(
        "Wybierz rodzaj zabezpieczenia używany podczas kontroli poprawności wysłanego pakietu:\n 1 - Brak zabezpieczenia\n "
        "2 - Bit parzystości\n 3 - Cykliczny kod nadmiarowy\n\tWybór: "))
    frameAmount = int(input("Ile ramek danych chcesz przesłać? "))
    bitChainLength = int(input("Podaj długość ciągu bitów, który zostanie losowo wygenerowany: "))
    dataSize = frameAmount * bitChainLength
    distortionLevel = int(input("Podaj procent przekłamania: "))

    # Tworzy (numpy.ndarray) - zmienione na liste - wypełnioną w losowy sposób zerami i jedynkami o długości równej dataSize


    # Bit parzystości
    if mode == 2:
        message = Generator(dataSize)
        parityCode = ParityBitCoder(message.generate())
        print("Ciąg bitów bez kodowania:")
        print(str(parityCode.parityCoddedMessage))
        print("Ciąg bitów z dodanym bitem parzystości:")
        print(parityCode.code_bits())

        parityCodeWithNoise = ParityCodeNoise.ParityCodeNoise(parityCode.parityCoddedMessage, distortionLevel)
        print("Ciąg bitów z nałożonym szumem:")
        print(parityCodeWithNoise.add_noise())

        # parity_decoded = pbd.ParityBitDecoder(parity.coded_arr)
        # parity_decoded.decoding()
        # print("Parzystoćś bitów z szumem - zdekodowana: ")
        # print(parity_decoded.returnArray())

    # Kod CRC
    elif mode == 3:
        message = Generator(16)
        crcCode = CRCCoder.CRCCoder(message.generate())
        print("Ciąg bitów bez kodowania:")
        print(message.message)
        print("Reszta z dzielenia w CRC 16:")
        print(crcCode.code_bits())

        # parityCodeWithNoise = ParityCodeNoise.ParityCodeNoise(parityCode.parityCoddedMessage, distortionLevel)
        # print("Ciąg bitów z nałożonym szumem:")
        # print(parityCodeWithNoise.add_noise())

if __name__ == "__main__":
    initialize()
