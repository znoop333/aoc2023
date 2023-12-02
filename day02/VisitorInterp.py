import sys
from antlr4 import *
from gen.day02Lexer import day02Lexer
from gen.day02Parser import day02Parser
from gen.day02Visitor import day02Visitor

from dataclasses import dataclass
from typing import List
import datetime
import time


class VisitorInterp(day02Visitor):

    # Visit a parse tree produced by day02Parser#color_spec.
    def visitColor_spec(self, ctx:day02Parser.Color_specContext):
        print(f'{ctx.color} = {ctx.count}')
        return [ctx.color.text, int(ctx.count.text)]


    # Visit a parse tree produced by day02Parser#start.
    def visitStart(self, ctx:day02Parser.StartContext):
        for i in range(0, ctx.getChildCount(), 1):
            self.visit(ctx.getChild(i))
        return self.visitChildren(ctx)

