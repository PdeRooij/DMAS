from directions import Directions

__author__ = 'tom, stef, pieter'


class Transition:


    def __init__(self, driver):
        self.driver = driver
        self.location = [0,0]
        self.start = [0,0]
        self.end = [0,0]
        