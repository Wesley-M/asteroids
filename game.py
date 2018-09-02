import pygame
import os
import menu
from pygame import mouse
from pygame.locals import *
from util import *
from settings import *

# Setting the working directory
os.chdir("/home/wesley/asteroid")

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image("imgs/nave.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = DISPLAY_WIDTH / 2
        self.rect.bottom = DISPLAY_HEIGHT - 10
        self.speed_x = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3

    def update(self):
        self.speed_x = 0
        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_LEFT]:
            self.speed_x = -10
        if key_state[pygame.K_RIGHT]:
            self.speed_x = 10
        if key_state[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speed_x

        if self.rect.right > DISPLAY_WIDTH:
            self.rect.right = DISPLAY_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            b = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            shoot_sound.play()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image("imgs/asteroide.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = DISPLAY_WIDTH / 2
        self.rect.bottom = DISPLAY_HEIGHT - 10
        self.speedy = 50

    def update(self):
        self.speedy = 0
        self.rect.y += self.speedy
        if rect.rect.top > DISPLAY_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("imgs/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Game:
    def __init__(self):
        pg.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()

        self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.nave = Nave()

    def run(self):

        # Game loop
        pygame.mixer.music.load("audio/star_commander.wav")
        self.selecting = True
        while self.selecting:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.selecting:
                    self.selecting = False
                self.running = False

    def draw(self):

        self.screen.fill(LIGHT_BLUE)
        self.screen.blit(get_image("imgs/bg_game_start.jpg"), (0, 0))
        self.all_sprites.draw(self.screen)

        pg.display.flip()


g = Game()

while g.running:
    g.run()

pg.quit()
