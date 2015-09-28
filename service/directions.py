__author__ = 'tom, stef, pieter'

"""
A dead simple enumeration of the four wind directions.
It utilizes basic functions for added convenience.
"""


# Wind directions ported to a class for convenience
class Directions:
    # Make the enumeration happen!
    def __init__(self):
        self.directions = ['North', 'East', 'South', 'West']

    # The indices 0 through 3 now correspond to a wind direction and vice versa
    def __getitem__(self, item):
        # Resolve class of item
        if isinstance(item, str):
            # Input was a string, return index of that element
            return self.directions.index(item)
        elif isinstance(item, int):
            # Int - get element at that index
            return self.directions[item]
        elif isinstance(item, slice):
            # Slice - get elements according to start, stop, and step
            return [self.directions[i] for i in xrange(*item.indices(len(self.directions)))]
        else:
            # Unhandled class, raise error
            raise TypeError("Invalid argument type.\n"
                            "Expected str, int or slice, got", item, 'instead.')

    # Length is the length of the directions list (4)
    def __len__(self):
        return len(self.directions)

    # A neat print of the directions and their respective number
    def __str__(self):
        string = 'Wind directions and corresponding numbers:\n'
        for idx, direction in enumerate(self.directions):
            string += direction + '\t' + str(idx) + '\n'
        return string
