import numpy as np

class Connection(object):
    def __init__(self, input, output, innov):
        self.input_id = input
        self.output_id = output
        self.weight = np.random.randn()
        self.enabled = True
        self.innov = innov

    def __str__(self):
        return "Input: "+ str(self.input_id) + ", Output: " + str(self.output_id) + ", Weight: " + str(self.weight) + ", Enabled: " + str(self.enabled) + ", Innov: " + str(self.innov)


