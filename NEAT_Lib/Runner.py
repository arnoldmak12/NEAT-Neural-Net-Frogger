import numpy as np
from NeuralNet import NeuralNet
from Population import Population
from NNData import NNData
from Frogger import Frogger




print("\n\n===================================")
print("\tWelcome to Frog.io!")
print("===================================\n")

print("-----------------------------------\n       Simulation Parameters\n-----------------------------------\n")

pop_size = input(" - How many frogs would you like in each generation? (Recommended: 200-400) ")
static_start = input(" - Do you want the cars to start in the same position each generation? (Y/N) ")
is_static = static_start == "Y" or static_start == "y"
num_generations = input(" - How many generations would you like to simulate? (Recommended: 30-50) ")
print_best = input(" - Do you want to print the best network after each generation? (Y/N) ")
is_print = print_best == "Y" or print_best == "y"

print("\n\n-----------------------------------\n        General Information\n-----------------------------------\n")

print("\t- A neural network is saved and updated for you automatically after each generation.\n\t- If you've run this simulation before, it'll be included in the starting population.")
input("\nPress [Enter] when you are ready to begin the simulation")

print("\n\n-----------------------------------\n         Simulation Start\n-----------------------------------\n")

print("Preparing the starting population. This will only take a moment...")

data = NNData()
pop = Population(13, 5, int(pop_size), data)

print("Starting population complete!")

print("\n\n===================================\n    Simulating " + num_generations + " generation(s)\n===================================\n\n")

pop.simulate_generations(int(num_generations), is_static, is_print)

print("\n-----------------------------------\n          Continuing play\n-----------------------------------\n")

response = input("\n\nWould you like to play continuous frogger games with the best frog? (Y/N) ")
if response == "Y" or response == "y":
    while True:
        frogger = Frogger()
        frog = Frogger.Frog(350,750,50, pop.get_master_parent(13, 5, data), frogger.game_data)
        frogger.begin_game([frog], is_static)


