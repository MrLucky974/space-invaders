import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
WIN_SIZE = WIDTH, HEIGHT

ENTITIES = pygame.sprite.Group()
ENEMIES = pygame.sprite.Group()
UFOG = pygame.sprite.Group()
BULLETS = pygame.sprite.Group()
EFFECTS = pygame.sprite.Group()
OBSTACLES = pygame.sprite.Group()

USER_INTERFACE = pygame.sprite.Group()


TEXTURES_PATH = "assets/textures"
PNG = ".png"

AUDIO_PATH = "assets/audio"
SOUNDS_PATH = AUDIO_PATH + "/sounds"
MUSIC_PATH = AUDIO_PATH + "/music"

LEVEL = 0