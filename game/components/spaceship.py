import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP
#Nuevo import para mover la nave de forma horizontal
from game.utils.constants import SCREEN_WIDTH

# casi Todo en pygame es un objeto
# Un personaje en mi juego es un objeto (instancia de algo)
# La nave (spaceship) es un personaje => necesito una clase


# SpaceShip es una clase derivada (hija) de Sprite

# spaceship tiene una "imagen"
class SpaceShip(Sprite):
    
    def __init__(self):
        self.image_size = (40, 60)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = self.image_size[0]
        self.image_rect.y = self.image_size[1]

    def update(self):
        pass

    def move_right(self):
        #Mueve la nave a la derecha
        self.image_rect.x += 50
        #Si la nave sale de la pantalla por la derecha
        if self.image_rect.x > SCREEN_WIDTH:
            #Aparece en el lado izquierdo
            self.image_rect.x = -self.image_size[0]

    def move_left(self):
        #Mueve la nave a la izquierda
        self.image_rect.x -= 50
        #Si la nave sale por la izquierda
        if self.image_rect.right < 0:
            #Aparece en el lado derecho
            self.image_rect.x = SCREEN_WIDTH
