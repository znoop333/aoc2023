import dataclasses
import sys
from antlr4 import *
from gen.day08Lexer import day08Lexer
from gen.day08Parser import day08Parser
from gen.day08Visitor import day08Visitor
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import datetime
import time
from math import prod, lcm
from collections import defaultdict
import functools


class VisitorInterp(day08Visitor):
    def __init__(self):
        self.root = None
        self.graph = dict()
        self.instructions = []
        self.answer = None

    def walk(self, current_node, depth, instruction_index):
        if current_node == 'ZZZ':
            return depth

        instruction_index = (instruction_index + 1) % len(self.instructions)
        print(f'at node {current_node}, instruction {self.instructions[instruction_index]} with depth {depth}')
        if self.instructions[instruction_index] == 'L':
            return self.walk(self.graph[current_node][0], depth + 1, instruction_index)
        return self.walk(self.graph[current_node][1], depth + 1, instruction_index)

    def walk_iter(self, start_):
        current_node = start_
        steps = 0
        instruction_index = 0

        while current_node != 'ZZZ':
            # if steps % 100 == 0:
            #     print(f'at node {current_node}, instruction {self.instructions[instruction_index]} with steps {steps}')
            if self.instructions[instruction_index] == 'L':
                current_node = self.graph[current_node][0]
            else:
                current_node = self.graph[current_node][1]
            steps += 1
            instruction_index = (instruction_index + 1) % len(self.instructions)
        return steps

    def ghost_starting_nodes(self):
        return [k for k in self.graph if k.endswith('A')]

    def ghost_walk(self, starting_node):
        current_node = starting_node
        steps = 0
        visited = []
        solutions = []
        instruction_index = 0

        while len(solutions) < 10:
            # if steps % 100 == 0:
            # print(f'at node {current_node}, instruction {self.instructions[instruction_index]} with steps {steps}')
            if current_node.endswith('Z'):
                solutions.append(steps)

            if self.instructions[instruction_index] == 'L':
                current_node = self.graph[current_node][0]
            else:
                current_node = self.graph[current_node][1]
            steps += 1
            instruction_index = (instruction_index + 1) % len(self.instructions)

        return solutions

    def visitStart(self, ctx: day08Parser.StartContext):
        self.visitChildren(ctx)
        self.instructions = [item for item in ctx.lr.text]
        # self.answer = self.walk_iter('AAA')

        # part 2: parallel ghost walking from **A to **Z loops
        starting_nodes = self.ghost_starting_nodes()
        some_solutions = {}
        periods = {}
        all_periods = []
        for node in starting_nodes:
            some_solutions[node] = self.ghost_walk(node)
            periods[node] = np.diff(np.array(some_solutions[node]))
            all_periods.append(periods[node][0])

        self.answer = lcm(*all_periods)

        return self.answer

    def visitNode(self, ctx: day08Parser.NodeContext):
        if self.root is None:
            self.root = ctx.base.text
        self.graph[ctx.base.text] = (ctx.left.text, ctx.right.text)
        return self.visitChildren(ctx)
