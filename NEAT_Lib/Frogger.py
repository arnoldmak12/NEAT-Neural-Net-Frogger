import pygame
import random
import time
from NeuralNet import NeuralNet
from GameData import GameData
import math
import numpy as np

class Frogger():
    def __init__(self):
        self.init_game()


    # Reset game board
    def reset(self):
        for r in self.game_data.get_turtles():
            r.kill()
        for r in self.game_data.get_all_sprites():
            r.kill()

        turtleCounter = 0

        # Creation of objects
        stable_vals = self.static_start
        offset1 = (np.random.randint(-150, 150), 0) [stable_vals]
        offset2 = (np.random.randint(-150, 150), 0) [stable_vals]
        offset3 = (np.random.randint(-150, 150), 0) [stable_vals]
        offset4 = (np.random.randint(-150, 150), 0) [stable_vals]
        offset5 = (np.random.randint(-150, 150), 0) [stable_vals]
        dist1 = (np.random.randint(150,250), 150) [stable_vals]
        dist2 = (np.random.randint(150,250), 150) [stable_vals]
        dist3 = (np.random.randint(150,250), 150) [stable_vals]
        dist4 = (np.random.randint(150,250), 150) [stable_vals]
        dist5 = (np.random.randint(300,400), 300) [stable_vals]
        #(x, y, img, speed, direction, width, height)
        for i in range(0, 12):
            if i < 3:
                self.game_data.add_all_sprites(self.Car(200 + dist1 * (3 - i) + offset1, 650, 'yellow', 6*4, 1, 50, 50, self.game_data))
            elif i < 6:
                self.game_data.add_all_sprites(self.Car(-300 + dist2 * (6 - i) + offset2, 600, 'dozer', 2*4, -1, 50, 50, self.game_data))
            elif i < 9:
                self.game_data.add_all_sprites(self.Car(100 + dist3 * (9 - i) + offset3, 550, 'purple', 4*4, 1, 50, 50, self.game_data))
            elif i < 10:
                self.game_data.add_all_sprites(self.Car(50 + dist4 * (10 - i) + offset4, 500, 'green', 10*4, -1, 50, 50, self.game_data))
            elif i < 12:
                self.game_data.add_all_sprites(self.Car(100 + dist5 * (12 - i) + offset5, 450, 'truck', 3*4, 1, 100, 50, self.game_data))

        for i in range(0, 9):
            if i < 3:
                self.game_data.add_all_sprites(self.Log(-200 + 350 * (3 - i), 300, 'short', 100, 50, 6*2, self.game_data))
            elif i < 6:
                self.game_data.add_all_sprites(self.Log(-300 + 450 * (6 - i), 250, 'long', 275, 50, 8*2, self.game_data))
            elif i < 9:
                self.game_data.add_all_sprites(self.Log(-400 + 350 * (9 - i), 150, 'medium', 150, 50, 12*2, self.game_data))

        for i in range(0, 8):
                # dive, size, startX, startY, width, height, speed
            if i < 4:
                if i == 2:
                    self.game_data.add_turtles(self.Turtle(2, 3, 250 * (4 - i), 350, 125, 50, -2*4, self.game_data))
                else:
                    self.game_data.add_turtles(self.Turtle(1, 3, 250 * (4 - i), 350, 125, 50, -2*4, self.game_data))
            elif i < 8:
                if i == 7:
                    self.game_data.add_turtles(self.Turtle(2, 2, 225 * (8 - i), 200, 75, 50, -2*4, self.game_data))
                else:
                    self.game_data.add_turtles(self.Turtle(1, 2, 225 * (8 - i), 200, 75, 50, -2*4, self.game_data))
        return


    def killAll(self):
        for i in self.game_data.get_frogs():
            if i.dead is False:
                i.die()
        return
    
    
    def begin_game(self, frog_pop, static_start):
        self.static_start = static_start
        self.reset()
        self.game_data.set_frogs_alive(len(frog_pop))
        for f in frog_pop:
            self.game_data.add_frogs(f)


        # Event handling loop (game loop)
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.screen.blit(self.game_data.backgroundImg, (0, 0))

            # If all frogs are dead, reset game board
            if self.game_data.get_frogs_alive() == 0:
                self.done = True

            self.game_data.get_all_sprites().update()
            self.game_data.get_all_sprites().draw(self.screen)
            self.game_data.get_turtles().update()
            self.game_data.get_turtles().draw(self.screen)
            self.game_data.get_frogs().update()
            self.game_data.get_frogs().draw(self.screen)

            pygame.display.update()

            self.clock.tick(self.fps)

            # Handling diving of turtle. Dives only at certain times
            self.turtleCounter += 1
            if self.turtleCounter == 50:
                self.turtleCounter = 0
                for t in self.game_data.get_turtles():
                    if t.dive == 2:
                        if t.state == 0:
                            t.state = 1
                            if t.size == 2:
                                t.image = self.game_data.turtleTwoDownImg
                            else:
                                t.image = self.game_data.turtleThreeDownImg
                        else:
                            t.state = 0
                            if t.size == 2:
                                t.image = self.game_data.turtleTwoImg
                            else:
                                t.image = self.game_data.turtleThreeImg

            self.game_data.inc_frame_count()


    def init_game(self):
        pygame.init()
        self.game_data = GameData()

        self.white = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.game_data.display_width, self.game_data.display_height))
        pygame.display.set_caption('Frogger')
        self.clock = pygame.time.Clock()
        

        self.frogsNum = 200  # Number of frogs spawned per generation
        self.done = False   # Application is still running
        self.turtleCounter = 0  # Timer for turtle state
        self.fps = 15  # Simulation speed (actions per second)


    # Classes


    class Turtle(pygame.sprite.Sprite):
        def __init__(self, dive, size, startX, startY, width, height, speed, data):
            pygame.sprite.Sprite.__init__(self)
            self.game_data = data
            self.dive = dive  # 1 - does not dive. 2 - dives
            self.size = size
            self.speed = speed
            self.width = width
            self.height = height
            self.state = 0  # State 0 - Not diving. State 1 - Diving

            self.image = pygame.Surface((self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.x = startX
            self.rect.y = startY

            if (self.size == 2):
                self.image = self.game_data.turtleTwoImg
            elif (self.size == 3):
                self.image = self.game_data.turtleThreeImg

        # Updating its new location
        def update(self):
            self.rect.x += self.speed

            if (self.size == 2):
                if (self.rect.x + 100 < 0):
                    self.rect.x = self.game_data.display_width + 100
            elif (self.size == 3):
                if (self.rect.x + 150 < 0):
                    self.rect.x = self.game_data.display_width + 150

            self.collision()

        # Checking if frog is on turtle. Frog dies if turtle is diving.
        def collision(self):
            for f in self.game_data.get_frogs():
                if f.rect.colliderect(self) and f.dead == False:
                    if self.state == 1:
                        f.die()
                    else:
                        f.rect.x += self.speed
            return


    class Frog(pygame.sprite.Sprite):
        dead = False
        reachedGoal = False
        fitness = 0

        def __init__(self, xpos, ypos, size, brain, data):
            pygame.sprite.Sprite.__init__(self)
            self.game_data = data
            self.image = pygame.Surface((50, 50))
            self.score = 0
            self.time_remaining = 60
            self.highest_dist = 0
            self.rect = self.image.get_rect()
            self.image = self.game_data.frogUpImg
            self.rect.x = xpos
            self.rect.y = ypos
            self.size = size
            self.brain = brain
            self.stabilityUp = self.stability(self.rect.x, self.rect.y - 50)
            self.stabilityDown = 0
            self.stabilityRight = self.stability(self.rect.x + 50, self.rect.y)
            self.stabilityLeft = self.stability(self.rect.x - 50, self.rect.y)
            self.stabilityCurrent = self.stability(self.rect.x, self.rect.y)
        

        
        def stability(self, x, y):
            stability = 0

            if y == 700 or y == 400:
                stability = 1

            elif x < 0 or x > 700 or y < 100 or y > 800:
                stability = 0

            elif y == 100:
                if x >= 55 and x <= 145:
                    stability = 1

                elif x >= 205 and x <= 295:
                    stability = 1

                elif x >= 355 and x <= 445:
                    stability = 1

                elif x >= 505 and x <= 595:
                    stability = 1

            elif y == 650 or y == 550:
                leftSide = 1
                rightSide = 0

                # This checks cars on current space, since cars traveling left, if none directly there, its perfectly safe
                for s in self.game_data.get_all_sprites():
                    if s.rect.y == y:
                        if x > (s.rect.x - 25) and x < (s.rect.x + 25):
                            leftSide = 0
        

                # This checks cars on right, since cars traveling left, looks for closest car to the frog
                foundObject = False
                tempX = x
                while foundObject is False and tempX < 700:
                    tempX += 50
                    for s in self.game_data.get_all_sprites():
                        if s.rect.y == y:
                            if tempX > (s.rect.x - 25) and tempX < (s.rect.x + 25):
                                rightSide = (tempX - x) / 50
                                foundObject = True

                if rightSide > 5:
                    rightSide = 5
                stability = 0 if leftSide == 0 else rightSide / 5 ######################################## CHNAGE THIS ##########################
            
            elif y == 600 or y == 500:
                leftSide = 0
                rightSide = 1

                # This checks cars on current space, since cars traveling right, if none directly there, its perfectly safe
                for s in self.game_data.get_all_sprites():
                    if s.rect.y == y:
                        if x > (s.rect.x - 25) and x < (s.rect.x + 25):
                            rightSide = 0
        

                # This checks cars on left, since cars traveling right, looks for closest car to the frog
                foundObject = False
                tempX = x
                while foundObject is False and tempX > 0:
                    tempX -= 50
                    for s in self.game_data.get_all_sprites():
                        if s.rect.y == y:
                            if tempX > (s.rect.x - 25) and tempX < (s.rect.x + 25):
                                leftSide = abs((tempX - x)) / 50
                                foundObject = True
                        

                if leftSide > 5:
                    leftSide = 5
                stability = 0 if rightSide == 0 else leftSide / 5 ######################################## CHNAGE THIS ##########################            


            elif y == 450:
                leftSide = 1
                rightSide = 0

                # This checks cars on current space, since cars traveling left, if none directly there, its perfectly safe
                for s in self.game_data.get_all_sprites():
                    if s.rect.y == y:
                        if x > (s.rect.x - 50) and x < (s.rect.x + 50):
                            leftSide = 0
        

                # This checks cars on right, since cars traveling left, looks for closest car to the frog
                foundObject = False
                tempX = x
                while foundObject is False and tempX < 700:
                    tempX += 50
                    for s in self.game_data.get_all_sprites():
                        if s.rect.y == y:
                            if tempX > (s.rect.x - 50) and tempX < (s.rect.x + 50):
                                rightSide = (tempX - x) / 50
                                foundObject = True

                if rightSide > 5:
                    rightSide = 5
                stability = 0 if leftSide == 0 else rightSide / 5 ######################################## CHNAGE THIS ##########################


            elif y == 350 or y == 200:
                for t in self.game_data.get_turtles():
                    if t.rect.y == y:
                        if x > (t.rect.x - ((t.size * 50 - 25) / 2)) and x < (t.rect.x + ((t.size * 50 - 25) / 2)) and t.state == 0:
                            stability = x / 1400.0 + 0.5

            elif y == 300 or y == 250 or y == 150:
                for s in self.game_data.get_all_sprites():
                    if s.rect.y == y:
                        if s.size == 'short':
                            if x > (s.rect.x - ((100 - 25) / 2)) and x < (s.rect.x + ((100 - 25) / 2)):
                                stability = 1 - (x / 1400.0)
                        if s.size == 'medium':
                            if x > (s.rect.x - ((150 - 25) / 2)) and x < (s.rect.x + ((150 - 25) / 2)):
                                stability = 1 - (x / 1400.0)
                        if s.size == 'long':
                            if x > (s.rect.x - ((275 - 25) / 2)) and x < (s.rect.x + ((275 - 25) / 2)):
                                stability = 1 - (x / 1400.0)

            if stability > 1:
                stability = 1
            #print("STAB at y-cord " + str(y) + "is: " + str(stability))
            return stability    
            
            
        # Update frog position
        def update(self):
            if self.dead:
                return
            self.time_remaining -= 1
            if self.time_remaining == 0:
                self.die()
                return
            if self.reachedGoal:
                self.score += (650/10)*self.game_data.get_frame_count()/(4000.0*100)
                return

            self.stabilityUp = self.stability(self.rect.x, self.rect.y - 50)
            self.stabilityDown = self.stability(self.rect.x, self.rect.y + 50)
            self.stabilityRight = self.stability(self.rect.x + 50, self.rect.y)
            self.stabilityLeft = self.stability(self.rect.x - 50, self.rect.y)
            self.stabilityCurrent = self.stability(self.rect.x, self.rect.y)

            stabilityUp2 = self.stability(self.rect.x, self.rect.y - 100)
            stabilityDown2 = self.stability(self.rect.x, self.rect.y + 100)
            stabilityRight2 = self.stability(self.rect.x + 100, self.rect.y)
            stabilityLeft2 = self.stability(self.rect.x - 100, self.rect.y)
            stabilityDTR = self.stability(self.rect.x + 50, self.rect.y - 50)
            stabilityDTL = self.stability(self.rect.x - 50, self.rect.y - 50)
            stabilityDBR = self.stability(self.rect.x + 50, self.rect.y + 50)
            stabilityDBL = self.stability(self.rect.x - 50, self.rect.y + 50)

            inputs = [self.stabilityUp, self.stabilityRight, self.stabilityDown, self.stabilityLeft, self.stabilityCurrent]

            extra = [stabilityUp2, stabilityDown2, stabilityRight2, stabilityLeft2, stabilityDTR, stabilityDTL, stabilityDBR, stabilityDBL]

            inputs.extend(extra)
            dist = max(750-self.rect.y, 0)
            if dist > self.highest_dist:
                self.highest_dist = dist
                self.time_remaining = 60
            values = self.brain.forward_prop(inputs)
            result = values.index(max(values))
            bonus = (dist/10)*self.game_data.get_frame_count()/(4000.0*100)
            if result == 0:
                self.rect.y -= 50
            elif result == 1:
                self.rect.x += 50
            elif result == 2:
                self.rect.y += 50
            elif result == 3:
                self.rect.x -= 50
            
            if self.rect.x < 0 or self.rect.x >= 700 or self.rect.y < 0 or self.rect.y >= 800:
                self.die()

            self.score += bonus

            # If frog is in the river
            if self.rect.y <= 350 and self.rect.y != 100 and self.dead == False:
                crash = False
                for x in self.game_data.get_all_sprites():
                    if x.rect.colliderect(self):
                        crash = True
                        break
                for x in self.game_data.get_turtles():
                    if x.rect.colliderect(self):
                        crash = True
                        break
                if crash == False:
                    self.die()
            elif self.rect.y == 100 and self.dead == False:
                if self.stability(self.rect.x, self.rect.y) == 1:
                    self.score += 200.0 / self.game_data.get_frame_count()
                    self.reachedGoal = True
                else:
                    self.image = self.game_data.frogDead
                    self.dead = True
                    self.score += self.highest_dist/50.0
                    self.game_data.sub_frogs_alive()

        # If the frog dies
        def die(self):
            self.score += self.highest_dist/50.0
            self.image = self.game_data.frogDead
            self.dead = True
            self.rect.x = -100
            self.game_data.sub_frogs_alive()


    class Log(pygame.sprite.Sprite):
        def __init__(self, startX, startY, size, width, height, speed, data):  # Constructor
            pygame.sprite.Sprite.__init__(self)
            self.size = size
            self.speed = speed
            self.width = width
            self.height = height
            self.game_data = data

            self.image = pygame.Surface((self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.x = startX
            self.rect.y = startY

            if (self.size == 'short'):
                self.image = self.game_data.logShortImg
            elif (self.size == 'medium'):
                self.image = self.game_data.logMediumImg
            elif (self.size == 'long'):
                self.image = self.game_data.logLongImg

        # Updating log position
        def update(self):
            self.rect.x += self.speed

            if (self.size == 'short' or self.size == 'medium'):
                if (self.rect.x - 200 > self.game_data.display_width):
                    self.rect.x = -200
            else:
                if (self.rect.x - 400 > self.game_data.display_width):
                    self.rect.x = -400

            self.collision()

        # Checking for collision with frog.
        def collision(self):
            for f in self.game_data.get_frogs():
                if f.rect.colliderect(self) and f.dead == False:
                    f.rect.x += self.speed
            return


    # Car Object
    class Car(pygame.sprite.Sprite):
        def __init__(self, startX, startY, img, speed, direction, width, height, data):  # Constructor
            pygame.sprite.Sprite.__init__(self)
            self.img = img
            self.speed = speed
            self.direction = direction  # (-1)-left (1)-right
            self.width = width
            self.height = height
            self.game_data = data

            self.image = pygame.Surface((self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.x = startX
            self.rect.y = startY

            if (self.img == 'yellow'):
                self.image = self.game_data.yellowCarImg
            elif (self.img == 'green'):
                self.image = self.game_data.greenCarImg
            elif (self.img == 'truck'):
                self.image = self.game_data.truckImg
            elif (self.img == 'dozer'):
                self.image = self.game_data.dozerImg
            elif (self.img == 'purple'):
                self.image = self.game_data.purpleCarImg

        # Update Car position
        def update(self):
            if (self.direction == -1):
                self.rect.x += self.speed
            elif (self.direction == 1):
                self.rect.x -= self.speed

            if (self.direction == -1 and self.rect.x - 150 > self.game_data.display_width):
                self.rect.x = -150
            elif (self.direction == 1 and self.rect.x + 150 < 0):
                self.rect.x = self.game_data.display_width + 150
            self.collision()

        # Checks car collision with frogs
        def collision(self):
            for f in self.game_data.get_frogs():
                if (self.rect.colliderect(f) and f.dead == False):
                    f.die()
            return

   


    
