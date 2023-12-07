import dataclasses
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


@dataclasses.dataclass
class iRange:
    # inclusive range: [start, stop] with fixed step size 1
    # normally start<=stop.
    start: int
    stop: int

    def isEmpty(self):
        return self.start > self.stop

    def __len__(self):
        return 0 if self.isEmpty() else self.stop - self.start + 1

    @staticmethod
    def emptyIRange():
        return iRange(0, -1)

    def __add__(self, shift_):
        if isinstance(shift_, int):
            return iRange(self.start + shift_, self.stop + shift_)


def IntersectionWithTransformation(a: iRange, b: iRange, tx_shift: int) -> List[iRange]:
    # always returns 3 iRanges, but some of them can be None

    # case 0: empty ranges
    if a.isEmpty() or b.isEmpty():
        return [None, None, None]

    # case 1: identical ranges
    if a == b:
        return [None, a + tx_shift, None]

    overlap = iRange(max(a.start, b.start), min(a.stop, b.stop))
    if overlap.isEmpty():
        # case 2: non-overlapping ranges
        return [None, a, None]
    # past this point, there must be some non-trivial overlap between a and b
    overlap_shifted = iRange(overlap.start, overlap.stop) + tx_shift

    # case 3: a is entirely contained in b
    if b.start <= a.start and a.stop <= b.stop:
        return [None, overlap_shifted, None]

    # case 6: b is entirely contained in a. a is split into 3 pieces: before, overlap, and after
    if a.start < b.start and b.stop < a.stop:
        before = iRange(a.start, b.stop - 1)
        after = iRange(b.stop + 1, a.stop)
        return [before, overlap_shifted, after]

    # case 5: a begins before b and also overlaps it. part of a is not transformed.
    if a.start < b.start and a.stop <= b.stop:
        before = iRange(a.start, b.start - 1)
        return [before, overlap_shifted, None]

    # case 4: a ends after b and also overlaps it. part of a is not transformed.
    if a.start >= b.start and a.stop > b.stop:
        after = iRange(b.stop + 1, a.stop)
        return [None, overlap_shifted, after]

    return [None, overlap_shifted, None]


def IntersectionWithTransformationTests():
    a = iRange(50, 3)
    assert a.isEmpty()

    a = iRange(51, 60)
    assert len(a) == 10
    assert a + (-50) == iRange(1, 10)

    b = iRange(55, 65)
    before, overlap_shifted, after = IntersectionWithTransformation(a, b, -50)
    assert len(overlap_shifted) == 6
    assert before == iRange(51, 54)
    assert overlap_shifted == iRange(5, 10)
    assert after is None

    c = iRange(1000, 3000)
    before, overlap_shifted, after = IntersectionWithTransformation(a, c, 0)
    assert before is None
    assert overlap_shifted == a
    assert after is None

    before, overlap_shifted, after = IntersectionWithTransformation(b, a, 0)
    assert before is None
    assert overlap_shifted == iRange(55, 60)
    assert after == iRange(61, 65)

    i1 = iRange(10, 10)
    i2 = iRange(20, 20)
    assert len(i1) == 1
    assert i1 + 10 == i2

    before, overlap_shifted, after = IntersectionWithTransformation(i1, i2, 10)
    assert before is None
    assert overlap_shifted == i1
    assert after is None

    before, overlap_shifted, after = IntersectionWithTransformation(i1, i1, 0)
    assert before is None
    assert overlap_shifted == i1
    assert after is None


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
        IntersectionWithTransformationTests()

    def visitSeed_list(self, ctx: day05Parser.Seed_listContext):
        # self.seeds = set([int(ct.text) for ct in ctx.seeds])
        self.seeds = []
        if len(ctx.seeds):
            for i in range(0, len(ctx.seeds), 2):
                self.seeds.append(
                    iRange(int(ctx.seeds[i].text), int(ctx.seeds[i].text) + int(ctx.seeds[i + 1].text)))
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

    def search_ranges(self, a: iRange) -> iRange:
        active_ranges = [a]
        for j in range(self.maxmaps):
            if not len(active_ranges) > 0:
                return []

            i = self.lookup(j, i)
        return i

    def visitStart(self, ctx: day05Parser.StartContext):
        self.visitChildren(ctx)
        for rng in self.seeds:
            soln = self.search_ranges(rng)
            # for seed in rng:
            #     i = self.search_maps(seed)

            if self.answer is None:
                self.answer = i
            else:
                self.answer = min(self.answer, i)

        return self.answer
