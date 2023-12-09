import dataclasses
import sys
from antlr4 import *
from gen.day08Lexer import day08Lexer
from gen.day08Parser import day08Parser
from gen.day08Visitor import day08Visitor

from dataclasses import dataclass
from typing import List, Dict
import datetime
import time
from math import prod
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

    def visitStart(self, ctx: day08Parser.StartContext):
        self.visitChildren(ctx)
        self.instructions = [item for item in ctx.lr.text]
        self.answer = self.walk(self.root, 0, -1)

        return self.answer

    def visitNode(self, ctx: day08Parser.NodeContext):
        if self.root is None:
            self.root = ctx.base.text
        self.graph[ctx.base.text] = (ctx.left.text, ctx.right.text)
        return self.visitChildren(ctx)
