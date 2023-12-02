import sys
from antlr4 import *
from gen.day02Lexer import day02Lexer
from gen.day02Parser import day02Parser
from gen.day02Visitor import day02Visitor

from dataclasses import dataclass
from typing import List, Dict
import datetime
import time

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
    def visitColors(self, ctx:day02Parser.ColorsContext):
        #print(f'{ctx.color} = {ctx.count}')
        return [ctx.color.text, int(ctx.count.text)]

    # Visit a parse tree produced by day02Parser#draw.
    def visitDraw(self, ctx:day02Parser.DrawContext):
        return dict([self.visit(ctx.getChild(i)) for i in range(0, ctx.getChildCount())])

    # Visit a parse tree produced by day02Parser#game.
    def visitGame(self, ctx:day02Parser.GameContext):
        for i in range(0, ctx.getChildCount(), 1):
            draw = self.visit(ctx.getChild(i))
            if draw:
                if not isWithinLimits(draw, self.limits):
                    break
                print(f'game {ctx.id_.text} was {draw}')
        else:
            self.total += int(ctx.id_.text)

        # return self.visitChildren(ctx)


