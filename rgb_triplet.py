# -*- coding: utf-8 -*-
try:
    from collections import namedtuple
except ImportError:
    # micropython doesn't have collections but it does have a suitable ucollections
    from ucollections import namedtuple

class rgb(namedtuple('rgb', ['r', 'g', 'b'])):
    """RGB triplet
    
    Apart from the named elements, it supports a few operations you would
    expect to find in a vector room.

    """
    def __add__(self, other):
        """add two RGB triplets"""
        return rgb(self[0] + other[0],
                   self[1] + other[1],
                   self[2] + other[2])

    def __mul__(self, other):
        """multiply by a scalar"""
        return rgb(self[0] * other,
                   self[1] * other,
                   self[2] * other)

    def __rmul__(self, other):
        """multiply by a scalar"""
        return self * other

# unit vectors with the according color components
rgb.RED = rgb(1, 0, 0)
rgb.GREEN = rgb(0, 1, 0)
rgb.BLUE = rgb(0, 0, 1)

# white vector
rgb.WHITE = rgb.RED + rgb.GREEN + rgb.BLUE
