import pygame
from src.Dependency import *
import random

class Brick:
    def __init__(self, x, y,screen):
        self.tier=0   #n->0
        self.color=1  #5->1
        self.type = 'normal'

        self.x=x
        self.y=y

        self.width = 96
        self.height = 48

        self.screen = screen

        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.ballOne = 0


    def Hit(self):
        gSounds['brick-hit2'].play()
        
        # self.ballOne = Ball(6)
        # self.ballOne.rect.x = self.x
        # self.ballOne.rect.y = self.y
        # self.ballOne.dx = random.randint(-300,300)
        # self.ballOne.dy = random.randint(-300,300)

        # print(ballOne)
        if self.tier > 0:
            if self.color == 1:
                self.tier = self.tier - 1
                self.color = 5
            else:
                self.color = self.color - 1


        else:
            if self.color == 1:
                self.alive = False
            else:
                self.color = self.color - 1

        if not self.alive:
            gSounds['brick-hit1'].play()

    def update(self, dt):
        pass

    def render(self, screen,dt):

        if self.alive:

            screen.blit(brick_image_list[((self.color-1)*4)+self.tier], (self.rect.x, self.rect.y))