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
        self.maxmaps = 7
        self.maps = list(range(self.maxmaps))
        self.map2ind = {
            'seed': 0,
            'soil': 1,
            'fertilizer': 2,
            'water': 3,
            'light': 4,
            'temperature': 5,
            'humidity': 6,
            'location': 7,
        }

    def visitSeed_list(self, ctx: day05Parser.Seed_listContext):
        # self.seeds = set([int(ct.text) for ct in ctx.seeds])
        self.seeds = []
        if len(ctx.seeds):
            for i in range(0, len(ctx.seeds), 2):
                self.seeds.append(
                    range(int(ctx.seeds[i].text), int(ctx.seeds[i].text) + int(ctx.seeds[i + 1].text) + 1))
        return self.visitChildren(ctx)

    def visitMap(self, ctx: day05Parser.MapContext):
        self.visitChildren(ctx)
        map_ = {
            'destination': int(ctx.destination.text),
            'source': int(ctx.source.text),
            'length': int(ctx.length.text)
        }
        map_['s0'] = map_['source']
        map_['s1'] = map_['source'] + map_['length']
        map_['d0'] = map_['destination']
        map_['d1'] = map_['destination'] + map_['length']
        return map_

    def visitMaps(self, ctx: day05Parser.MapsContext):
        entries = [self.visitMap(entry) for entry in ctx.entries]
        self.maps[self.map2ind[ctx.source.text]] = entries
        return self.visitChildren(ctx)

    def lookup(self, map_no: int, item: int) -> int:
        for entry in self.maps[map_no]:
            if entry['s0'] <= item <= entry['s1']:
                return entry['d0'] + item - entry['s0']
        return item

    @functools.cache
    def search_maps(self, i: int) -> int:
        for j in range(self.maxmaps):
            i = self.lookup(j, i)
        return i

    def visitStart(self, ctx: day05Parser.StartContext):
        self.visitChildren(ctx)
        for rng in self.seeds:
            for seed in rng:
                i = self.search_maps(seed)

                if self.answer is None:
                    self.answer = i
                else:
                    self.answer = min(self.answer, i)

        return self.answer
