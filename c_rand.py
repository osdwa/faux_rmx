"""
Documentation (kinda)
You must create instance of CRandom before using it.

= set_seed(seed) - sets seed

= roll() - basically randd()

= rand(roll?)
If roll=True (default), does what roll() does
If roll=False, returns current seed without rerolling

= rand_int(size, roll?) - random int in [0, size] range;
size - the right bound
roll (default=True) - should it be rerolled first?

= rand_float(roll?) - random float in [0, 1] range;
roll (default=True) - should it be rerolled first?

= rand_bool(chance, roll?) - random bool with X chance to be True
chance - float, in 0-1 range
roll (default=True) - should it be rerolled first?
"""


class CRandom:
    UINT_LIMIT = 2 ** 32
    M0 = 0x007fffff
    M1 = 0x00800000
    def __init__(self):
        self.ran = 0

    def set_seed(self, seed: int):
        self.ran = seed % self.UINT_LIMIT

    def roll(self):
        self.ran = (self.ran * 0x0BB38435) % self.UINT_LIMIT
        self.ran = (self.ran + 0x3619636B) % self.UINT_LIMIT
        return self.ran

    def rand(self, roll=True):
        if roll:
            return self.roll()
        else:
            return self.ran

    def rand_int(self, size: int, roll=True):
        n = self.rand(roll)
        return  int(((n & self.M0) - (8388)) / (self.M1 / size))

    def rand_float(self, roll=True):
        n = self.rand(roll)
        return (n & self.M0) / self.M0

    def rand_bool(self, chance: float, roll=True):
        return self.rand_float(roll) < chance


def test():
    cr = CRandom()

    maxx = -1
    minn = 2

    for _ in range(10_000_000):
        r = cr.rand_float()
        maxx = max(r, maxx)
        minn = min(r, minn)

    print(maxx, minn)


if __name__ == "__main__":
    test()
