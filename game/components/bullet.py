import pygame
from pygame.sprite import Sprite
from game.utils.constants import SCREEN_HEIGHT

class Bullet(Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__() # Llama al método __init__ de la clase base Sprite
        self.image = pygame.transform.scale(image, (15, 30)) # Escala la imagen de la bala
        self.rect = self.image.get_rect() # Obtiene el rectángulo que encierra la imagen de la bala
        self.rect.bottom = y # Establece la posición y del borde inferior del rectángulo
        self.rect.centerx = x # Establece la posición x del centro del rectángulo
        self.speed = speed # Establece la velocidad

    def update(self):
        self.rect.y += self.speed # Actualiza la posición vertical de la bala de acuerdo a su velocidad
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT: # Si la bala sale fuera de los límites de la pantalla, se elimina del grupo de balas
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect) # Dibuja la imagen de la bala
