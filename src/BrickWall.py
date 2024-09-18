import pygame
from src.Dependency import *
import random

class BrickWall:
    def __init__(self, x, y,screen):
        self.tier=0   #n->0
        self.color=1  #5->1
        self.type = 'wall'

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
        
    def update(self, dt):
        pass

    def render(self, screen,dt):

        if self.alive:
            screen.blit(brick_image_list[-2], (self.rect.x, self.rect.y))