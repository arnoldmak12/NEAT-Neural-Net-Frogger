from SnakeTest import Snake
from Population import Population
from NNData import NNData
import time
import os

response = input("Please select an option: \n\n1.Play snake game\n2.Let computer learn to play\n0.Exit program\n")

while response != "0":
    if response == "1":
        print("\nGame starting...")
        time.sleep(1)
        snake = Snake(True,0)
        final_score = snake.new_game()
        print("\nYou finished with a score of: " + str(final_score))
    elif response == "2":
        print("\nYou have chosen to let the computer learn how to play.")
        print("The computer learns to play by generating random populations of snakes and letting them evolve and reproduce.")
        print("In essence, the computer is attempting to mimic how we evolve in nature.")
        print("\nNow that you understand how the computer will learn, you need to decide how many generations to simulate.")
        print("Each generation consists of 200 snakes. The snakes will move randomly at first but slowly learn to play over time.")
        print("\nKeep in mind that this process can take a long time depending on how many generations you choose to simulate.")
        num_generations = input("\nHow many generations do you want to simulate? (Smart snakes usually form by Generation 30): ")
        if num_generations == "0":
            print("\nSince you entered 0 generations, you will be returned to the main menu...\n")
        else:
            print("\nGame starting...")
            time.sleep(1)
            pop = Population(8, 4, 500, NNData())
            pop.simulate_generations(int(num_generations))
            break
            print("\n\nThe computer has kept the best snake from the last generation.")
            response = input("\nPlease select an option:\n\n1.Play game with computer snake\n0.Exit Program (your computer snake will be lost and the computer will have to retrain from scratch)\n")
            while response != "0":
                if response == "1":
                    print("\nGame starting...")
                    time.sleep(1)
                    pop.simulate_snake(best_snake)
                else:
                    print("\nYou have entered an invalid option. Please select again...\n")
                response = input("\nPlease select an option:\n\n1.Play game with computer snake\n0.Exit Program (your computer snake will be lost and the computer will have to retrain from scratch)\n")
            break
    else:
        print("\nYou entered an invalid option. Please enter a number from the options listed.\n\n")
    response = input("\nPlease select an option: \n\n1.Play snake game\n2.Let computer learn to play\n0.Exit program\n")
print("\n\nGoodybye!")
time.sleep(1)
os._exit(1)
