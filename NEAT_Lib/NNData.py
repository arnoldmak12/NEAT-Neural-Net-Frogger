class NNData(object):
    def __init__(self):
        self.struct_scale = 3
        self.weight_scale = 1.25
        self.diff_threshold = 2
        self.debug = False
        global next_innov
        global master_connection_list
        next_innov = 1
        master_connection_list = []

    def increment_innov(self):
        global next_innov
        next_innov += 1

    def get_innov(self):
        global next_innov
        return next_innov

    def set_innov(self, new_innov):
        global next_innov
        next_innov = new_innov

    def add_master_connection(self, c):
        global master_connection_list
        for con in master_connection_list:
            if c.input_id == con.input_id and c.output_id == con.output_id:
                return
        master_connection_list.append(c)
        self.increment_innov()

    def print_master_connections(self):
        global master_connection_list
        for c in master_connection_list:
            print(str(c))

    def get_existing_connection(self, input, output):
        global master_connection_list
        for con in master_connection_list:
            if con.input_id == input and con.output_id == output:
                return con
        return


