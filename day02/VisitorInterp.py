import sys
from antlr4 import *
from gen.day02Lexer import day02Lexer
from gen.day02Parser import day02Parser
from gen.day02Visitor import day02Visitor

from dataclasses import dataclass
from typing import List, Dict
import datetime
import time
from math import prod


def minLimitReduction(draws: List[Dict]) -> Dict:
    # the argument is a list of dicts like: [{'green': 2, 'blue': 5}, {'blue': 15, 'red': 3}]
    # return a dict containing the maximum of each individual color as another dict, e.g.,
    # {'green': 2, 'blue': 15, 'red': 3}. this is the minimum Limit to play the game.
    limit = {}
    for draw in draws:
        for color, count in draw.items():
            limit[color] = max(count, limit.get(color, 0))

    return limit


def isWithinLimits(draw: Dict, limits: Dict) -> bool:
    # both arguments are of the form: {'green': 2, 'blue': 15, 'red': 3}
    # return True if all the values in draw are <= the values in limits
    for color, count in draw.items():
        if color in limits and count > limits[color]:
            return False
    return True


class VisitorInterp(day02Visitor):

    def __init__(self, limits: Dict):
        self.limits = limits
        self.total = 0

    # Visit a parse tree produced by day02Parser#color_spec.
    def visitColors(self, ctx: day02Parser.ColorsContext):
        # print(f'{ctx.color} = {ctx.count}')
        return [ctx.color.text, int(ctx.count.text)]

    # Visit a parse tree produced by day02Parser#draw.
    def visitDraw(self, ctx: day02Parser.DrawContext):
        return dict([self.visit(ctx.getChild(i)) for i in range(0, ctx.getChildCount())])

    # Visit a parse tree produced by day02Parser#game.
    def visitGame(self, ctx: day02Parser.GameContext):
        # part 2:
        draws = []
        for i in range(0, ctx.getChildCount(), 1):
            draw = self.visit(ctx.getChild(i))
            if draw:
                draws.append(draw)

        limit = minLimitReduction(draws)
        cube_power = prod(limit.values())
        print(f'Game {ctx.id_.text} cube_power = {cube_power}')
        return cube_power

    def visitStart(self, ctx: day02Parser.StartContext):
        self.total = 0
        for i in range(0, ctx.getChildCount(), 1):
            cube_power = self.visit(ctx.getChild(i))
            if cube_power:
                self.total += cube_power
        print(f'Total cube_power {self.total}')

    def visitGame_part1(self, ctx: day02Parser.GameContext):

        for i in range(0, ctx.getChildCount(), 1):
            draw = self.visit(ctx.getChild(i))
            if draw:
                if not isWithinLimits(draw, self.limits):
                    print(f'Disqualified game {ctx.id_.text} by {draw}')
                    break
        else:
            print(f'Game {ctx.id_.text} counted!')
            self.total += int(ctx.id_.text)

        # return self.visitChildren(ctx)
