from globals import *
from entities import UFO, EnemyManager, Player, alien_setup, create_multiple_obstacles
from tools import Background, Text

import sys
import pygame as pg
import pygame_gui as pygui
from pygame.locals import *

pygame.init()
pygame.mixer.init()

pygame.mixer.set_num_channels(16)

FONT = pygame.font.SysFont(None, 24)

screen = pg.display.set_mode(WIN_SIZE)
clock = pg.time.Clock()

pg.display.set_caption('sp@c3 1vadé IV')


def main_menu():
    manager = pygui.UIManager(WIN_SIZE)

    play_button_rect = pg.Rect((0, 0), (275, 75))
    play_button_rect.center = (WIDTH // 2, HEIGHT // 2 - 95)
    play_button = pygui.elements.UIButton(relative_rect=play_button_rect, text='Play', manager=manager)

    options_button_rect = pg.Rect((0, 0), (275, 75))
    options_button_rect.center = (WIDTH // 2, HEIGHT // 2)
    options_button = pygui.elements.UIButton(relative_rect=options_button_rect, text='Options', manager=manager)

    quit_button_rect = pg.Rect((0, 0), (275, 75))
    quit_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 95)
    quit_button = pygui.elements.UIButton(relative_rect=quit_button_rect, text='Quit', manager=manager)

    main_title_rect = pg.Rect((0, 0), (WIDTH, 75))
    main_title = pygui.elements.UILabel(relative_rect=main_title_rect, text="SP@C3 1VADé", manager=manager)

    while True:
        screen.fill((0, 0, 0))
        time_delta = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    game()
                if event.ui_element == quit_button:
                    pg.quit()
                    sys.exit()

            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(screen)

        pg.display.update()


def game():
    manager = pygui.UIManager(WIN_SIZE)
    running = True

    background = Background()

    score = 0
    score_text = Text(f"Score: {score}", (255, 255, 255), 0, 0, FONT)
    score_text.rect.y = HEIGHT - score_text.rect.width // 2

    player = Player()
    player.rect.centerx = WIDTH // 2
    player.rect.y = HEIGHT - player.rect.height * 2

    ufo = UFO()
    ufo.direction = 1
    ufo.rect.x = 0
    ufo.rect.y = 16

    amount = 5
    offsets = [num * (WIDTH / amount) for num in range(amount)]
    create_multiple_obstacles(40, 450, amount, *offsets)

    alien_setup(rows=5, columns=11, y_offset=60)
    enemy_manager = EnemyManager()

    while running:
        screen.fill((0, 0, 0))
        time_delta = clock.tick(60) / 1000.0

        background.update()
        background.render(screen)

        for interface in USER_INTERFACE:
            interface.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    player.shoot()

            manager.process_events(event)

        for entity in ENTITIES:
            entity.update(time_delta)

        for bullet in BULLETS:
            if bullet.rect.centerx < 0 or bullet.rect.centerx > WIDTH or bullet.rect.centery < 0 or bullet.rect.centery > HEIGHT:
                # print("bullet destroyed")
                bullet.destroy()

            for other_bullet in BULLETS:
                if bullet != other_bullet:
                    if bullet.rect.colliderect(other_bullet.rect):
                        bullet.destroy()
                        other_bullet.destroy()

            for obstacle in OBSTACLES:
                if bullet.rect.colliderect(obstacle.rect):
                    # print("collided obstacle")
                    bullet.destroy()
                    obstacle.destroy()

            for enemy in ENEMIES:
                if type(bullet.parent) == Player:
                    if bullet.rect.colliderect(enemy.rect):
                        # print("collided enemy")
                        bullet.destroy()

                        enemy.health -= 1
                        if enemy.health <= 0:
                            score += type(enemy).score
                            enemy.killed = True
                        # enemy.destroy()

        manager.update(time_delta)
        manager.draw_ui(screen)

        enemy_manager.update(time_delta)

        score_text.text = f"Score: {score}"

        ENTITIES.draw(screen)
        EFFECTS.draw(screen)
        USER_INTERFACE.draw(screen)

        pg.display.update()

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()
