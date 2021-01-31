import pygame
import random
import time
from NeuralNet import NeuralNet
from GameData import GameData
import math

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
        #(x, y, img, speed, direction, width, height)
        for i in range(0, 12):
            if i < 3:
                self.game_data.add_all_sprites(self.Car(200 + 150 * (3 - i), 650, 'yellow', 6, 1, 50, 50, self.game_data))
            elif i < 6:
                self.game_data.add_all_sprites(self.Car(-300 + 150 * (6 - i), 600, 'dozer', 2, -1, 50, 50, self.game_data))
            elif i < 9:
                self.game_data.add_all_sprites(self.Car(100 + 150 * (9 - i), 550, 'purple', 4, 1, 50, 50, self.game_data))
            elif i < 10:
                self.game_data.add_all_sprites(self.Car(50 + 150 * (10 - i), 500, 'green', 10, -1, 50, 50, self.game_data))
            elif i < 12:
                self.game_data.add_all_sprites(self.Car(100 + 300 * (12 - i), 450, 'truck', 3, 1, 100, 50, self.game_data))

        for i in range(0, 9):
            if i < 3:
                self.game_data.add_all_sprites(self.Log(-200 + 300 * (3 - i), 300, 'short', 100, 50, 6, self.game_data))
            elif i < 6:
                self.game_data.add_all_sprites(self.Log(-300 + 400 * (6 - i), 250, 'long', 275, 50, 8, self.game_data))
            elif i < 9:
                self.game_data.add_all_sprites(self.Log(-400 + 300 * (9 - i), 150, 'medium', 150, 50, 12, self.game_data))

        for i in range(0, 8):
                # dive, size, startX, startY, width, height, speed
            if i < 4:
                if i == 2:
                    self.game_data.add_turtles(self.Turtle(2, 3, 200 * (4 - i), 350, 125, 50, -2, self.game_data))
                else:
                    self.game_data.add_turtles(self.Turtle(1, 3, 200 * (4 - i), 350, 125, 50, -2, self.game_data))
            elif i < 8:
                if i == 7:
                    self.game_data.add_turtles(self.Turtle(2, 2, 175 * (8 - i), 200, 75, 50, -2, self.game_data))
                else:
                    self.game_data.add_turtles(self.Turtle(1, 2, 175 * (8 - i), 200, 75, 50, -2, self.game_data))
        return


    def killAll(self):
        print("-------------- TIME RAN OUT ----- ")
        for i in self.frogs:
            if i.dead is False:
                i.die()
        return
    
    
    def begin_game(self, frog_pop):
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

            
            self.total_seconds = self.game_data.get_frame_count() // self.fps

            if self.total_seconds > 5:
                self.done = True

            #message_display('generation: ' + str(pop.generation))
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
        #pygame.quit()


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
        self.fps = 30  # Simulation speed (actions per second)


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
                if x >= 80 and x <= 170:
                    stability = 1

                elif x >= 230 and x <= 320:
                    stability = 1

                elif x >= 380 and x <= 470:
                    stability = 1

                elif x >= 530 and x <= 620:
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

                stability = 0 if leftSide == 0 else rightSide / 10 ######################################## CHNAGE THIS ##########################
            
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
                        

                stability = 0 if rightSide == 0 else leftSide / 10 ######################################## CHNAGE THIS ##########################            


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

                stability = 0 if leftSide == 0 else rightSide / 10 ######################################## CHNAGE THIS ##########################


            elif y == 350 or y == 200:
                for t in self.game_data.get_turtles():
                    if t.rect.y == y:
                        if x > (t.rect.x - ((t.size * 50 - 25) / 2)) and x < (t.rect.x + ((t.size * 50 - 25) / 2)) and t.state == 0:
                            stability = x / 700

            elif y == 300 or y == 250 or 150:
                for s in self.game_data.get_all_sprites():
                    if s.rect.y == y:
                        if s.size == 'short':
                            if x > (s.rect.x - ((100 - 25) / 2)) and x < (s.rect.x + ((100 - 25) / 2)):
                                stability = 1 - (x / 700)
                        if s.size == 'medium':
                            if x > (s.rect.x - ((150 - 25) / 2)) and x < (s.rect.x + ((150 - 25) / 2)):
                                stability = 1 - (x / 700)
                        if s.size == 'long':
                            if x > (s.rect.x - ((275 - 25) / 2)) and x < (s.rect.x + ((275 - 25) / 2)):
                                stability = 1 - (x / 700)

            #print("STAB at y-cord " + str(y) + "is: " + str(stability))
            return stability    
            
            
        # Update frog position
        def update(self):
            if self.dead:
                return
            self.stabilityUp = self.stability(self.rect.x, self.rect.y - 50)
            self.stabilityDown = self.stability(self.rect.x, self.rect.y + 50)
            self.stabilityRight = self.stability(self.rect.x + 50, self.rect.y)
            self.stabilityLeft = self.stability(self.rect.x - 50, self.rect.y)
            self.stabilityCurrent = self.stability(self.rect.x, self.rect.y)

            inputs = [self.stabilityUp, self.stabilityRight, self.stabilityDown, self.stabilityLeft, self.stabilityCurrent]
            dist = max(700-self.rect.y, 0)
            distances = [(dist-50/14.0), dist/14.0, (dist+50)/14.0, dist/14.0, dist/14.0]
            inputs.extend(distances)
            values = self.brain.forward_prop(inputs)
            result = values.index(max(values))
            bonus = (dist/50)*self.game_data.get_frame_count()/20.0
            if result == 0:
                self.rect.y -= 50
            elif result == 1:
                self.rect.x += 50
            elif result == 2:
                self.rect.y += 50
            elif result == 3:
                self.rect.x -= 50
            
            if self.rect.x < 0 or self.rect.x > 700 or self.rect.y < 0 or self.rect.y > 800:
                self.die()

            if result != 4:
                self.score += bonus

            # If frog is in the river
            if self.rect.y <= 350 and self.rect.y != 100 and self.dead == False:
                crash = False
                for x in self.game_data.get_all_sprites():
                    if x.rect.colliderect(self):
                        crash = True
                        break
                for x in turtles:
                    if x.rect.colliderect(self):
                        crash = True
                        break
                if crash == False:
                    self.die()
            elif self.rect.y == 100 and self.dead == False:
                self.fitness = 13
                self.dead = True
                self.frogs_alive -= 1

            self.stabilityUp = self.stability(self.rect.x, self.rect.y - 50)
            self.stabilityDown = self.stability(self.rect.x, self.rect.y + 50)
            self.stabilityRight = self.stability(self.rect.x + 50, self.rect.y)
            self.stabilityLeft = self.stability(self.rect.x - 50, self.rect.y)
            self.stabilityCurrent = self.stability(self.rect.x, self.rect.y)

        # If the frog dies
        def die(self):
            self.score += max(700-self.rect.y, 0)
            self.image = self.game_data.frogDead
            self.dead = True
            self.rect.x = -100
            self.game_data.sub_frogs_alive()
            #print('Frogs alive: ' + str(self.game_data.get_frogs_alive()))
            #print('Frogs Score: ' + str(self.score))


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

    # Randomly mutates the direction vectors of the given frog


    

   


    def text_objects(text, font):
        textSurface = font.render(text, True, white)
        return textSurface, textSurface.get_rect()


    def message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf', 24)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((display_width / 2), 20)
        screen.blit(TextSurf, TextRect)


    