from chip8 import CHIP_8
from argparse import ArgumentParser

parser = ArgumentParser(description="Shitty CHIP-8 Emulator")
parser.add_argument("ROM")

args = parser.parse_args()

if __name__ == '__main__':
 
    chip8 = CHIP_8(args.ROM)
    chip8.memory.loadrom(args.ROM)
    chip8.memory.debug()

