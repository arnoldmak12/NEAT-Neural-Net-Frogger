import numpy as np

class Node(object):
    def __init__(self, id, type):
        self.id = id
        self.connections = []
        self.bias = (np.random.randn(), 0) [type == "Input"] # input nodes has no bias
        self.type = type
        self.value = 0

    def __str__(self):
        res = "ID: " + str(self.id) + ", Bias: " + str(self.bias) + ", Type: " + self.type + ", Value: " + str(self.value) + "\n"
        if(len(self.connections) == 0):
            res += "No connections\n"
        for c in self.connections:
            res += "Connected to: " + str(c.output_id) + (" (Disabled)", " (Enabled)") [c.enabled] + " with weight: " + str(c.weight) + ", Innov: " + str(c.innov) + "\n"
        return res


