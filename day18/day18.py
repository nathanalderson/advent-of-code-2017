#! /usr/bin/env python3
import collections
import queue
import threading
import time

def main():
    test_instructions = [
        "set a 1", "add a 2", "mul a a", "mod a 5", "snd a",
        "set a 0", "rcv a", "jgz a -1", "set a 1", "jgz a -2"
    ]
    assert play1(test_instructions) == 4
    instructions = [line.strip() for line in open("input", "r").readlines()]
    result = play1(instructions)
    print("part 1 =", result)
    q1, q2 = queue.Queue(), queue.Queue()
    p0 = Program(instructions, 0, queue.Queue(), queue.Queue())
    p1 = Program(instructions, 1, p0.rcv_queue, p0.send_queue)
    monitor = Monitor(p0, p1)
    p0.start()
    p1.start()
    print("starting monitor...")
    monitor.start()
    p0.join()
    p1.join()
    monitor.join()
    print("part 2 =", p1.sent)

class Monitor(threading.Thread):
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        super().__init__()

    def run(self):
        while True:
            if self.p0.blocking and self.p1.blocking:
                print("deadlock")
                print("p1 sent", self.p1.sent)
                self.p0.stop()
                self.p1.stop()
                return
            time.sleep(0.1)

class Program(threading.Thread):
    def __init__(self, instructions, prog_num, send_queue, rcv_queue):
        self.instructions = instructions
        self.prog_num = prog_num
        self.send_queue = send_queue
        self.rcv_queue = rcv_queue
        self.pc = 0
        self.sent = 0
        self.registers = collections.defaultdict(int)
        self.registers['p'] = self.prog_num
        self.blocking = False
        self.terminated = False
        super().__init__()

    def val_or_reg(self, reg):
        try:
            val = int(reg)
        except:
            val = self.registers[reg]
        return val

    def run(self):
        print("starting prog", self.prog_num)
        while True:
            time.sleep(0)
            if self.terminated:
                break
            try:
                op, regs = self.instructions[self.pc].split(" ", maxsplit=1)
                print("prog", self.prog_num, self.pc, op, regs)
            except IndexError:
                break
            if op == "set":
                reg1, reg2 = regs.split()
                self.registers[reg1] = self.val_or_reg(reg2)
                self.pc += 1
            elif op == "add":
                reg1, reg2 = regs.split()
                self.registers[reg1] += self.val_or_reg(reg2)
                self.pc += 1
            elif op == "mul":
                reg1, reg2 = regs.split()
                self.registers[reg1] *= self.val_or_reg(reg2)
                self.pc += 1
            elif op == "mod":
                reg1, reg2 = regs.split()
                self.registers[reg1] %= self.val_or_reg(reg2)
                self.pc += 1
            elif op == "snd":
                reg = regs
                self.send_queue.put(self.val_or_reg(reg))
                self.sent += 1
                # print("program", self.prog_num, "sent", self.sent)
                self.pc += 1
            elif op == "rcv":
                reg = regs
                self.blocking = True
                self.registers[reg] = self.rcv_queue.get()
                self.blocking = False
                self.pc += 1
            elif op == "jgz":
                reg1, reg2 = regs.split()
                if self.val_or_reg(reg1) > 0:
                    self.pc += self.val_or_reg(reg2)
                else:
                    self.pc += 1

    def stop(self):
        self.terminated = True

def play1(instructions):
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
        except IndexError:
            break
        if op == "set":
            reg1, reg2 = regs.split()
            registers[reg1] = val_or_reg(reg2)
            pc += 1
        elif op == "add":
            reg1, reg2 = regs.split()
            registers[reg1] += val_or_reg(reg2)
            pc += 1
        elif op == "mul":
            reg1, reg2 = regs.split()
            registers[reg1] *= val_or_reg(reg2)
            pc += 1
        elif op == "mod":
            reg1, reg2 = regs.split()
            registers[reg1] %= val_or_reg(reg2)
            pc += 1
        elif op == "snd":
            reg = regs
            last_freq = val_or_reg(reg)
            pc += 1
        elif op == "rcv":
            reg = regs
            if val_or_reg(reg) != 0:
                return last_freq
            pc += 1
        elif op == "jgz":
            reg1, reg2 = regs.split()
            if val_or_reg(reg1) > 0:
                pc += val_or_reg(reg2)
            else:
                pc += 1

if __name__ == "__main__":
    main()
