# -*- coding: utf-8 -*-
import collections
import random
card=collections.namedtuple('card',('rank','suit'))


class FrenchDuck(object):
    rank=[i for i in range(2,11)]+list('JQKA')
    suit=['black_heart','red_heart','meihua','fangkuai']

    def __init__(self):
        self._cards=[card(i,j) for i in self.rank for j in self.suit]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __enter__(self):
        return random.choice(self._cards)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return random.choice(self._cards)


card1=FrenchDuck()
print card1[23]
