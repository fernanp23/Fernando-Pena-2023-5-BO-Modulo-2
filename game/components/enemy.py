import pygame
from pygame.sprite import Sprite
import random
from game.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_ENEMY
from game.components.bullet import Bullet

class Enemy(Sprite):
    def __init__(self, x, y, width, height, image, speed, screen, game):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.screen = screen
        self.direction = random.choice(['left', 'right', 'up', 'down'])

        self.game = game

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.top = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
            self.rect.top = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)

        if random.randint(0, 100) < 5:
            self.direction = random.choice(['left', 'right', 'up', 'down'])

    def draw(self):
        self.screen.blit(self.image, self.rect)
        
    def shoot(self, enemy_bullets):
        if random.randint(0, 500) < 5:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, BULLET_ENEMY, 5)
            enemy_bullets.add(bullet)
            return True
        return False
