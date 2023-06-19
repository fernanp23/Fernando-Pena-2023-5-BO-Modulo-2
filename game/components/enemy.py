import pygame
from pygame.sprite import Sprite
import random
from game.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_ENEMY
from game.components.bullet import Bullet

class Enemy(Sprite):
    def __init__(self, x, y, width, height, image, speed, screen, game):
        super().__init__() # Llama al método __init__ de la clase base Sprite
        self.image = pygame.transform.scale(image, (width, height)) # Escala la imagen del enemigo
        self.rect = self.image.get_rect() # Obtiene el rectángulo que encierra la imagen del enemigo
        self.rect.x = x # Establece la posición x
        self.rect.y = y # Establece la posición y
        self.speed = speed # Establece la velocidad del enemigo
        self.screen = screen # Establece la pantalla donde se dibujará el enemigo
        self.direction = random.choice(['left', 'right', 'up', 'down']) # Establece la dirección del enemigo de manera aleatoria al inicio del juego

        self.game = game

    def update(self):
        if self.direction == 'left': # Si la dirección es izquierda
            self.rect.x -= self.speed # Mueve el rectángulo hacia la izquierda
        elif self.direction == 'right': # Si la dirección es derecha
            self.rect.x += self.speed # Mueve el rectángulo hacia la derecha
        elif self.direction == 'up': # Si la dirección es arriba
            self.rect.y -= self.speed # Mueve el rectángulo hacia arriba
        elif self.direction == 'down': # Si la dirección es abajo
            self.rect.y += self.speed # Mueve el rectángulo hacia abajo

        # Si el enemigo sale de la pantalla en cualquier dirección, aparece en una posición aleatoria en otra dirección aleatoria
        if self.rect.right < 0:   # Si el enemigo sale por la izquierda, aparece por la derecha en una posición aleatoria
            self.rect.left = SCREEN_WIDTH
            self.rect.top = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif self.rect.left > SCREEN_WIDTH:   # Si el enemigo sale por la derecha, aparece por la izquierda en una posición aleatoria
            self.rect.right = 0
            self.rect.top = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif self.rect.bottom < 0:   # Si el enemigo sale por arriba, aparece por abajo en una posición aleatoria
            self.rect.top = SCREEN_HEIGHT
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)
        elif self.rect.top > SCREEN_HEIGHT:   # Si el enemigo sale por abajo, aparece por arriba en una posición aleatoria
            self.rect.bottom = 0
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)

        # Genera un número aleatorio para determinar si el enemigo cambia de dirección
        if random.randint(0, 100) < 5:   # Si el número aleatorio es menor que 5, cambia la dirección del enemigo de manera aleatoria
            self.direction = random.choice(['left', 'right', 'up', 'down'])

    def draw(self):
        self.screen.blit(self.image, self.rect)   # Dibuja el enemigo en la pantalla en la posición del rectángulo

    def shoot(self, enemy_bullets):
        if random.randint(0, 500) < 5:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, BULLET_ENEMY, 5)
            enemy_bullets.add(bullet)
            return True
        return False
