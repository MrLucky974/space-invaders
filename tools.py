from globals import HEIGHT, USER_INTERFACE, WIDTH

import pygame
from pygame.locals import *


'''
Tools
'''


class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, color: tuple, x: float, y: float, font):
        pygame.sprite.Sprite.__init__(self)

        self.text = text
        self.font = font
        self.color = color

        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect(topleft=(x, y))

        USER_INTERFACE.add(self)

    def update(self):
        self.image = self.font.render(self.text, True, self.color)


class Background:
    def __init__(self):
        self.bgimage = pygame.image.load('assets/textures/background.png')
        self.rectBGimg = self.bgimage.get_rect()
        self.bgimage = pygame.transform.scale(self.bgimage, (int(WIDTH / self.rectBGimg.width * self.rectBGimg.width),
                                                             int(WIDTH / self.rectBGimg.width * self.rectBGimg.height)))
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingUpSpeed = 1

    def update(self):
        self.bgY1 += self.movingUpSpeed
        self.bgY2 += self.movingUpSpeed

        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height
        # if self.bgY1 <= -self.rectBGimg.height:
        #    self.bgY1 = self.rectBGimg.height
        # if self.bgY2 <= -self.rectBGimg.height:
        #    self.bgY2 = self.rectBGimg.height

    def render(self, screen):
        screen.blit(self.bgimage, (self.bgX1, self.bgY1))
        screen.blit(self.bgimage, (self.bgX2, self.bgY2))
