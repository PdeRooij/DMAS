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
        try:
            idx = int(item)
        except ValueError:
            # Cannot make an int, assume input was a string
            print 'Implement inputting string to Directions!!'

        return self.directions[idx]

    # A neat print of the directions and their respective number
    def __str__(self):
        string = 'Wind directions and corresponding numbers:\n'
        for idx, direction in enumerate(self.directions):
            string += direction + '\t' + idx + '\n'
        return string