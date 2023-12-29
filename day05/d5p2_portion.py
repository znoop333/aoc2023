import portion as P


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
  return shift_interval(intersection, offset) | (input_interval - domain)


def try_portion():
  aa = make_interval(79, 14)
  s2s = make_interval(50, 48)

  soils = intersect_and_transform(aa, s2s, 52 - 50)
  1


if __name__ == '__main__':
  try_portion()
