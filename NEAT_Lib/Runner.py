import numpy as np
from NeuralNet import NeuralNet
from Population import Population
from NNData import NNData

# This demo shows how to use the NeuralNet library
# In this example, we give the NN 2 random floats, and train it to determine which float is greater than the other.


# This is how we will generate data for the NN to train with. Format: [float1, float2, expected_output]
def generate_sample_data(size):
    data = np.random.randn(size,3)
    for i in range(size):
        data[i][2] = (1,0) [data[i][0] < data[i][1]]
    return data


pop = Population(5, 5, 500, NNData())

pop.simulate_generations(100)

# Next, you need to generate the starting NN. Storing the result is optional.



print("\nTraining in progress...\n")

# Here we specify some key parameters that affect how the NN trains.
num_batches = 1 # 5000
batch_size = 1 # 20
training_rate = 0.05

# This is optional, but gives us an idea of how accurate the NN is.
num_correct = 0
num_total = 0

# This is where we train the NN.
for i in range(num_batches):
    # First, we retrieve the data for a given batch.
    sample_data = generate_sample_data(batch_size)
    # Then we get a prediction for each data set in the batch.
    for k in range(batch_size):
        pass
        # To start, we pass the inputs to the NN and get the output nodes.
        #outputs = net.forward_prop([sample_data[k][0], sample_data[k][1]])
        # Next, we need to determine what the expected output should be based on the inputs.
        #expected_outputs = [sample_data[k][2]]
        # We compare the output nodes to the expected output nodes and determine the cost of each node.
        #costs = net.calculate_costs(outputs, expected_outputs)
        # Finally, we use the costs to adjust the weights of the NN.
        #net.backward_prop(costs, training_rate)
        # Here we can update the parameters that determine the NN's accuracy.
        #num_total = num_total+1
        #num_correct = (num_correct,num_correct+1) [np.abs(outputs[0]-expected_outputs[0]) < 0.5]
    #print(str(i+1) + "/" + str(num_batches) + " batches completed, Accuracy: " + str(round(num_correct/num_total*100, 3)) + "%\t", end='\r')

print("\n\n", end='\n')
#pop.simulate_generations(100)
print("Ending Neural Net:\n")
#pop.print_pop()
input("Finished")

# Now we can feed custom inputs to the NN and see how accurate it is. Note: inputs for NN should be scaled to be within [-5,5]
while True:
    first = input("\nFirst Number: ")
    second = input("Second Number: ")
    test_data = [float(first), float(second)]
    outputs = net.forward_prop(test_data)
    print(outputs)
    if outputs[0] > 0.5:
        print("First number is greater than the second!")
    else:
        print("Second number is greater than the first!")

