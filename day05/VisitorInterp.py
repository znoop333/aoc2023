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

import d5p2_portion

# PART2 = True
PART2 = False


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
    self.ind2map = {v: k for k, v in self.map2ind.items()}

  def visitSeed_list(self, ctx: day05Parser.Seed_listContext):
    self.seeds = []
    if len(ctx.seeds):
      if not PART2:
        # part 1
        for i in range(len(ctx.seeds)):
          self.seeds.append(d5p2_portion.make_single(int(ctx.seeds[i].text)))

      else:
        # part 2
        for i in range(0, len(ctx.seeds), 2):
          self.seeds.append(d5p2_portion.make_interval(int(ctx.seeds[i].text), int(ctx.seeds[i + 1].text)))
    return self.visitChildren(ctx)

  def visitMap(self, ctx: day05Parser.MapContext):
    self.visitChildren(ctx)
    return {
      'destination': int(ctx.destination.text),
      'source': d5p2_portion.make_interval(int(ctx.source.text), int(ctx.length.text)),
      'shift': int(ctx.destination.text) - int(ctx.source.text),
    }

  def visitMaps(self, ctx: day05Parser.MapsContext):
    entries = [self.visitMap(entry) for entry in ctx.entries]
    self.maps[self.map2ind[ctx.source.text]] = entries
    return self.visitChildren(ctx)

  def search_ranges(self, a) -> int:
    active_interval = a
    for map_no in range(self.maxmaps):

      for entry in self.maps[map_no]:
        active_interval = d5p2_portion.intersect_and_transform(active_interval, entry['source'], entry['shift'])
        if active_interval.empty:
          return -1
      print(f'Map {map_no}, {self.ind2map[map_no + 1]}: {active_interval}')

    min_el = active_interval.lower

    print(f'Final answer: {a} went to {min_el}')

    return min_el

  def visitStart(self, ctx: day05Parser.StartContext):
    self.visitChildren(ctx)
    for rng in self.seeds:
      soln = self.search_ranges(rng)
      if self.answer is None or self.answer > soln:
        self.answer = soln

    return self.answer
