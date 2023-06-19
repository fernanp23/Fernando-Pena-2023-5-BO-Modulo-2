import pygame
from pygame.sprite import Sprite
from game.utils.constants import SCREEN_HEIGHT

class Bullet(Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        self.image = pygame.transform.scale(image, (15, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
