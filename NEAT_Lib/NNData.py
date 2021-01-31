class NNData(object):
    def __init__(self):
        self.struct_scale = 1
        self.weight_scale = 2
        self.diff_threshold = 1.5
        global next_innov
        next_innov = 1

    def increment_innov(self):
        global next_innov
        next_innov += 1

    def get_innov(self):
        global next_innov
        return next_innov


