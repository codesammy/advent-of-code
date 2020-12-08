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
        op_name, op_argument = op.split(" ")
        if self.is_responsible_for(op_name):
            self.execute(int(op_argument))
        else:
            next_handler = self.next_handler
            if next_handler:
                next_handler.handle(op)

    def is_responsible_for(self, op):
        return False

class AccumulateOp(Op):
    def __init__(self, bootcode):
        Op.__init__(self, bootcode)
        self.value = 0

    def is_responsible_for(self, name):
        return "acc" == name

    def execute(self, argument):
        self.value += argument
        self.bootcode.ip += 1

class JumpOp(Op):
    def __init__(self, bootcode):
        Op.__init__(self, bootcode)

    def is_responsible_for(self, name):
        return "jmp" == name

    def execute(self, argument):
        self.bootcode.ip += argument

class NoOp(Op):
    def __init__(self, bootcode):
        Op.__init__(self, bootcode)

    def is_responsible_for(self, name):
        return "nop" == name

    def execute(self, argument):
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

    def accumulate_until_repeat(self):
        self.visited_ips = set()
        while True:
            ip = self.ip
            if ip in self.visited_ips:
                break
            op_at_ip = self.memory[self.ip]
            self.op_handler.handle(op_at_ip)
            self.visited_ips.add(ip)
        return self.acc.value

def part1(lines):
    code = BootCode(lines)
    acc = code.accumulate_until_repeat()
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

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
