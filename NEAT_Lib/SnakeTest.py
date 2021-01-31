import time
import math
import numpy as np
import gc
import turtle

from NeuralNet import NeuralNet

from pynput import keyboard

class Snake():
    def __init__(self, play_as_human, neural_net):
        self.controllable = play_as_human
        self.direction = "right"
        self.alive = True
        self.pos_offset = 10*math.sqrt(2)
        self.empty_spaces = []
        self.body = []
        self.head = turtle.Turtle()
        self.food = turtle.Turtle()
        self.body_positions = []
        self.score = 0
        self.moves_till_death = 500
        self.total_moves = 0
        if play_as_human:
            self.delay = .05
        else:
            self.nn = neural_net
            self.delay = 0

    #kills snake
    def die(self):
        self.alive = False

    #sets direction of snake
    def set_direction(self,direction):
        self.direction = direction

    #removes the square at back of snake
    def remove_tail(self):
        tail = self.body.pop(len(self.body)-1)
        tail.ht()
        del tail
        tail_pos = self.body_positions.pop(len(self.body_positions)-1)
        self.empty_spaces.append((int(tail_pos[0]),int(tail_pos[1])))

    #adds a square at the old head location
    def new_top_body(self,xcor,ycor):
        self.body.insert(0,turtle.Turtle())
        self.body[0].shape("square")
        self.body[0].color("white")
        self.body[0].penup()
        self.body[0].setpos(xcor,ycor)
        self.body_positions.insert(0,(xcor,ycor))

    #performs 1 move for the snake
    def move(self):
        self.moves_till_death -= 1
        self.total_moves += 1
        oldx = self.head.xcor()
        oldy = self.head.ycor()
        #move to new location depending on snake direction
        if self.direction == "right":
            self.head.setx(oldx+20)
        elif self.direction == "left":
            self.head.setx(oldx-20)
        elif self.direction == "up":
            self.head.sety(oldy+20)
        else:
            self.head.sety(oldy-20)
        self.new_top_body(oldx,oldy)
        newx = int(self.head.xcor())
        newy = int(self.head.ycor())
        #if moved to food location
        if newx == int(self.food.xcor()) and newy == int(self.food.ycor()):
            self.score += 5
            self.moves_till_death = 500
            self.empty_spaces.remove((newx,newy))
            new_loc = np.random.randint(0,len(self.empty_spaces))
            self.food.setpos(self.empty_spaces[new_loc][0], self.empty_spaces[new_loc][1])
        else:
            self.remove_tail()
            #checks for death
            if self.empty_spaces.count((newx,newy)) == 0:
                self.die()
            elif self.moves_till_death == 0:
                self.die()
            else:
                self.empty_spaces.remove((newx,newy))

    #sets direction based on which key is pressed
    def on_press(self, key):
        if self.controllable:
            if key == keyboard.Key.up:
                self.set_direction("up")
            elif key == keyboard.Key.down:
                self.set_direction("down")
            elif key == keyboard.Key.left:
                self.set_direction("left")
            elif key == keyboard.Key.right:
                self.set_direction("right")
            else:
                pass

    def on_release(self,key):
        pass

    #calculates number of moves it would take to reach food, assuming clear path
    def distance_to_food(self, head_x, head_y):
        return abs(self.food.xcor()-head_x)/20 + abs(self.food.ycor()-head_y)/20

    #generate the inputs for the neural network based on information of the game state
    def generate_nn_inputs(self, head_x, head_y):
        inputs = []
        og_x = int(head_x)
        og_y = int(head_y)

        xr = int(head_x+20)
        xl = int(head_x-20)
        yu = int(head_y+20)
        yd = int(head_y-20)

        #looks to see which directions are safe. Appending a 1 = safe, 0 = death.
        #looks right
        if self.empty_spaces.count((xr, og_y)) == 0:
            inputs.append(0)
        else:
            inputs.append(1)
        #looks left
        if self.empty_spaces.count((xl, og_y)) == 0:
            inputs.append(0)
        else:
            inputs.append(1)
        #looks up
        if self.empty_spaces.count((og_x, yu)) == 0:
            inputs.append(0)
        else:
            inputs.append(1)
        #looks down
        if self.empty_spaces.count((og_x, yd)) == 0:
            inputs.append(0)
        else:
            inputs.append(1)
        #looks for food, Appends a 1 if food is in that direction, a 0 otherwise
        if self.food.xcor() >= xr:
            inputs.append(1)
        else:
            inputs.append(0)
        if self.food.xcor() <= xl:
            inputs.append(1)
        else:
            inputs.append(0)
        if self.food.ycor() >= yu:
            inputs.append(1)
        else:
            inputs.append(0)
        if self.food.ycor() <= yd:
            inputs.append(1)
        else:
            inputs.append(0)
        #adds input on how many moves are available until death
        #inputs.append(self.moves_till_death/500.0)
        return inputs

    #plays a full game of snake
    def new_game(self):
        listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        listener.start()
        self.window = turtle.Screen()
        #puts game window on top
        rootwindow = self.window.getcanvas().winfo_toplevel()
        rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
        rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
        self.initialize_game()
        self.window.update()
        while self.alive:
            time.sleep(self.delay)
            #if human is controlling snake
            if self.controllable:
                self.move()
            else:
                old_distance = self.distance_to_food(self.head.xcor(),self.head.ycor())
                inputs = self.generate_nn_inputs(self.head.xcor(),self.head.ycor())
                #performs forward propogation to get the neural networks prediction for the best move
                values = self.nn.forward_prop(inputs)
                result = values.index(max(values))
                if result == 0:
                    self.set_direction("up")
                elif result == 1:
                    self.set_direction("down")
                elif result == 2:
                    self.set_direction("right")
                else:
                    self.set_direction("left")
                self.move()
                new_distance = self.distance_to_food(self.head.xcor(),self.head.ycor())
                #adjusts score for neural network
                if new_distance < old_distance:
                    self.score += .05
                else:
                    self.score -= .05
            #updates game screen
            self.window.update()
        if self.controllable:
            print("\nYou died...")
            time.sleep(3)
        self.reset_window()
        #returns the score with a bonus added for how long the snake stayed alive
        return self.score + self.total_moves/75.0

    #resets the game window
    def reset_window(self):
        self.window.clear()
        self.window.reset()
        self.window.bgcolor("black")

    #sets up the game window
    def initialize_game(self):
        #initialize window
        self.window.title("Snake")
        self.window.bgcolor("black")
        self.window.setup(width = 1000, height = 600)
        self.window.tracer(0)

        #initialize walls
        wall_turt = turtle.Turtle()
        wall_turt.color("white")
        wall_turt.pencolor("white")
        wall_turt.penup()
        wall_turt.setpos(480,300)
        wall_turt.pensize(20)
        wall_turt.pendown()
        wall_turt.setpos(-490,300)
        wall_turt.setpos(-490,-290)
        wall_turt.setpos(480,-290)
        wall_turt.setpos(480,300)
        wall_turt.setpos(500,300)
        wall_turt.setpos(500,-290)

        #initialize snake head
        self.head.shape("square")
        self.head.color("white")
        self.head.penup()
        self.head.setpos(self.pos_offset,self.pos_offset)

        #initialize snake body
        for i in range(3):
            self.body.append(turtle.Turtle())
            self.body[i].shape("square")
            self.body[i].color("white")
            self.body[i].penup()
            self.body[i].setpos(self.pos_offset-20*(i+1),self.pos_offset)
            self.body_positions.append((self.pos_offset-20*(i+1),self.pos_offset))


        #initialize empty spaces
        for i in range(-24,23,1):
            for k in range(-14,14,1):
                if int(i*20 + self.pos_offset) != int(self.head.xcor()) or int(k*20 + self.pos_offset) != int(self.head.ycor()):
                    flag = True
                    for j in range(len(self.body_positions)):
                        if int(i*20 + self.pos_offset) == int(self.body_positions[j][0]) and int(k*20 + self.pos_offset) == int(self.body_positions[j][1]):
                            flag = False
                    if flag:
                        self.empty_spaces.append((int(i*20+self.pos_offset),int(k*20+self.pos_offset)))


        #initialize food location
        self.food.shape("square")
        self.food.color("red")
        self.food.penup()
        loc = np.random.randint(0,len(self.empty_spaces))
        self.food.setpos(self.empty_spaces[loc][0], self.empty_spaces[loc][1])
