from enum import Enum
from time import sleep

class Register(Enum):
    V0 = 0
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4
    V5 = 5
    V6 = 6
    V7 = 7
    V8 = 8
    V9 = 9
    VA = 10
    VB = 11
    VC = 12
    VD = 13
    VE = 14
    VF = 15


fontset = [
	0xF0, 0x90, 0x90, 0x90, 0xF0, 
	0x20, 0x60, 0x20, 0x20, 0x70, 
	0xF0, 0x10, 0xF0, 0x80, 0xF0, 
	0xF0, 0x10, 0xF0, 0x10, 0xF0, 
	0x90, 0x90, 0xF0, 0x10, 0x10, 
	0xF0, 0x80, 0xF0, 0x10, 0xF0, 
	0xF0, 0x80, 0xF0, 0x90, 0xF0, 
	0xF0, 0x10, 0x20, 0x40, 0x40, 
	0xF0, 0x90, 0xF0, 0x90, 0xF0, 
	0xF0, 0x90, 0xF0, 0x10, 0xF0, 
	0xF0, 0x90, 0xF0, 0x90, 0x90, 
	0xE0, 0x90, 0xE0, 0x90, 0xE0, 
	0xF0, 0x80, 0x80, 0x80, 0xF0, 
	0xE0, 0x90, 0x90, 0x90, 0xE0, 
	0xF0, 0x80, 0xF0, 0x80, 0xF0, 
	0xF0, 0x80, 0xF0, 0x80, 0x80  
]


class Display():

    def __init__(self):
        self.display = [[0] * 32] * 64
    
    def clear(self):
        self.display = [[0] * 32] * 64

    def draw(self, x, y, val):
        self.display[x][y] = val
        
class Memory():

    FONT_START_ADDRESS = 0x50
    FONT_END_ADDRESS = 0x50 + len(fontset)
    ROM_START_ADDRESS = 0x200

    def __init__(self, rom):

        #4096 kb of memory (0x000 - 0x1FF is not used aside from storing the fonts, the rest was originally for the interpreter)
        self.memory = [0] * 4096

        #Load fontset into memory
        self.memory[Memory.FONT_START_ADDRESS : Memory.FONT_END_ADDRESS] = fontset

        #Load ROM into memory
        self.ROM_END_ADDRESS = self.load_ROM(rom)
            
    def load_ROM(self, rom):

        #load ROM into memory byte by byte
        with open(rom, 'rb') as f:
            i = 0
            while True:
                byte = f.read(1)
    
                if not byte:
                    break

                self.memory[Memory.ROM_START_ADDRESS + i] = byte
                i += 1

        return Memory.ROM_START_ADDRESS + i

    def debug(self):

        print("ROM DATA")
        for byte in self.memory[Memory.ROM_START_ADDRESS : self.ROM_END_ADDRESS]:
            print(byte)

        print("FONT SET")
        for byte in self.memory[Memory.FONT_START_ADDRESS : Memory.FONT_END_ADDRESS]:
            print(byte)


class CHIP_8():

    def __init__(self, rom):

        #16 8-bit registers
        self.registers = [0] * 16 

        self.index_register = 0
        self.sound_timer = 0
        self.delay_timer = 0
 
        #Program Counter
        self.pc = 0x200

        #4096 kb of memory
        self.memory = Memory(rom)

        """
        NOTE : Might wanna load the rom after the class initialization
               or back in main to handle file errors
        """
        
#       self.memory.load(rom)

        # 16 bit values
        self.stack = [0] * 16

        self.stack_pointer = 0

        self.keypad = [0] * 16
   
        #64 x 32 display
        self.display = Display()

    def setRegister(self, register, num):

        if register is not Register:
            print(f"ERROR: {register} is not a valid register")
            exit()

        if 0x00 < num < 0xFF:
            print(f"ERROR: Number is too big for register")
            exit()

        self.registers[register] = num


    def tick(self):
        if self.delay_timer != 0:
            self.delay_timer -= 1

        if self.sound_timer != 0:
            self.sound_timer -= 0
        else:
            #Add sound tick here later
            pass

    def fetch_instruction(self, addr):  

        instr = self.memory[addr] + 0xF + self.memory[addr+1]

        temp = {
            "full" : instr,
            "upper_byte" : instr >> 8,
            "lower_byte" : instr & 0x00FF,
            "nnn" : (0x0FFF & instr),
            'w' : (0xF000 & instr) >> 12, 
            "x" : (0x0F00 & instr) >> 8,
            "y" : (0x00F0 & instr) >> 4,
            "n" : (0x000F & instr),
        }

        return temp        
        
    def execute(self):

        instr = self.fetch_instruction(self.pc)
    
        match instr['w']:
            case 0x0:
                if instr['lower'] == 0xEE:
                    self.PC = self.stack[-1]
                    self.stack_pointer -= 1
                elif lower == 0xE0:
                    self.display.clear()
            case 0x1:
                #JUMP 
                self.PC = nnn 
            case 0x2:
                #CALL
                self.stack_pointer += 1
                self.stack[-1] = self.PC
                self.PC = nnn
            case 0x3:
                if one == lower:
                    self.PC += 2
            case 0x4:
                if one != lower:
                    self.PC += 2
            case 0x5:
                if two == three:
                    self.PC +=2 
            case = 0x6:
                pass
            case _:
                print(f"ERROR: Invalid instruction {byte}")
                exit()

    def debug(self):
        registers = [f"{i}: {val}" for i, val in enumerate(self.registers)]
        print("Registers")
        print("\n".join(registers))
