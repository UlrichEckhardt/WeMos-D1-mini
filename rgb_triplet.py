# -*- coding: utf-8 -*-
import collections

class rgb(collections.namedtuple('rgb', ['r', 'g', 'b'])):
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

