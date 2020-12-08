from aocd import data as input_data
from enum import Enum


class ProgramStatus(Enum):
    LOOP = 1
    IN_PROGRESS = 2
    FINISHED = 3


class Program:
    def __init__(self, data):
        self.cache = set()
        self.data = data
        self.accumulator = 0
        self.position = 0

    def acc(self, x):
        self.accumulator += x

    def jmp(self, x):
        self.position += x - 1

    def nop(self, x):
        pass

    def step(self):
        if self.position in self.cache:
            return ProgramStatus.LOOP
        self.cache.add(self.position)

        if self.position >= len(self.data):
            return ProgramStatus.FINISHED

        cmd, x = self.data[self.position].split(' ')
        eval(f'self.{cmd}({x})')
        self.position += 1
        return ProgramStatus.IN_PROGRESS


def parse_data():
    return [x for x in input_data.split('\n')]


def solve_a(data):
    p = Program(data)
    while True:
        status = p.step()
        if status == ProgramStatus.LOOP:
            return p.accumulator


def solve_b(data):
    for change_from, change_to in [('jmp', 'nop'), ('nop', 'jmp')]:
        for i in range(len(data)):
            if change_from not in data[i]:
                continue

            cdata = [x for x in data]
            cdata[i] = cdata[i].replace(change_from, change_to)

            p = Program(cdata)
            while True:
                status = p.step()
                if status == ProgramStatus.FINISHED:
                    return p.accumulator
                if status == ProgramStatus.LOOP:
                    break


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
