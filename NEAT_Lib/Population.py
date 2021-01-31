from NeuralNet import NeuralNet
from NNData import NNData
from SnakeTest import Snake
from Frogger import Frogger
import copy as copy
import numpy as np
import math

class Population(object):
    def __init__(self, num_inputs, num_outputs, pop_size, data):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.pop_size = pop_size
        self.data = data
        master_parent = NeuralNet(num_inputs, num_outputs, data)
        master_parent.reset_neural_net()
        self.reference = copy.deepcopy(master_parent)
        self.networks = [master_parent]
        for i in range(math.floor(pop_size)):
            net = copy.deepcopy(master_parent)
            net.randomize()
            net.mutate()
            self.networks.append(net)
        self.species = self.assign_pop_to_species(self.networks, [])


    def sum_fitness(self, s):
        sum = 0
        for net in s:
            sum += net.fitness
            if net.fitness < 0:
                print(sum)
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
                        if(self.calc_difference(net, rep) < self.data.diff_threshold):
                            s.append(net)
                            species_found = True
                            break
            if not species_found:
                species.append([net])
        return species


    def determine_connection(self, p1, p2, innov):
        c1 = p1.find_connection_innov(innov)
        c2 = p2.find_connection_innov(innov)
        if c1 is None:
            return c2
        if c2 is None:
            return c1
        if not c1.enabled and c2.enabled:
            return c1
        if not c2.enabled and c1.enabled:
            return c2
        seed = np.random.random()
        if seed < 0.5:
            return c1
        return c2



    def crossover(self, p1, p2):
        child = copy.deepcopy(self.reference)
        child.randomize_all_bias()
        for i in range(self.data.get_innov() - 1):
            pot_c = self.determine_connection(p1, p2, i+1)
            child.handle_new_connection(pot_c)
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
    
    
    def prepare_next_gen(self):
        avg_fit = self.avg_fitness(self.networks)
        new_pop = self.top_pop(50)
        num_left = self.pop_size - 50
        species_list = self.order_species(avg_fit)
        counter = 0
        for s in species_list:
            if num_left > 0:
                counter+=1
                num_offspring = max(math.ceil(self.avg_fitness(s) * len(s) / avg_fit), 1)
                num_left -= (num_offspring)
                if num_left < 0:
                    num_offspring += num_left
                    print("-----------------------------BREAK (" + str(counter) + ")------------------------------")
                new_members = []
                for i in range(num_offspring):
                    parent1 = self.choose_parent(s)
                    parent2 = self.choose_parent(s)
                    res = self.crossover(parent1, parent2)
                    res.mutate()
                    new_members.append(copy.deepcopy(res))
                if len(new_members) > 0:
                    new_pop.extend(new_members)
            else:
                self.networks = new_pop
                self.species = self.assign_pop_to_species(self.networks, [])
                return
        self.networks = new_pop
        self.species = self.assign_pop_to_species(self.networks, [])



    def simulate_generations(self, num_generations):
        print("\n\n------------------------------\nSimulating " + str(num_generations) + " generations!\n------------------------------\n\n")
        for i in range(num_generations):
            frogger = Frogger()
            sum = 0
            scores = []
            frogs = []
            best_score = -100
            best_net = []
            for net in self.networks:
                frog = Frogger.Frog(335,700,50,net, frogger.game_data)
                frogs.append(frog)
                #snake = Snake(False, net)
                #score = snake.new_game()
                #print(str(score) + "\n")
                #net.fitness = score
                #scores.append(score)
                #sum += score
                #if score > best_score:
                    #best_score = score
                    #best_net = net
                #frog = Frog(net)
                #score = frog.simulate_game()
                #scores.append(score)
                #sum += score
                #outputs = net.forward_prop([1,1])
                #net.fitness = outputs[0].value
            #print("\nBest performers:")
            frogger.begin_game(frogs)
            for j in range(len(frogs)):
                self.networks[j].fitness = frogs[j].score
                if frogs[j].score > best_score:
                    best_score = frogs[j].score
                    best_net = self.networks[j]
            for k in range(0):
                max_value = max(scores)
                max_index = scores.index(max_value)
                scores[max_index] = -1000000000
                #print(max_value)
            avg_score = self.avg_fitness(self.networks)
            best_net.show_net()
            print("\n\nGeneration " + str(i+1) + " results:\nHighest Score: " + str(best_score) + "\nAverage score: " + str(avg_score) + "\nNum species: " + str(len(self.species)) + "\nNum members: " + str(len(self.networks)))
            self.prepare_next_gen()
            print("Finished!")
            print("\n\nStarting Generation " + str(i+2) + ": Members = " + str(len(self.networks)) + ", Species = " + str(len(self.species)))

            #print("Avg score: " + str(sum/len(self.networks)))
        print("Done!")
    


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
        for c1 in net1.connection_list:
            for c2 in net2.connection_list:
                if c1.enabled and c2.enabled:
                    if c1.innov == c2.innov:
                        num_matches += 1
                        weight_diff += np.abs(c1.weight - c2.weight)
        tot_diff += (self.data.weight_scale * weight_diff / max(1, num_matches), 100) [num_matches == 0]
        num_connections = len(net1.connection_list) + len(net2.connection_list)
        tot_diff += self.data.struct_scale * (num_connections - 2 * num_matches) / num_connections
        return tot_diff



