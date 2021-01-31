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

    #runs sigmoid on a layer of nodes. Used on output layer
    def sigmoid_layer(self, nodes):
        for i in range(len(nodes)):
            nodes[i] = self.sigmoid(nodes[i])
        return nodes

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
                c = Connection(n.id, self.next_id, self.data.get_innov())
                self.connection_list.append(c)
                n.connections.append(c)
                self.add_and_sort_nodes(n.id, new_node.id)
                self.data.increment_innov()
            self.next_id += 1
        return self.node_list

    def add_and_sort_nodes(self, input_node, output_node):
        if input_node in self.node_order and output_node in self.node_order:
            if self.node_order.index(input_node) > self.node_order.index(output_node):
                self.node_order.remove(input_node)
                self.node_order.insert(self.node_order.index(output_node), input_node)
        elif input_node in self.node_order:
            self.node_order.append(output_node)
        elif output_node in self.node_order:
            self.node_order.insert(self.node_order.index(output_node), input_node)
        else:
            self.node_order.append(input_node)
            self.node_order.append(output_node)
    
    #takes input info and propogates forward through the nn.
    def forward_prop(self, inputs):
        self.init_inputs(inputs)
        for i in range(len(self.node_order)):
            node = self.find_node(self.node_order[i])
            if not node.type == "Input":
                node.value = self.sigmoid(node.value)
            for c in node.connections:
                if c.enabled:
                    output = self.find_node(c.output_id)
                    output.value += node.value * c.weight + output.bias
        return self.get_output_nodes()

    
    def randomize_all_bias(self):
        for n in self.node_list:
            n.bias = (np.random.randn(), 0) [n.type == "Input"]
    
    
    def mutate(self):
        if np.random.random() < 0.9:
            self.mutate_weights()
        if np.random.random() < 0.06:
            self.add_connection()
        if np.random.random() < 0.015:
            self.add_node()


    def mutate_weights(self):
        for c in self.connection_list:
            seed = np.random.random()
            if seed < 0.1:
                c.weight = np.random.randn()
            elif seed < 0.5:
                c.weight += 2*np.random.random() - 1
        #print("Mutating Weights!")



    def connection_exists(self, n1, n2):
        for c in self.connection_list:
            if c.input_id == n1.id or c.input_id == n2.id:
                if c.output_id == n1.id or c.output_id == n2.id:
                    return True
        return False


    def connection_valid(self, n1, n2):
        if self.connection_exists(n1, n2):
            return False
        if n1.type == "Input":
            if n2.type == "Hidden" or n2.type == "Output":
                return True
        elif n1.type == "Hidden":
            if n2.type == "Hidden" or n2.type == "Output":
                return True
        elif n1.type == "Output":
            if n2.type == "Hidden" or n2.type == "Input":
                return True
        return False



    def append_connection(self, n1, n2):
        index1 = self.node_order.index(n1.id)
        index2 = self.node_order.index(n2.id)
        if index1 < index2:
            self.connection_list.append(Connection(n1.id, n2.id, self.data.get_innov()))
        else:
            self.connection_list.append(Connection(n2.id, n1.id, self.data.get_innov()))
        self.data.increment_innov()
    
    
    def add_connection(self):
        #print("Mutating Connections!")
        n_list1 = copy.deepcopy(self.node_list)
        n_list2 = copy.deepcopy(self.node_list)
        shuffle(n_list1)
        shuffle(n_list2)
        for n1 in n_list1:
            for n2 in n_list2:
                if self.connection_valid(n1, n2):
                    self.append_connection(n1, n2)
                    return
        return



    def add_node(self):
        #print("Mutating Nodes!")
        con = self.connection_list[np.random.randint(0, len(self.connection_list))]
        input_n = self.find_node(con.input_id)
        output_n = self.find_node(con.output_id)
        con.enabled = False
        new_node = Node(self.next_id, "Hidden")
        self.node_list.append(new_node)
        self.next_id += 1

        c1 = Connection(con.input_id, new_node.id, self.data.get_innov())
        c1.weight = con.weight
        self.connection_list.append(c1)
        input_n.connections.append(c1)
        self.add_and_sort_nodes(input_n.id, new_node.id)
        self.data.increment_innov()

        c2 = Connection(new_node.id, con.output_id, self.data.get_innov())
        c2.weight = con.weight
        self.connection_list.append(c2)
        new_node.connections.append(c2)
        self.add_and_sort_nodes(new_node.id, output_n.id)
        self.data.increment_innov()



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
    
    
    def handle_new_connection(self, c):
        if c is None:
            return
        existing_c = self.search_connections(c.input_id, c.output_id)
        if existing_c is None:
            new_node_input = self.find_node(c.input_id)
            new_node_output = self.find_node(c.output_id)
            if new_node_input is None:
                new_node_input = Node(c.input_id, "Hidden")
                self.node_list.append(new_node_input)
                self.next_id = (self.next_id, new_node_input.id + 1) [new_node_input.id+1 > self.next_id]
            if new_node_output is None:
                new_node_output = Node(c.output_id, "Hidden")
                self.node_list.append(new_node_output)
                self.next_id = (self.next_id, new_node_output.id + 1) [new_node_output.id+1 > self.next_id]
            new_c = Connection(new_node_input.id, new_node_output.id, c.innov)
            new_c.enabled = c.enabled
            self.connection_list.append(new_c)
            new_node_input.connections.append(new_c)
            self.add_and_sort_nodes(new_node_input.id, new_node_output.id)
        else:
            existing_c.enabled = c.enabled

    
    
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

    #adjusts weights by a fraction of the desired change
    def adjust_weights(self, change, layer, training_rate):
        for i in range(len(self.neural_net[layer])):
            for k in range(len(change)):
                sign = (-1,1) [self.nodes[layer][i]>0]
                self.neural_net[layer][i][k] = self.neural_net[layer][i][k] + change[k]*training_rate*sign
    

    def show_net(self):
        for n in self.node_list:
            print(str(n))
        print("\n")


    #calculates cost of each output node based on the expected outcome
    def calculate_costs(self, outputs, expected_outputs):
        costs = []
        for i in range(len(outputs)):
            costs.append(expected_outputs[i] - outputs[i])
        return costs


