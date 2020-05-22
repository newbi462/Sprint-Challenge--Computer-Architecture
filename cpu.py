"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001
PUSH = 0b01000101
SP = 7
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #pass

        #Registers
        #self.registers = [0] * 8 # Registers | 8 general-purpose 8-bit numeric registers R0-R7.
        self.reg = [0] * 8# exisisting code NOT IN SPEC DOC uses self.reg???
        #R5 is reserved as the interrupt mask (IM)
        #R6 is reserved as the interrupt status (IS)
        #R7 is reserved as the stack pointer (SP)

        #Internal Registers
        self.pc = 0 #PC: Program Counter, address of the currently executing instruction
        #IR: Instruction Register, contains a copy of the currently executing instruction
        ##FROM STEP 2: You don't need to add the MAR or MDR to your CPU class #MAR: Memory Address Register, holds the memory address we're reading or writing
        ##FROM STEP 2: You don't need to add the MAR or MDR to your CPU class #MDR: Memory Data Register, holds the value to write or the value just read
        #FL: Flags, see below

        #Memory
        #self.memory = [0] * 256 #Memory | The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256 #per line 49 ERROR name already defined but not given in spec
        #Stack

        #clean table
        self.branchtable = {}
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[MUL] = self.MUL
        self.branchtable[HLT] = self.HLT
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        ##make sure there is a file passed
        if len(sys.argv) != 2:
            print('PLEASE USE ls8.py path_to_file_to_run')
            sys.exit(1)

        """program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1"""
        ## Reaplace with import logic
        file_to_run = sys.argv[1]
        try:
            #pass
            with open(file_to_run) as program:
                #pass
                for line in program:
                    if line.split('#')[0].strip() == "":
                        continue
                    #print(int(line.split('#')[0].strip(), 2))
                    self.ram[address] = int(line.split('#')[0].strip(), 2)
                    address += 1
        except FileNotFoundError:
            #pass
            print("it failed")
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def LDI(self):
        register = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[register] = value
        self.pc += 3

    def PRN(self):
        register = self.ram_read(self.pc+1)
        print(self.reg[register])
        self.pc += 2

    def HLT(self):
        sys.exit(0)

    def MUL(self):
        register = self.ram_read(self.pc + 1)
        register2 = self.ram_read(self.pc + 2)
        self.reg[register] *= self.reg[register2]
        self.pc += 3

    def PUSH(self):
        self.reg[SP] -= 1
        reg_num = self.ram_read(self.pc+1)
        val = self.reg[reg_num]
        top_of_stack_addr = self.reg[SP]
        self.ram[top_of_stack_addr] = val
        self.pc += 2

    def POP(self):
        #print("should pop")
        # Copy the value from the address pointed to by SP to the given register.
        reg_num = self.ram_read(self.pc+1)
        self.reg[reg_num] = self.ram_read(self.reg[SP])
        #Increment SP
        self.reg[SP] += 1
        self.pc += 2

    def CALL(self):
        #pass
        print("is call")

    def RET(self):
        pass

    def run(self):
        """Run the CPU."""
        #pass
        print(sys.argv)
        self.pc = 0
        halted = False

        while not halted:
            #print(self.ram_read(self.pc))
            """if 0b10000010 == self.ram_read(self.pc):
                self.LDI()
            elif 0b01000111 == self.ram_read(self.pc):
                self.PRN()
            elif 0b10100010 == self.ram_read(self.pc):
                self.MUL()
            elif 0b00000001 == self.ram_read(self.pc):
                self.HLT()"""
            ###MAKE CLEAN
            option = self.ram_read(self.pc)# use var to get around try catchs
            if option in self.branchtable:
                self.branchtable[option]()
            else:
                print("you break it you buy it")
                sys.exit(1)




    #should accept the address to read and return the value stored there
    def ram_read(self, address_to_read):
        #pass
        return self.ram[address_to_read]

    # should accept a value to write, and the address to write it to.
    def ram_write(self, value_to_write, address_to_write_it_to):
        #pass
        self.ram[address_to_write_it_to] = value_to_write
