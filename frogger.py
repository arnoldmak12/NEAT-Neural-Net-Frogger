import pygame
import random
import time

pygame.init()
display_width = 700
display_height = 800

white = (255, 255, 255)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
turtles = pygame.sprite.Group()
frogs = pygame.sprite.Group()

frogUpImg = pygame.transform.scale2x(pygame.image.load('sprites/frog10.gif'))
frogDead = pygame.transform.scale2x(pygame.image.load('sprites/frog11.png'))

yellowCarImg = pygame.transform.scale2x(pygame.image.load('sprites/yellowCar.gif'))  # 2nd Row
dozerImg = pygame.transform.scale2x(pygame.image.load('sprites/dozer.gif'))  # 3rd Row
purpleCarImg = pygame.transform.scale2x(pygame.image.load('sprites/purpleCar.gif'))  # 4th Row
greenCarImg = pygame.transform.scale2x(pygame.image.load('sprites/greenCar.gif'))  # 5th Row
truckImg = pygame.transform.scale2x(pygame.image.load('sprites/truck.gif'))  # 6th Row

logShortImg = pygame.transform.scale2x(pygame.image.load('sprites/logShort.gif'))
logMediumImg = pygame.transform.scale2x(pygame.image.load('sprites/logMedium.gif'))
logLongImg = pygame.transform.scale2x(pygame.image.load('sprites/logLong.gif'))

turtleTwoImg = pygame.transform.scale2x(pygame.image.load('sprites/turtletwo.gif'))
turtleTwoDownImg = pygame.transform.scale2x(pygame.image.load('sprites/turtletwodown.gif'))
turtleThreeImg = pygame.transform.scale2x(pygame.image.load('sprites/turtlethree.gif'))
turtleThreeDownImg = pygame.transform.scale2x(pygame.image.load('sprites/turtlethreedown.gif'))

backgroundImg = pygame.transform.scale2x(pygame.image.load('sprites/background.gif'))

frogsNum = 100  # Number of frogs spawned per generation
done = False   # Application is still running
turtleCounter = 0  # Timer for turtle state
fps = 5  # Simulation speed (actions per second)
frame_count = 0


# Classes


class Population:
    bestFrog = 0  # The index for the best (most fit) frog
    minStep = 1000  # The fastest route to get to the highest fitness
    fitnessSum = 0  # Sum of all frogs' fitness
    frogs_alive = frogsNum  # All frogs are alive at the beginning
    isFinished = False  # Whether or not a frog has ever reached the end
    generation = 1

    def __init__(self, tests, size):  # Constructor
        self.frogs_alive = tests
        self.size = size
        self.tests = tests
        self.randomize()

    # Randomizes the frog's directions
    def randomize(self):
        for i in range(0, self.tests):
            directions = []
            for z in range(0, self.size):
                randomNum = random.randint(0, 4)
                directions.append(randomNum)

            b = Brain(1000, directions)
            frogs.add(Frog(335, 700, self.size, b))

    # Randomly selecting a parent frog from previous generation
    def selectParent(self):
        self.setFitnessSum()
        rand = random.randint(frogsNum, self.fitnessSum)
        runningSum = 0

        for i in frogs:
            runningSum += i.fitness
            if runningSum >= rand:
                return i.brain.directions

    # Finding the sum of all the fitnesses from previous generation
    def setFitnessSum(self):
        sum = 0
        for i in frogs:
            sum += i.fitness
        self.fitnessSum = sum

    # Selecting a new generation of frogs
    def selection(self):
        temp = list(self.bestFrog())
        newFrogs = []
        if (self.isFinished == False):
            d = list(temp)
            b = Brain(1000, d)
            newFrogs.append(Frog(335, 700, self.size, b))

            for x in range(1, frogsNum):
                d = list(self.selectParent())
                b = Brain(1000, mutate(d))
                newFrogs.append(Frog(335, 700, self.size, b))
            Population.frogs_alive = frogsNum

            frogs.empty()
            for i in newFrogs:
                frogs.add(i)
        else:
            frogs.empty()
            for x in range(0, 1):
                d = list(temp)
                b = Brain(1000, d)
                frogs.add(Frog(335, 700, self.size, b))
            Population.frogs_alive = 1

    def killAll(self):
        print("-------------- TIME RAN OUT ----- ")
        for i in frogs:
            if i.dead is False:
                i.die()


    # Determining the best frog from the previous generation and returning its directions
    def bestFrog(self):
        if (self.isFinished == False):

            fitnessList = []
            stepsList = []
            for sprite in frogs:
                stepsList.append(sprite.brain.step)
                fitnessList.append(sprite.fitness)

            for i in range(0, frogsNum - 1):
                for j in range(0, frogsNum - 1):
                    if (fitnessList[j] > fitnessList[j + 1]):
                        temp = fitnessList[j]
                        fitnessList[j] = fitnessList[j + 1]
                        fitnessList[j + 1] = temp

                        temp = stepsList[j]
                        stepsList[j] = stepsList[j + 1]
                        stepsList[j + 1] = temp

            print(fitnessList[frogsNum - 1])
            print(stepsList[frogsNum - 1])

            best = frogsNum - 1
            for h in range(0, frogsNum - 1):
                if stepsList[h] < stepsList[frogsNum - 1] and fitnessList[frogsNum - 1] == fitnessList[h]:
                    best = h

            print(fitnessList[best])
            print(stepsList[best])

            if (fitnessList[best] == 13):
                self.isFinished = True
            else:
                self.generation += 1

            for sprite in frogs:
                if (fitnessList[best] == sprite.fitness and stepsList[best] == sprite.brain.step):
                    bestFrog = list(sprite.brain.directions)
                    print(str(sprite.fitness) + '   ' + str(sprite.brain.step))
                    break

            return bestFrog

        else:
            for sprite in frogs:
                bestFrog = list(sprite.brain.directions)
            return bestFrog


class Brain:
    step = 0

    def __init__(self, size, directions):
        self.size = size
        self.directions = directions


class Turtle(pygame.sprite.Sprite):
    def __init__(self, dive, size, startX, startY, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
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
            self.image = turtleTwoImg
        elif (self.size == 3):
            self.image = turtleThreeImg

    # Updating its new location
    def update(self):
        self.rect.x += self.speed

        if (self.size == 2):
            if (self.rect.x + 100 < 0):
                self.rect.x = display_width + 100
        elif (self.size == 3):
            if (self.rect.x + 150 < 0):
                self.rect.x = display_width + 150

        self.collision()

    # Checking if frog is on turtle. Frog dies if turtle is diving.
    def collision(self):
        for f in frogs:
            if f.rect.colliderect(self) and f.dead == False:
                if self.state == 1:
                    f.die()
                else:
                    f.rect.x += self.speed


class Frog(pygame.sprite.Sprite):
    dead = False
    reachedGoal = False
    fitness = 0

    def __init__(self, xpos, ypos, size, brain):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.image = frogUpImg
        self.rect.x = xpos
        self.rect.y = ypos
        self.size = size
        self.brain = brain

    # Update frog position
    def update(self):
        stepNum = self.brain.step
        if stepNum < self.size and self.dead == False:
            if self.brain.directions[stepNum] == 1:
                self.rect.y -= 50
                self.fitness += 1
            elif self.brain.directions[stepNum] == 2 and self.rect.y < 375:
                self.rect.y += 50
                self.fitness -= 1
            elif self.brain.directions[stepNum] == 3 and self.rect.x > 25:
                self.rect.x -= 50
            elif self.brain.directions[stepNum] == 4 and self.rect.x < 300:
                self.rect.x += 50

            self.brain.step += 1

        # If frog is in the river
        if self.rect.y <= 350 and self.rect.y != 100 and self.dead == False:
            crash = False
            for x in all_sprites:
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
            Population.frogs_alive -= 1

    # If the frog dies
    def die(self):
        self.image = frogDead
        self.dead = True
        Population.frogs_alive -= 1
        print('Frogs alive: ' + str(Population.frogs_alive))


class Log(pygame.sprite.Sprite):
    def __init__(self, startX, startY, size, width, height, speed):  # Constructor
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY

        if (self.size == 'short'):
            self.image = logShortImg
        elif (self.size == 'medium'):
            self.image = logMediumImg
        elif (self.size == 'long'):
            self.image = logLongImg

    # Updating log position
    def update(self):
        self.rect.x += self.speed

        if (self.size == 'short' or self.size == 'medium'):
            if (self.rect.x - 200 > display_width):
                self.rect.x = -200
        else:
            if (self.rect.x - 400 > display_width):
                self.rect.x = -400

        self.collision()

    # Checking for collision with frog.
    def collision(self):
        for f in frogs:
            if f.rect.colliderect(self) and f.dead == False:
                f.rect.x += self.speed


# Car Object
class Car(pygame.sprite.Sprite):
    def __init__(self, startX, startY, img, speed, direction, width, height):  # Constructor
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.speed = speed
        self.direction = direction  # (-1)-left (1)-right
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY

        if (self.img == 'yellow'):
            self.image = yellowCarImg
        elif (self.img == 'green'):
            self.image = greenCarImg
        elif (self.img == 'truck'):
            self.image = truckImg
        elif (self.img == 'dozer'):
            self.image = dozerImg
        elif (self.img == 'purple'):
            self.image = purpleCarImg

    # Update Car position
    def update(self):
        if (self.direction == -1):
            self.rect.x += self.speed
        elif (self.direction == 1):
            self.rect.x -= self.speed

        if (self.direction == -1 and self.rect.x - 150 > display_width):
            self.rect.x = -150
        elif (self.direction == 1 and self.rect.x + 150 < 0):
            self.rect.x = display_width + 150
        self.collision()

    # Checks car collision with frogs
    def collision(self):
        for f in frogs:
            if (self.rect.colliderect(f) and f.dead == False):
                f.die()

# Randomly mutates the direction vectors of the given frog


def mutate(d):
    for i in range(0, len(d)):
        randomNum = random.randint(0, 4)
        if randomNum == 1:
            d[i] = random.randint(0, 4)
    return d

# Reset game board


def reset():
    for r in turtles:
        r.kill()
    for r in all_sprites:
        r.kill()

    turtleCounter = 0

    # Creation of objects
    #(x, y, img, speed, direction, width, height)
    for i in range(0, 12):
        if i < 3:
            all_sprites.add(Car(200 + 150 * (3 - i), 650, 'yellow', 6, 1, 50, 50))
        elif i < 6:
            all_sprites.add(Car(-300 + 150 * (6 - i), 600, 'dozer', 2, -1, 50, 50))
        elif i < 9:
            all_sprites.add(Car(100 + 150 * (9 - i), 550, 'purple', 4, 1, 50, 50))
        elif i < 10:
            all_sprites.add(Car(50 + 150 * (10 - i), 500, 'green', 10, -1, 50, 50))
        elif i < 12:
            all_sprites.add(Car(100 + 300 * (12 - i), 450, 'truck', 3, 1, 100, 50))

    for i in range(0, 9):
        if i < 3:
            all_sprites.add(Log(-200 + 300 * (3 - i), 300, 'short', 62.5, 50, 6))
        elif i < 6:
            all_sprites.add(Log(-300 + 400 * (6 - i), 250, 'long', 150, 50, 8))
        elif i < 9:
            all_sprites.add(Log(-400 + 300 * (9 - i), 150, 'medium', 87.5, 50, 12))

    for i in range(0, 8):
            # dive, size, startX, startY, width, height, speed
        if i < 4:
            if i == 2:
                turtles.add(Turtle(2, 3, 200 * (4 - i), 350, 150, 50, -2))
            else:
                turtles.add(Turtle(1, 3, 200 * (4 - i), 350, 150, 50, -2))
        elif i < 8:
            if i == 7:
                turtles.add(Turtle(2, 2, 175 * (8 - i), 200, 100, 50, -2))
            else:
                turtles.add(Turtle(1, 2, 175 * (8 - i), 200, 100, 50, -2))


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 24)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), 20)
    screen.blit(TextSurf, TextRect)


pop = Population(frogsNum, 1000)
reset()


# Event handling loop (game loop)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(backgroundImg, (0, 0))

    # If all frogs are dead, reset game board
    if (Population.frogs_alive == 0):
        pop.selection()
        reset()
        time.sleep(1)

            
    total_seconds = frame_count // fps

    if total_seconds > 2:
        pop.killAll()
        pop.selection()
        reset()
        time.sleep(1)
        frame_count = 0;

    print (total_seconds) #print how many seconds

    message_display('generation: ' + str(pop.generation))
    all_sprites.update()
    all_sprites.draw(screen)
    turtles.update()
    turtles.draw(screen)
    frogs.update()
    frogs.draw(screen)

    pygame.display.update()

    clock.tick(fps)

    # Handling diving of turtle. Dives only at certain times
    turtleCounter += 1
    if turtleCounter == 50:
        turtleCounter = 0
        for t in turtles:
            if t.dive == 2:
                if t.state == 0:
                    t.state = 1
                    if t.size == 2:
                        t.image = turtleTwoDownImg
                    else:
                        t.image = turtleThreeDownImg
                else:
                    t.state = 0
                    if t.size == 2:
                        t.image = turtleTwoImg
                    else:
                        t.image = turtleThreeImg

    frame_count+=1

pygame.quit()
quit()