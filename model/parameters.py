__author__ = 'tom, stef, pieter'

# A container of set variables for a simulation.
# It is implemented as a dictionary, where a specific parameter name is the key.


class Parameters():
    # Creates a new set of parameters with standard values.
    def __init__(self):
        print("Init Parameters...")
        self.param = {'n_drivers': 2,
                      'grid_size': [3, 3],
                      'max_cycles': 10
                      }

    # Returns setting of specified parameter
    def get(self, param):
        return self.param[param]

    # Set a parameter to a certain value
    # NOTE ought only to happen BEFORE starting a simulation,
    # value has to be verified BEFORE passing onto this method.
    def set(self, param, value):
        self.param[param] = value

    # Override standard print to list all parameters
    def __str__(self):
        print('%%%%%%%%%%%%%%%%%%%%%%\nParameters\n%%%%%%%%%%%%%%%%%%%%%%')
        print('parameter\tvalue')
        for key, value in self.param.iteritems():
            print("{}\t{}".format(key, value))