import pygame
import random
from game.utils.constants import ENEMY_1, SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite): #Clase para crear sprites
    def __init__(self, x, y, width, height, image, speed, screen):
        #Llama al constructor de la clase padre
        super().__init__() 
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.screen = screen
        # Establece la dirección del sprite de manera aleatoria al inicio del juego
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

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
        self.screen.blit(self.image, self.rect)   # Dibuja el enemigo

