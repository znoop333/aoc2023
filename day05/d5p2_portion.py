import portion as P
import unittest


class IntInterval(P.AbstractDiscreteInterval):
  _step = 1


# https://pypi.org/project/portion/
D = P.create_api(IntInterval)


def make_interval(lb, size_):
  return D.closed(lb, lb + size_)


def make_single(val):
  return D.singleton(val)


def shift_interval(interval, offset):
  return interval.replace(lower=lambda x: x + offset, upper=lambda x: x + offset)


def intersect_and_transform(input_interval, domain, offset):
  intersection = input_interval & domain
  return shift_interval(intersection, offset) | (input_interval - domain), not intersection.empty


def try_portion():
  aa = make_interval(79, 14)
  s2s = make_interval(50, 48)

  soils, matched = intersect_and_transform(aa, s2s, 52 - 50)
  1


class TestCalculations(unittest.TestCase):

  def test_79(self):
    n = make_single(79)
    m1 = make_interval(50, 48)
    n = intersect_and_transform(n, m1, 52 - 50)
    self.assertEqual(n.lower, 81, 'Seed number 79 corresponds to soil number 81.')

  def test_14(self):
    input_stream = FileStream('test_input.txt', 'utf-8')
    # input_stream = FileStream('input.txt', encoding='utf-8')

    lexer = day05Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = day05Parser(stream)
    tree = parser.start()
    if parser.getNumberOfSyntaxErrors() > 0:
      print("syntax errors")
    else:
      vinterp = VisitorInterp()
      vinterp.visit(tree)

    active_interval = make_single(14)
    expected_vals = [14, 53, 49, 42, 42, 43, 43]
    for map_no in range(vinterp.maxmaps):
      for entry in vinterp.maps[map_no]:
        active_interval, matched = intersect_and_transform(active_interval, entry['source'], entry['shift'])
        if matched:
          break
        if active_interval.empty:
          return -1
      print(f'Map {map_no}, {vinterp.ind2map[map_no + 1]}: {active_interval}')

      self.assertEqual(active_interval.lower, expected_vals[map_no],
                       'Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43')


if __name__ == '__main__':
  from antlr4 import *
  from gen.day05Lexer import day05Lexer
  from gen.day05Parser import day05Parser
  from VisitorInterp import VisitorInterp

  unittest.main()
  try_portion()
