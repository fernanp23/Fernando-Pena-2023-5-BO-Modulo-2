import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT
from game.components.bullet import Bullet
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
        self.image_rect.x = 500
        self.image_rect.y = 500

    def move_right(self):
        #Mueve la nave a la derecha
        self.image_rect.x += 50
        #Si la nave sale de la pantalla por la derecha
        if self.image_rect.x > SCREEN_WIDTH:
            #Aparece en el lado izquierdo
            self.image_rect.x =- self.image_size[0]

    def move_left(self):
        #Mueve la nave a la izquierda
        self.image_rect.x -= 50
        #Si la nave sale por la izquierda
        if self.image_rect.right < 0:
            #Aparece en el lado derecho
            self.image_rect.x = SCREEN_WIDTH

    def move_up(self):
        #Mueve la nave hacia arriba
        self.image_rect.y -= 50
        #Si la nave sale por arriba
        if self.image_rect.top < 0:
            #Aparece en el lado de abajo
            self.image_rect.y = SCREEN_HEIGHT - self.image_rect.height

    def move_down(self):
        #Mueve la nave hacia abajo
        self.image_rect.y += 50
        #Si la nave sale por abajo
        if self.image_rect.bottom > SCREEN_HEIGHT:
            #Aparece en el lado de arriba
            self.image_rect.y = 0

    def shoot(self, bullets):
        bullet = Bullet(self.image_rect.centerx, self.image_rect.top) # Crea un nuevo objeto bala en la posición especificada
        bullets.add(bullet) # Agrega el objeto Bullet al grupo de balas

