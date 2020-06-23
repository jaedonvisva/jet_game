import pygame
import random

from pygame.locals import *

import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAMEBAR_HEIGHT = 30
NUM_HEALTH = 100
GAME_OVER = False
# pygame.mixer.init()
pygame.init()
# pygame.mixer.music.load("background.mp3")
# pygame.mixer.music.play(loops = -1)


def draw_text(screen, text, size, x, y):
    font = pygame.font.Font("Bruzh.ttf", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        #self.surf = pygame.Surface((75, 25))
        # self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.top = SCREEN_HEIGHT / 2

    def update(self, pressed_keys):
        if GAME_OVER:
            return
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, +5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(+5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < GAMEBAR_HEIGHT:
            self.rect.top = GAMEBAR_HEIGHT
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        #self.surf = pygame.Surface((20, 10))
        #self.surf.fill((255,255, 0))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH,
                random.randint(GAMEBAR_HEIGHT, SCREEN_HEIGHT)
            )
        )
        self.speed_left_right = random.randint(5, 15)
        self.speed_up_down = random.randint(-7, 7)

    def update(self):
        if GAME_OVER:
            return
        self.rect.move_ip(-self.speed_left_right, self.speed_up_down)
        if self.rect.right < 0:
            self.kill()

        if self.rect.top < GAMEBAR_HEIGHT:
            self.kill()


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super(GameOver, self).__init__()
        self.surf = pygame.Surface((0, 0))
        self.rect = self.surf.get_rect()

    def update(self, screen):
        self.surf = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.surf.convert_alpha()

        draw_text(screen, "GAME OVER", 40, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


class HealthBack(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthBack, self).__init__()
        self.surf = pygame.Surface((100, 20))
        self.surf.fill((128, 128, 128))
        self.rect = self.surf.get_rect()
        self.rect.left = 5
        self.rect.top = 5


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthBar, self).__init__()
        self.surf = pygame.Surface((100, 20))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect()
        self.rect.left = 5
        self.rect.top = 5

    def update(self, num_health):
        self.surf = pygame.Surface((num_health, 20))
        self.surf.fill((0, 255, 0))


class GameBar(pygame.sprite.Sprite):
    def __init__(self):
        super(GameBar, self).__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH, GAMEBAR_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

running = True
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 150)

all_sprites = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()
# GameOver
gameOver = GameOver()
all_sprites.add(gameOver)
# GameBar
gameBar = GameBar()
all_sprites.add(gameBar)
# player
player = Player()
all_sprites.add(player)
# Health Bar
healthBack = HealthBack()
all_sprites.add(healthBack)

healthBar = HealthBar()
all_sprites.add(healthBar)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == ADDENEMY:
            if not GAME_OVER:
                new_enemy = Enemy()
                enemies_sprites.add(new_enemy)
                all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    if pygame.sprite.spritecollideany(player, enemies_sprites):
        NUM_HEALTH -= 5
        if NUM_HEALTH <= 0:
            # Game OVER
            GAME_OVER = True
            gameOver.update(screen)
            healthBar.update(0)
        else:
            healthBar.update(NUM_HEALTH)

    player.update(pressed_keys)
    enemies_sprites.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()


pygame.quit()
