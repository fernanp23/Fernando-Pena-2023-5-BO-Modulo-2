import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET, SPACESHIP_SHIELD, FPS, SHOOT_SOUND
from game.components.bullet import Bullet

class SpaceShip(Sprite):
    
    def __init__(self):
        self.image_size = (40, 60)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = 500
        self.image_rect.y = 500
        self.rect = self.image_rect
        self.shield_active = False
        self.shield_cooldown = 0
        self.shield_duration = 10 *FPS
        self.shield_image = pygame.transform.scale(SPACESHIP_SHIELD, (40, 60))
        self.shield_image_rect = self.shield_image.get_rect()
        self.shoot_sound = pygame.mixer.Sound(SHOOT_SOUND)

    def move_right(self): # Mueve la nave a la derecha
        self.image_rect.x += 50
        if self.image_rect.x > SCREEN_WIDTH: # Si la nave sale de la pantalla por la derecha
            self.image_rect.x =- self.image_size[0] # Aparece en el lado izquierdo

    def move_left(self): # Mueve la nave a la izquierda
        self.image_rect.x -= 50
        if self.image_rect.right < 0: # Si la nave sale por la izquierda
            self.image_rect.x = SCREEN_WIDTH # Aparece en el lado derecho

    def move_up(self):
        self.image_rect.y -= 50
        if self.image_rect.top < 0:
            self.image_rect.top = 0


    def move_down(self):
        self.image_rect.y += 50
        if self.image_rect.bottom > SCREEN_HEIGHT:
            self.image_rect.bottom = SCREEN_HEIGHT


    def update(self):
        self.rect.x = self.image_rect.x
        self.rect.y = self.image_rect.y
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1
        if self.shield_cooldown == 0 and self.shield_active:
            self.shield_active = False
            self.shield_cooldown = self.shield_duration
        self.shield_image_rect.x = self.image_rect.x
        self.shield_image_rect.y = self.image_rect.y
        
    def shoot(self, bullets):
        bullet = Bullet(self.image_rect.centerx, self.image_rect.top, BULLET, -10) # Crea un objeto de la clase Bullet en la posición del centro inferior del spaceship
        bullets.add(bullet) # Agrega el objeto Bullet al grupo de balas
        self.shoot_sound.play()

    def activate_shield(self):
        if self.shield_cooldown <= 0:
            self.shield_active = True
            self.shield_cooldown = self.shield_duration

