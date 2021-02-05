from NeuralNet import NeuralNet
from NNData import NNData
# from SnakeTest import Snake
from Frogger import Frogger
import copy as copy
import numpy as np
import math
import pickle
from os import path

class Population(object):
    def __init__(self, num_inputs, num_outputs, pop_size, data):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.pop_size = pop_size
        self.data = data
        self.reference = NeuralNet(num_inputs, num_outputs, data)
        self.reference.reset_neural_net()
        master_parent = self.get_master_parent(num_inputs, num_outputs, data)
        self.networks = [master_parent]
        for i in range(pop_size):
            net = copy.deepcopy(self.reference)
            net.randomize()
            net.mutate()
            self.networks.append(net)
        self.species = self.assign_pop_to_species(self.networks, [])


    def get_master_parent(self, num_inputs, num_outputs, data):
        if path.exists("neural_net.txt"):
            old_net = pickle.load(open("neural_net.txt", "rb"))
            old_net.master_reset_innov()
            return old_net
        net = NeuralNet(num_inputs, num_outputs, data)
        net.reset_neural_net()
        return net
        
        
    def sum_fitness(self, s):
        sum = 0
        for net in s:
            sum += net.fitness
        return sum

    def avg_fitness(self, s):
        return self.sum_fitness(s) / len(s)


    def find_best_member(self, s):
        best_fitness = s[0].fitness
        best_member = s[0]
        for net in s:
            if net.fitness > best_fitness:
                best_member = net
                best_fitness = net.fitness
        return best_member



    def choose_parent(self, s):
        threshold = np.random.random() * self.sum_fitness(s)
        sum = 0
        for net in s:
            sum += net.fitness
            if sum >= threshold:
                return net
        return s[len(s)-1]



    def assign_pop_to_species(self, pop, species):
        for net in pop:
            species_found = False
            for s in species:
                if not species_found:
                    if(len(s) > 0):
                        rep = s[np.random.randint(0, len(s))]
                        diff = self.calc_difference(net, rep)
                        if(diff < self.data.diff_threshold):
                            s.append(net)
                            species_found = True
                            break
                else:
                    break
            if not species_found:
                species.append([net])
        return species


    def determine_connection(self, p1, p2, innov):
        c1 = p1.find_connection_innov(innov)
        c2 = p2.find_connection_innov(innov)
        if c1 is None:
            return [c2, p2]
        if c2 is None:
            return [c1, p1]
        if not c1.enabled and c2.enabled:
            return [c1, p1]
        if not c2.enabled and c1.enabled:
            return [c2, p2]
        seed = np.random.random()
        if seed < 0.5:
            return [c1, p1]
        return [c2, p2]



    def crossover(self, p1, p2):
        child = copy.deepcopy(self.reference)
        child.copy_bias(p1)
        for i in range(self.data.get_innov() - 1):
            res = self.determine_connection(p1, p2, i+1)
            child.handle_new_connection(res[0], res[1])
        if self.data.debug:
            child.validate_connections()
        return child

    
    
    def top_pop(self, num):
        order = []
        nums = []
        for k in range(len(self.networks)):
            n = self.networks[k]
            nums.append(n.fitness)
        for i in range(num):
            max_index = nums.index(max(nums))
            nums[max_index] = -100000
            order.append(copy.deepcopy(self.networks[max_index]))
        return order
    
    
    def order_species(self, avg_fit):
        order = []
        nums = []
        for k in range(len(self.species)):
            s = self.species[k]
            nums.append((self.avg_fitness(s) * len(s) / avg_fit))
        for i in range(len(nums)):
            max_index = nums.index(max(nums))
            nums[max_index] = -100000
            order.append(copy.deepcopy(self.species[max_index]))
        return order
    
    
    def prepare_next_gen(self, num_parents):
        avg_fit = self.avg_fitness(self.networks)
        new_pop = self.top_pop(num_parents)
        num_left = self.pop_size - num_parents
        species_list = self.order_species(avg_fit)
        counter = 0
        for s in species_list:
            if num_left > 0:
                counter+=1
                num_offspring = max(math.ceil(self.avg_fitness(s) * len(s) / avg_fit), 1)
                num_left -= (num_offspring)
                if num_left < 0:
                    num_offspring += num_left
                new_members = []
                for i in range(num_offspring):
                    print("Creating member " + str(len(new_pop) + i + 1) + "/" + str(self.pop_size) + "\t", end='\r')
                    parent1 = self.choose_parent(s)
                    parent2 = self.choose_parent(s)
                    res = self.crossover(parent1, parent2)
                    res.mutate()
                    new_members.append(copy.deepcopy(res))
                if len(new_members) > 0:
                    new_pop.extend(new_members)
            else:
                break
        print("\n - Top " + str(counter) + " species survived\n", end='\n')
        self.networks = new_pop
        self.species = self.assign_pop_to_species(self.networks, [])



    def simulate_generations(self, num_generations, static_start, print_best):
        for i in range(num_generations):
            frogger = Frogger()
            sum = 0
            scores = []
            frogs = []
            best_score = -100
            best_net = []
            for net in self.networks:
                frog = Frogger.Frog(350,750,50,net, frogger.game_data)
                frogs.append(frog)
            frogger.begin_game(frogs, static_start)
            for j in range(len(frogs)):
                self.networks[j].fitness = frogs[j].score
                if frogs[j].score > best_score:
                    best_score = frogs[j].score
                    best_net = self.networks[j]
            for k in range(0):
                max_value = max(scores)
                max_index = scores.index(max_value)
                scores[max_index] = -1000000000
            avg_score = self.avg_fitness(self.networks)
            if print_best:
                best_net.show_net()
            print("-----------------------------------\t\t\t\t\t\t\n       Generation " + str(i+1) + " results\n-----------------------------------\n", end='\n')
            print("Highest Score: " + str(best_score) + "\nAverage score: " + str(avg_score) + "\nNum species: " + str(len(self.species)) + "\nInnovs tried: " + str(self.data.get_innov()) + "\n")
            pickle.dump(best_net, open("neural_net.txt", "wb"))
            if i != num_generations-1:
                self.prepare_next_gen(math.floor(self.pop_size/10))
                print("\nStarting Generation " + str(i+2) + ": Species = " + str(len(self.species)) + ", Innovs = " + str(self.data.get_innov()), end='\r')
        print("Finished simulation!")
    


    def print_pop(self):
        print("Each child in the population: \n")
        for net in self.networks:
            net.show_net()
        print("\nAll species (" + str(len(self.species)) + "):\n")
        for i in range(len(self.species)):
            s = self.species[i]
            print("Species " + str(i+1) + "\n\n")
            for n in s:
                n.show_net()
    


    def calc_difference(self, net1, net2):
        tot_diff = 0
        weight_diff = 0
        num_matches = 0
        innov_dict = {}
        for c1 in net1.connection_list:
            innov_dict[c1.innov] = c1.weight
        for c2 in net2.connection_list:
            if c2.innov in innov_dict:
                con1= net1.find_connection_innov(c2.innov)
                if con1.enabled and c2.enabled:
                    num_matches += 1
                    weight_diff += np.abs(con1.weight - c2.weight)
        tot_diff += (self.data.weight_scale * weight_diff / max(1, num_matches), 100) [num_matches == 0]
        num_connections = net1.num_active_connections() + net2.num_active_connections()
        tot_diff += self.data.struct_scale * (num_connections - 2 * num_matches) / num_connections
        return tot_diff



