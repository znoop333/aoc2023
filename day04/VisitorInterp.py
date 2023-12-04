import sys
from antlr4 import *
from gen.day04Lexer import day04Lexer
from gen.day04Parser import day04Parser
from gen.day04Visitor import day04Visitor

from dataclasses import dataclass
from typing import List, Dict
import datetime
import time
from math import prod
from collections import defaultdict


class VisitorInterp(day04Visitor):

    def __init__(self):
        self.total = 0

    # Visit a parse tree produced by day04Parser#card.
    def visitCard(self, ctx: day04Parser.CardContext):
        have = set([int(ctx.have[i].text) for i in range(len(ctx.have))])
        win = set([int(ctx.win[i].text) for i in range(len(ctx.win))])
        return len(have.intersection(win))


    # Visit a parse tree produced by day04Parser#start.
    def visitStart(self, ctx: day04Parser.StartContext):
        originals = {}
        for i in range(ctx.getChildCount()):
            win_ = self.visit(ctx.getChild(i))
            if win_:
                originals[int(ctx.getChild(i).id_.text)] = self.visit(ctx.getChild(i))

        copies = defaultdict(int)
        need_to_visit = list(originals.keys())
        while len(need_to_visit):
            visit = need_to_visit.pop()
            if visit in copies:
                1


        1

    # Visit a parse tree produced by day04Parser#start.
    def visitStart_part1(self, ctx: day04Parser.StartContext):
        for i in range(ctx.getChildCount()):
            count_won = self.visit(ctx.getChild(i))
            if count_won:
                self.total += count_won

    def visitCard_part1(self, ctx: day04Parser.CardContext):
        have = set([int(ctx.have[i].text) for i in range(len(ctx.have))])
        win = set([int(ctx.win[i].text) for i in range(len(ctx.win))])
        count_won = len(have.intersection(win))
        return 2 ** (count_won-1) if count_won > 0 else 0
