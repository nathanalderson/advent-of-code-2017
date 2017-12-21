#! /usr/bin/env python3
import collections

def main():
    test_instructions = [
        "set a 1", "add a 2", "mul a a", "mod a 5", "snd a",
        "set a 0", "rcv a", "jgz a -1", "set a 1", "jgz a -2"
    ]
    assert play(test_instructions) == 4
    instructions = [line.strip() for line in open("input", "r").readlines()]
    result = play(instructions)
    print("part 1 =", result)

def play(instructions):
    registers = collections.defaultdict(int)
    last_freq = 0
    pc = 0

    def val_or_reg(reg):
        try:
            val = int(reg)
        except:
            val = registers[reg]
        return val

    while True:
        try:
            op, regs = instructions[pc].split(" ", maxsplit=1)
            # print("*****", pc, op, regs)
        except IndexError:
            break
        if op == "set":
            reg1, reg2 = regs.split()
            registers[reg1] = val_or_reg(reg2)
            # print("set", reg1, reg2)
            # print(registers)
            pc += 1
        elif op == "add":
            reg1, reg2 = regs.split()
            registers[reg1] += val_or_reg(reg2)
            # print("add", reg1, reg2)
            # print(registers)
            pc += 1
        elif op == "mul":
            reg1, reg2 = regs.split()
            registers[reg1] *= val_or_reg(reg2)
            # print("mul", reg1, reg2)
            # print(registers)
            pc += 1
        elif op == "mod":
            reg1, reg2 = regs.split()
            try:
                registers[reg1] %= val_or_reg(reg2)
            except ZeroDivisionError:
                pass
            # print("mod", reg1, reg2)
            # print(registers)
            pc += 1
        elif op == "snd":
            reg = regs
            last_freq = val_or_reg(reg)
            # print("snd", reg)
            # print(registers)
            # print(last_freq)
            pc += 1
        elif op == "rcv":
            reg = regs
            # print("rcv", reg)
            # print(registers)
            # print(last_freq)
            if val_or_reg(reg) != 0:
                return last_freq
            pc += 1
        elif op == "jgz":
            reg1, reg2 = regs.split()
            # print("jgz", reg1, reg2)
            # print(registers)
            if val_or_reg(reg1) > 0:
                pc += val_or_reg(reg2)
            else:
                pc += 1

if __name__ == "__main__":
    main()
