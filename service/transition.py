__author__ = 'tom, stef, pieter'

'''
A transition object simply holds necessary information about a driver moving somewhere else.
Transition indicates whether the transition is within or between crossings,
driver is the agent involved, start and end are either grid locations or directions based on type.
'''


class Transition:

    def __init__(self, driver, start, end, transition='move'):
        self.type = transition
        self.driver = driver
        self.start = start
        self.end = end
