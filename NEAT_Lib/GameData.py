import pygame
class GameData(object):
    def __init__(self):
        global all_sprites
        global turtles
        global frogs
        global frogs_alive
        global frame_count
        all_sprites = pygame.sprite.Group()
        turtles = pygame.sprite.Group()
        frogs = pygame.sprite.Group()
        frogs_alive = 200
        frame_count = 0

        self.display_width = 700
        self.display_height = 800

        self.frogUpImg = pygame.transform.scale2x(pygame.image.load('sprites/frog10.gif'))
        self.frogDead = pygame.transform.scale2x(pygame.image.load('sprites/frog11.png'))

        self.yellowCarImg = pygame.transform.scale2x(pygame.image.load('sprites/yellowCar.gif'))  # 2nd Row
        self.dozerImg = pygame.transform.scale2x(pygame.image.load('sprites/dozer.gif'))  # 3rd Row
        self.purpleCarImg = pygame.transform.scale2x(pygame.image.load('sprites/purpleCar.gif'))  # 4th Row
        self.greenCarImg = pygame.transform.scale2x(pygame.image.load('sprites/greenCar.gif'))  # 5th Row
        self.truckImg = pygame.transform.scale2x(pygame.image.load('sprites/truck.gif'))  # 6th Row

        self.logShortImg = pygame.transform.scale2x(pygame.image.load('sprites/logShort.gif'))
        self.logMediumImg = pygame.transform.scale2x(pygame.image.load('sprites/logMedium.gif'))
        self.logLongImg = pygame.transform.scale2x(pygame.image.load('sprites/logLong.gif'))

        self.turtleTwoImg = pygame.transform.scale2x(pygame.image.load('sprites/turtletwo.gif'))
        self.turtleTwoDownImg = pygame.transform.scale2x(pygame.image.load('sprites/turtletwodown.gif'))
        self.turtleThreeImg = pygame.transform.scale2x(pygame.image.load('sprites/turtlethree.gif'))
        self.turtleThreeDownImg = pygame.transform.scale2x(pygame.image.load('sprites/turtlethreedown.gif'))

        self.backgroundImg = pygame.transform.scale2x(pygame.image.load('sprites/background.gif'))


    def get_all_sprites(self):
        global all_sprites
        return all_sprites


    def get_frogs(self):
        global frogs
        return frogs


    def get_frogs_alive(self):
        global frogs_alive
        return frogs_alive


    def sub_frogs_alive(self):
        global frogs_alive
        frogs_alive -= 1


    def get_frame_count(self):
        global frame_count
        return frame_count


    def inc_frame_count(self):
        global frame_count
        frame_count += 1

    def set_frogs_alive(self, num):
        global frogs_alive
        frogs_alive = num


    def add_all_sprites(self, new_obj):
        global all_sprites
        all_sprites.add(new_obj)


    def add_turtles(self, new_obj):
        global turtles
        turtles.add(new_obj)


    def add_frogs(self, new_obj):
        global frogs
        frogs.add(new_obj)

    def get_turtles(self):
        global turtles
        return turtles


