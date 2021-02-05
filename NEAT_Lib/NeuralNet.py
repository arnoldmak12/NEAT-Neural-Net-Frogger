import numpy as np
from Node import Node
from Connection import Connection
from NNData import NNData
import copy as copy
from random import shuffle

class NeuralNet():
    def __init__(self, num_inputs, num_outputs, data):
        self.node_list = []
        self.connection_list = []
        self.input_size = num_inputs
        self.output_size = num_outputs
        self.node_order = []
        self.data = data
        self.next_id = 1
        self.fitness = 0

    #will return value between 0 and 1.
    def sigmoid(self, x):
        #boundary check to get rid of potential overflow. Little effect on training
        if x > 100:
            return .99999
        elif x < -100:
            return 0.00001
        return 1/(1 + np.exp(-x))


    #generates a randomized neural network according to the dimensions upon creation
    def reset_neural_net(self):
        input_list = []
        for i in range(self.input_size):
            n = Node(self.next_id, "Input")
            input_list.append(n)
            self.node_list.append(n)
            self.next_id += 1
        for k in range(self.output_size):
            new_node = Node(self.next_id, "Output")
            self.node_list.append(new_node)
            for n in input_list:
                c = Connection(n.id, self.next_id, self.determine_innov(n.id, self.next_id))
                self.connection_list.append(c)
                n.connections.append(c)
                self.data.add_master_connection(c)
                self.add_and_sort_nodes(n.id, new_node.id)
                #self.validate_connections()
            self.next_id += 1
        return self.node_list

    
    def master_reset_innov(self):
        for c in self.connection_list:
            c.innov = self.determine_innov(c.input_id, c.output_id)
            self.data.add_master_connection(c)
    
    
    def get_placement_index(self, start, stop, step):
        for i in range(start, stop, step):
            if step == -1:
                if self.find_node(self.node_order[i]).type != "Output":
                    return i+1
            else:
                if self.find_node(self.node_order[i]).type != "Input":
                    return i
        return len(self.node_order)
    
    #adds and sorts nodes to maintain proper node order
    def add_and_sort_nodes(self, input_node, output_node):
        if input_node in self.node_order and output_node in self.node_order:
            if self.node_order.index(input_node) > self.node_order.index(output_node):
                self.node_order.remove(input_node)
                self.node_order.insert(self.node_order.index(output_node), input_node)
        elif input_node in self.node_order:
            self.node_order.insert(self.get_placement_index(self.node_order.index(input_node)+1, len(self.node_order), 1), output_node)
        elif output_node in self.node_order:
            self.node_order.insert(self.get_placement_index(self.node_order.index(output_node)-1, 0, -1), input_node)
        else:
            self.node_order.append(input_node)
            self.node_order.append(output_node)
    
    #takes input info and propogates forward through the nn.
    def forward_prop(self, inputs):
        self.init_inputs(inputs)
        for i in range(len(self.node_order)):
            node = self.find_node(self.node_order[i])
            node.value += node.bias
            if node.type != "Input":
                node.value = self.sigmoid(node.value)
            if self.data.debug and node.value > 1:
                self.show_net()
                print(str(node))
                raise Exception("Illegal value error: Node has value > 1")
            for c in node.connections:
                if c.enabled:
                    output = self.find_node(c.output_id)
                    if self.data.debug and self.node_order.index(node.id) > self.node_order.index(output.id):
                        self.show_net()
                        print(self.node_order)
                        raise Exception("Illegal node order error: Input order comes after output order.")
                    output.value += node.value * c.weight
        return self.get_output_nodes()

    # randomizes all bias values
    def randomize_all_bias(self):
        for n in self.node_list:
            n.bias = (np.random.randn(), 0) [n.type == "Input"]
    
    # mutates the neural net
    def mutate(self):
        if np.random.random() < 0.9:
            self.mutate_weights()
        if np.random.random() < 0.03:
            self.add_connection()
        if np.random.random() < 0.01:
            self.add_node()
        return


    def num_active_connections(self):
        sum = 0
        for c in self.connection_list:
            if c.enabled:
                sum += 1
        return sum
    
    
    def mutate_weights(self):
        for n in self.node_list:
            if n.type != "Input":
                seed = np.random.random()
                if seed < 0.1:
                    n.bias = np.random.randn()
                elif seed < 0.5:
                    n.bias += 2*np.random.random() - 1
        for c in self.connection_list:
            seed = np.random.random()
            if seed < 0.1:
                c.weight = np.random.randn()
            elif seed < 0.5:
                c.weight += 2*np.random.random() - 1
        return



    def connection_exists(self, n1, n2):
        for c in self.connection_list:
            if c.input_id == n1.id and c.output_id == n2.id:
                    return True
        return False


    def connection_valid(self, n1, n2):
        if n1 is None or n2 is None:
            return True
        if n1.id == n2.id:
            return False
        if self.connection_exists(n1, n2):
            return False
        if self.connection_exists(n2, n1):
            return False
        if self.node_order.index(n1.id) > self.node_order.index(n2.id):
            return False
        if n1.type == "Input":
            if n2.type == "Hidden" or n2.type == "Output":
                return True
        elif n1.type == "Hidden":
            if n2.type == "Hidden" or n2.type == "Output":
                return True
        return False

    
    
    def validate_connections(self):
        sum1 = len(self.connection_list)
        sum2 = 0
        for n in self.node_list:
            sum2 += len(n.connections)
            if n.type == "Output" and len(n.connections) != 0:
                self.show_net()
                raise Exception("Invalid node error: Ouput node has " + str(len(n.connections)) + " connections, when it should have 0.")
            if n.type == "Hidden" and len(n.connections) == 0:
                self.show_net()
                self.data.print_master_connections()
                raise Exception("Invalid node error: Hidden node cannot have 0 connections.")
        if sum1 != sum2:
            print("\n\n--------------------------------Network Connection List-----------------------------\n\n")
            self.show_connection_list()
            print("\n\n--------------------------------Network Node Connections-----------------------------\n\n")
            self.show_net()
            raise Exception("Unsynced network error: There are " + str(sum1) + " connections in the network list, but " + str(sum2) + " connections in the node lists\n")
        for c in self.connection_list:
            if c.innov >= self.data.get_innov():
                print(str(c) + "\n")
                self.data.print_master_connections()
                raise Exception("Invalid connection error: Connection not in master connection list")
            if self.find_node(c.input_id).type == "Output":
                print("\n\n--------------------------------Network Connection List-----------------------------\n\n")
                self.show_connection_list()
                print("\n\n--------------------------------Network Node Connections-----------------------------\n\n")
                self.show_net()
                raise Exception("Invalid connection error: Input was of type: Output")


    def append_connection(self, n1, n2):
        index1 = self.node_order.index(n1.id)
        index2 = self.node_order.index(n2.id)
        if index1 < index2:
            c = Connection(n1.id, n2.id, self.determine_innov(n1.id, n2.id))
            self.connection_list.append(c)
            n1.connections.append(c)
            self.data.add_master_connection(c)
            self.add_and_sort_nodes(n1.id, n2.id)
        else:
            c = Connection(n2.id, n1.id, self.determine_innov(n2.id, n1.id))
            self.connection_list.append(c)
            n2.connections.append(c)
            self.data.add_master_connection(c)
            self.add_and_sort_nodes(n2.id, n1.id)
        if self.data.debug:
            self.validate_connections()
    
    def copy_bias(self, parent):
        for n in self.node_list:
            pn = parent.find_node(n.id)
            if not pn is None:
                n.bias = pn.bias



    def add_connection(self):
        n_list1 = copy.deepcopy(self.node_list)
        n_list2 = copy.deepcopy(self.node_list)
        shuffle(n_list1)
        shuffle(n_list2)
        for n1 in n_list1:
            for n2 in n_list2:
                if self.connection_valid(n1, n2):
                    real_n1 = self.find_node(n1.id)
                    real_n2 = self.find_node(n2.id)
                    self.append_connection(real_n1, real_n2)
                    return
        return



    def add_node(self):
        con = self.connection_list[np.random.randint(0, len(self.connection_list))]
        input_n = self.find_node(con.input_id)
        output_n = self.find_node(con.output_id)
        con.enabled = False
        new_node = Node(self.next_id, "Hidden")
        self.node_list.append(new_node)
        self.next_id += 1

        c1 = Connection(con.input_id, new_node.id, self.determine_innov(con.input_id, new_node.id))
        self.connection_list.append(c1)
        input_n.connections.append(c1)
        self.data.add_master_connection(c1)
        self.add_and_sort_nodes(input_n.id, new_node.id)

        c2 = Connection(new_node.id, con.output_id, self.determine_innov(new_node.id, con.output_id))
        self.connection_list.append(c2)
        new_node.connections.append(c2)
        self.data.add_master_connection(c2)
        self.add_and_sort_nodes(new_node.id, output_n.id)
        if self.data.debug:
            self.validate_connections()



    # completely randomize weights of network
    def randomize(self):
        for c in self.connection_list:
            c.weight = np.random.randn()
        for n in self.node_list:
            n.bias = (np.random.randn(), 0) [n.type == "Input"]
    
    def get_output_nodes(self):
        nodes = []
        for n in self.node_list:
            if n.type == "Output":
                nodes.append(n.value)
        return nodes
    
    
    def search_connections(self, input, output):
        for c in self.connection_list:
            if c.input_id == input and c.output_id == output:
                return c
        return
    
    
    def determine_innov(self, input, output):
        c = self.data.get_existing_connection(input, output)
        if c is None:
            innov = self.data.get_innov()
            return innov
        return c.innov

    
    def handle_new_connection(self, c, parent):
        if c is None:
            return
        existing_c = self.search_connections(c.input_id, c.output_id)
        input_bias = parent.find_node(c.input_id).bias
        output_bias = parent.find_node(c.output_id).bias
        if existing_c is None:
            new_node_input = self.find_node(c.input_id)
            new_node_output = self.find_node(c.output_id)
            if not self.connection_valid(new_node_input, new_node_output):
                return
            if new_node_input is None:
                new_node_input = Node(c.input_id, "Hidden")
                new_node_input.bias = input_bias
                self.node_list.append(new_node_input)
                self.next_id = (self.next_id, new_node_input.id + 1) [new_node_input.id+1 > self.next_id]
            if new_node_output is None:
                new_node_output = Node(c.output_id, "Hidden")
                new_node_output.bias = output_bias
                self.node_list.append(new_node_output)
                self.next_id = (self.next_id, new_node_output.id + 1) [new_node_output.id+1 > self.next_id]
            self.add_and_sort_nodes(new_node_input.id, new_node_output.id)
            new_c = Connection(new_node_input.id, new_node_output.id, c.innov)
            new_c.enabled = c.enabled
            new_c.weight = c.weight
            self.connection_list.append(new_c)
            new_node_input.connections.append(new_c)
        else:
            existing_c.enabled = c.enabled
            existing_c.weight = c.weight

    def show_connection_list(self):
        for c in self.connection_list:
            print(str(c))
    
    def find_connection_innov(self, innov):
        for c in self.connection_list:
            if c.innov == innov:
                return c
        return
    
    
    def find_node(self, id):
        for n in self.node_list:
            if n.id == id:
                return n
        return
    
    def init_inputs(self, inputs):
        for i in range(len(inputs)):
            self.node_list[i].value = inputs[i]
    
    #takes costs of each output node and propogates backward through the nn
    def backward_prop(self, output_costs, training_rate):
        change = output_costs
        old_change = []
        start = len(self.dimensions)-2
        for i in range(len(self.dimensions)-1):
            #since we calc the next change before adjusting the weights, we need to create a deep copy of the current change
            old_change = copy.deepcopy(change)
            change = np.matmul(change, np.transpose(self.neural_net[start-i]))
            self.adjust_weights(old_change, start-i, training_rate)
   

    def show_net(self):
        print("", end='\n')
        for n in self.node_list:
            print(str(n))
        print("\n")



