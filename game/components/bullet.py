import pygame
from pygame.sprite import Sprite
from game.utils.constants import BULLET

class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__() # Llama al método __init__ de la clase base Sprite
        self.image = pygame.transform.scale(BULLET, (20, 40)) # Escala la imagen de la bala
        self.rect = self.image.get_rect() # Obtiene el rectángulo que encierra la imagen de la bala
        self.rect.bottom = y # Establece la posición y del borde inferior del rectángulo
        self.rect.centerx = x # Establece la posición x del centro del rectángulo
        self.speed = -20 # Establece la velocidad de la bala

    def update(self):
        self.rect.y += self.speed # Actualiza la posición y del rectángulo
        if self.rect.bottom < 0: # Si sale del borde de la pantalla
            self.kill() # Elimina la bala

    def draw(self, screen):
        screen.blit(self.image, self.rect) # Dibuja la imagen de la bala
