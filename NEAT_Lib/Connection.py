import numpy as np

class Connection(object):
    def __init__(self, input, output, innov):
        self.input_id = input
        self.output_id = output
        self.weight = np.random.randn()
        self.enabled = True
        self.innov = innov


