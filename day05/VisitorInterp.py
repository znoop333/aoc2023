import sys
from antlr4 import *
from gen.day05Lexer import day05Lexer
from gen.day05Parser import day05Parser
from gen.day05Visitor import day05Visitor

from dataclasses import dataclass
from typing import List, Dict
import datetime
import time
from math import prod
from collections import defaultdict
import functools


class VisitorInterp(day05Visitor):
    def __init__(self):
        self.seeds = set()
        self.answer = None
        self.maps = dict()

    def visitSeed_list(self, ctx: day05Parser.Seed_listContext):
        self.seeds = set([int(ct.text) for ct in ctx.seeds])
        return self.visitChildren(ctx)

    def visitMap(self, ctx: day05Parser.MapContext):
        self.visitChildren(ctx)
        return {
            'destination': int(ctx.destination.text),
            'source': int(ctx.source.text),
            'length': int(ctx.length.text)
        }

    def visitMaps(self, ctx: day05Parser.MapsContext):
        entries = [self.visitMap(entry) for entry in ctx.entries]
        self.maps[ctx.source.text] = {ctx.destination.text: entries}
        return self.visitChildren(ctx)
