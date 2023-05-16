from globals import *

import pygame
from pygame.locals import *


'''
Effects
'''


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 10
        self.current_frame = 0

        for frame in range(10):
            img = pygame.image.load(f"{TEXTURES_PATH}/explosion/explosion_{frame}{PNG}").convert()
            img.convert_alpha()

            self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        ENTITIES.add(self)
        EFFECTS.add(self)

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        if self.current_frame >= self.animation_frames - 1:
            self.destroy()

    def destroy(self):
        ENTITIES.remove(self)
        EFFECTS.remove(self)

        self.kill()
