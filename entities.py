from globals import *
from effects import Explosion

import pygame
from pygame.locals import *
import random
from arcade import clamp
import time


'''
Entities
'''


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(TEXTURES_PATH + "/player/debug/player_debug" + PNG).convert().convert_alpha()
        self.rect = self.image.get_rect()

        self.speed = 150

        self.bullet = None

        ENTITIES.add(self)

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.centerx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            if self.rect.x < WIDTH - self.rect.width:
                self.rect.centerx += (self.speed + 50) * dt

    def shoot(self):
        if self.bullet is None:
            bullet = Laser(parent=self, laser_type=2)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.centery = self.rect.centery - self.rect.height
            self.bullet = bullet

            SHOOT_SOUND = pygame.mixer.Sound(SOUNDS_PATH + '/effects/shoot.wav')
            SHOOT_SOUND.set_volume(1.0)
            SHOOT_SOUND.play()

    def update(self, dt):
        if self.bullet is not None:
            if self.bullet.destroyed:
                self.bullet = None

        self.move(dt)


class Laser(pygame.sprite.Sprite):
    def __init__(self, parent, laser_type: int = 1):
        pygame.sprite.Sprite.__init__(self)

        self.parent = parent

        laser_type = clamp(laser_type, 1, 2)

        img = pygame.image.load(f"{TEXTURES_PATH}/laser_{laser_type}{PNG}").convert().convert_alpha()

        self.destroyed = False

        self.image = img
        self.rect = self.image.get_rect()

        self.vertical_direction = -1
        self.speed = 350

        ENTITIES.add(self)
        BULLETS.add(self)

    def move(self, dt):
        self.rect.centery += self.speed * dt * self.vertical_direction

    def update(self, dt):
        self.move(dt)

    def destroy(self):
        ENTITIES.remove(self)
        BULLETS.remove(self)

        self.destroyed = True

        self.kill()


class Block(pygame.sprite.Sprite):
    default_shape = [
        '  xxxxxxx',
        ' xxxxxxxxx',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxx     xxx',
        'xx       xx'
    ]

    default_size = 6

    def __init__(self, size, color, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

        ENTITIES.add(self)
        OBSTACLES.add(self)

    def destroy(self):
        ENTITIES.remove(self)
        OBSTACLES.remove(self)

        self.kill()


def create_obstacle(x_start, y_start, x_offset):
    for row_index, row in enumerate(Block.default_shape):
        for column_index, column in enumerate(row):
            if column == 'x':
                x = x_start + column_index * Block.default_size + x_offset
                y = y_start + row_index * Block.default_size
                block = Block(6, (241, 79, 80), x, y)


def create_multiple_obstacles(x_start, y_start, amount, *offset):
    for x in range(amount):
        create_obstacle(x_start, y_start, offset[x])


class EnemyManager:
    directions = {
        "DOWN": 0,
        "LEFT": 1,
        "RIGHT": 2
    }

    def __init__(self) -> None:
        self.direction = EnemyManager.directions["RIGHT"]
        self.last_direction = EnemyManager.directions["LEFT"]

        self.countdown_reset = 1.0
        self.countdown = self.countdown_reset
        self.sound_countdown = self.countdown_reset
        self.speed = 10.0

        for enemy in ENEMIES:
            enemy.manager = self

    def update(self, dt):
        self.countdown -= dt
        self.sound_countdown -= dt

        if self.countdown <= 0:
            for enemy in ENEMIES:
                if type(enemy) != UFO:
                    if (enemy.rect.x + enemy.rect.width * 1.25 >= WIDTH and self.direction == EnemyManager.directions["RIGHT"]) or (enemy.rect.x <= enemy.rect.width * 0.5 and self.direction == EnemyManager.directions["LEFT"]):
                        self.last_direction = self.direction
                        self.direction = EnemyManager.directions["DOWN"]

            for enemy in ENEMIES:
                if self.direction == EnemyManager.directions["RIGHT"]:
                    if type(enemy) != UFO:
                        # enemy.rect.x += self.speed
                        enemy.move(self.speed, 0)

                elif self.direction == EnemyManager.directions["LEFT"]:
                    if type(enemy) != UFO:
                        # enemy.rect.x -= self.speed
                        enemy.move(-self.speed, 0)

                elif self.direction == EnemyManager.directions["DOWN"]:
                    if type(enemy) != UFO:
                        # enemy.rect.y += self.speed
                        enemy.move(0, self.speed)

            if self.last_direction == EnemyManager.directions["RIGHT"]:
                self.direction = EnemyManager.directions["LEFT"]
            elif self.last_direction == EnemyManager.directions["LEFT"]:
                self.direction = EnemyManager.directions["RIGHT"]

            self.countdown = self.countdown_reset

        if self.sound_countdown <= 0:
            if len(ENEMIES) - len(UFOG) > 0:
                MOVE_SND = pygame.mixer.Sound(SOUNDS_PATH + '/effects/fastinvader1.wav')
                MOVE_SND.set_volume(1.0)
                MOVE_SND.play()

            self.sound_countdown = clamp(self.countdown_reset, 0.15, 1)


class Enemy(pygame.sprite.Sprite):
    score = 0

    def __init__(self, sprite_name: str, frames: int, color: tuple):
        pygame.sprite.Sprite.__init__(self)
        self.manager: EnemyManager = None

        self.sprite_name = sprite_name
        self.images = []

        self.animation_time = 0.25
        self.current_time = 0

        self.animation_frames = frames
        self.current_frame = 0

        for frame in range(frames):
            img = pygame.image.load(f"{TEXTURES_PATH}/enemies/{sprite_name}_{frame}{PNG}").convert_alpha()

            color_shift = pygame.Surface(img.get_size()).convert_alpha()
            color_shift.fill(color)
            img.blit(color_shift, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        ENTITIES.add(self)
        ENEMIES.add(self)

        self.health = 1
        self.killed = False

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def update(self, dt):
        if self.health <= 0:
            self.destroy()

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

    def shoot(self):
        bullet = Laser(parent=self, laser_type=1)

        bullet.rect.centerx = self.rect.centerx
        bullet.rect.centery = self.rect.centery + self.rect.height
        bullet.vertical_direction = 1

    def destroy(self):
        ENTITIES.remove(self)
        ENEMIES.remove(self)

        if self.killed:
            DEATH_SND = pygame.mixer.Sound(SOUNDS_PATH + '/effects/invaderkilled.wav')
            DEATH_SND.set_volume(1.0)
            DEATH_SND.play()

            explosion = Explosion()
            explosion.rect.centerx = self.rect.centerx
            explosion.rect.centery = self.rect.centery

        self.manager.countdown_reset -= 0.017  # 0.015

        self.kill()


class Kani(Enemy):
    score = 20

    def __init__(self):
        super().__init__(sprite_name="kani_depth", frames=2, color=(183, 50, 255))

        self.health = 1


class Kura(Enemy):
    score = 10

    def __init__(self):
        super().__init__(sprite_name="kura", frames=2, color=(0, 148, 255))

        self.health = 3


class Ika(Enemy):
    score = 30

    def __init__(self):
        super().__init__(sprite_name="ika_depth", frames=2, color=(76, 255, 0))

        self.health = 1


class Tako(Enemy):
    score = 50

    def __init__(self):
        super().__init__(sprite_name="tako", frames=2, color=(255, 216, 0))

        self.health = 2


class Kumo(Enemy):
    score = 10

    def __init__(self):
        super().__init__(sprite_name="kumo", frames=2, color=(255, 106, 0))

        self.health = 1


class UFO(Enemy):
    score = 100

    def __init__(self):
        super().__init__(sprite_name="ufo_depth", frames=1, color=(255, 0, 0))
        UFOG.add(self)

        self.direction = 0
        self.speed = 200

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def update(self, dt):
        if self.rect.x + self.rect.width <= 0 or self.rect.x >= WIDTH:
            self.destroy()

        self.move(dt)

    def destroy(self):
        ENTITIES.remove(self)
        ENEMIES.remove(self)
        UFOG.remove(self)

        if self.killed:
            DEATH_SND = pygame.mixer.Sound(SOUNDS_PATH + '/effects/invaderkilled.wav')
            DEATH_SND.set_volume(1.0)
            DEATH_SND.play()

            explosion = Explosion()
            explosion.rect.centerx = self.rect.centerx
            explosion.rect.centery = self.rect.centery

        self.kill()


def alien_setup(rows, columns, x_distance=60, y_distance=48, x_offset=75, y_offset=20):
    for row_index, row in enumerate(range(rows)):
        for column_index, column in enumerate(range(columns)):
            x = column_index * x_distance + x_offset
            y = row_index * y_distance + y_offset

            if row == 0:
                alien = Ika()
                alien.rect.x = x
                alien.rect.y = y
            elif 0 < row < 3:
                alien = Kani()
                alien.rect.x = x
                alien.rect.y = y
            else:
                if row == 3:
                    alien = Kumo()
                    alien.rect.x = x
                    alien.rect.y = y
                else:
                    alien = Tako()
                    alien.rect.x = x
                    alien.rect.y = y
