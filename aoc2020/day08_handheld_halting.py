import sys
import re
sys.path.append('../')
from util import read_file, assert_equals

class Op:
    def __init__(self, bootcode):
        self.bootcode = bootcode
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, op):
        if self.is_responsible_for(op):
            self.execute(op)
        else:
            next_handler = self.next_handler
            if next_handler:
                next_handler.handle(op)

    def parse_op(self, op):
        return op.split(" ")

    def parse_op_name(self, op):
        return self.parse_op(op)[0]

    def parse_op_argument(self, op):
        return int(self.parse_op(op)[1])

    def is_responsible_for(self, op):
        return False

class AccumulateOp(Op):
    def __init__(self, bootcode):
        Op.__init__(self, bootcode)
        self.value = 0

    def is_responsible_for(self, op):
        return "acc" == self.parse_op_name(op)

    def execute(self, op):
        self.value += self.parse_op_argument(op)
        self.bootcode.ip += 1

class JumpOp(Op):
    def __init__(self, bootcode):
        Op.__init__(self, bootcode)

    def is_responsible_for(self, op):
        return "jmp" == self.parse_op_name(op)

    def execute(self, op):
        self.bootcode.ip += self.parse_op_argument(op)

class NoOp(Op):
    def __init__(self, bootcode):
        Op.__init__(self, bootcode)

    def is_responsible_for(self, op):
        return "nop" == self.parse_op_name(op)

    def execute(self, op):
        # Argument is ignored
        self.bootcode.ip += 1

class BootCode:
    def __init__(self, memory):
        self.memory = memory
        self.ip = 0
        self.acc = AccumulateOp(self)
        self.jmp = JumpOp(self)
        self.nop = NoOp(self)
        self.acc.set_next(self.jmp)
        self.jmp.set_next(self.nop)
        self.op_handler = self.acc
        self.repeated = False
        self.completed = False

    def run(self):
        self.visited_ips = set()
        while True:
            ip = self.ip
            if ip in self.visited_ips:
                self.repeated = True
                break
            op_at_ip = self.memory[self.ip]
            self.op_handler.handle(op_at_ip)
            self.visited_ips.add(ip)
            if self.ip == len(self.memory):
                self.completed = True
                break
        return self.acc.value

def part1(lines):
    code = BootCode(lines)
    acc = code.run()
    return acc

def part2(lines):
    nop_op = NoOp(None)
    jmp_op = JumpOp(None)
    nops = [(i, "jmp") for i, e in enumerate(lines) if nop_op.is_responsible_for(e)]
    jmps = [(i, "nop") for i, e in enumerate(lines) if jmp_op.is_responsible_for(e)]
    for i, replacement in nops+jmps:
        memory = lines.copy()
        memory[i] = replacement + memory[i][3:]
        code = BootCode(memory)
        acc = code.run()
        if code.completed:
            return acc

sample = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".split("\n")
assert_equals(part1(sample), 5)
assert_equals(part2(sample), 8)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
