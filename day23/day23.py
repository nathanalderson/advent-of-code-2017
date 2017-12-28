#! /usr/bin/env python3
import collections
import time

def main():
    # instructions = read_instructions("input")
    # prog = Program(instructions)
    # prog.run()
    # print("part 1 =", prog.muls)
    instructions2 = read_instructions("optimized")
    prog2 = Program(instructions2, regs = {"a":1})
    prog2.run()
    print("part 2 =", prog2.registers['h'])

def read_instructions(filename):
    return [line.strip() for line in open(filename, "r").readlines() if line.strip() != ""]

class Program():
    def __init__(self, instructions, regs = None):
        self.instructions = instructions
        self.pc = 0
        self.muls = 0
        self.registers = collections.defaultdict(int)
        regs = regs or {}
        for k,v in regs.items():
            self.registers[k] = v

    def val_or_reg(self, reg):
        try:
            val = int(reg)
        except:
            val = self.registers[reg]
        return val

    def run(self):
        while True:
            time.sleep(0.1)
            try:
                op, regs = self.instructions[self.pc].split(" ", maxsplit=1)
                print(self.pc, op, regs, end="")
            except IndexError:
                break
            if op == "set":
                reg1, reg2 = regs.split()
                self.registers[reg1] = self.val_or_reg(reg2)
                self.pc += 1
            elif op == "sub":
                reg1, reg2 = regs.split()
                self.registers[reg1] -= self.val_or_reg(reg2)
                self.pc += 1
            elif op == "mul":
                reg1, reg2 = regs.split()
                self.registers[reg1] *= self.val_or_reg(reg2)
                self.muls += 1
                self.pc += 1
            elif op == "jnz":
                reg1, reg2 = regs.split()
                if self.val_or_reg(reg1) != 0:
                    self.pc += self.val_or_reg(reg2)
                else:
                    self.pc += 1
            print("->", self.registers)

if __name__ == "__main__":
    main()
