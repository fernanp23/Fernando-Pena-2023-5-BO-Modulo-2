import pygame
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, ENEMY_1, ENEMY_2, FONT_STYLE, SHIELD, HEART

class GameRenderer:
    def __init__(self, game, screen, font, spaceship, enemies, bullets, enemy_bullets, game_speed):
        self.game = game
        self.screen = screen
        self.font = font
        self.spaceship = spaceship
        self.enemies = enemies
        self.bullets = bullets
        self.enemy_bullets = enemy_bullets
        self.game_speed = game_speed

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.game.x_pos_bg, self.game.y_pos_bg))
        self.screen.blit(image, (self.game.x_pos_bg, self.game.y_pos_bg - image_height))
        if self.game.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.game.x_pos_bg, self.game.y_pos_bg - image_height))
            self.game.y_pos_bg = 0
        self.game.y_pos_bg += self.game.game_speed


    def draw_spaceship(self):
        self.screen.blit(self.spaceship.image, self.spaceship.image_rect)
        if self.spaceship.shield_active:
            self.screen.blit(self.spaceship.shield_image, self.spaceship.shield_image_rect)

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw()

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw(self.screen)

    def draw_enemy_bullets(self):
        self.enemy_bullets.draw(self.screen)

    def draw_lives_counter(self):
        lives_text = f'{self.game.lives}'
        lives_surface = self.font.render(lives_text, True, (255, 255, 255))
        lives_rect = lives_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(lives_surface, lives_rect)
        # Dibuja la imagen del corazón
        heart_image = HEART
        heart_image_rect = heart_image.get_rect(topright=(SCREEN_WIDTH - 10 - 50, 10))
        self.screen.blit(heart_image, heart_image_rect)

    def draw_enemies_remaining(self):
        enemies_text = f'Enemies remaining: {len(self.enemies)}'
        enemies_surface = self.font.render(enemies_text, True, (255, 255, 255))
        enemies_rect = enemies_surface.get_rect(topleft=(10, 10))
        self.screen.blit(enemies_surface, enemies_rect)

    def draw_shield_cooldown(self):
        if self.spaceship.shield_cooldown > 0:
            cooldown_text = f'Shield Cooldown: {int(self.spaceship.shield_cooldown / FPS)}'
            cooldown_surface = self.font.render(cooldown_text, True, (255, 255, 255))
            cooldown_rect = cooldown_surface.get_rect(topright=(SCREEN_WIDTH - 10, 40))
            self.screen.blit(cooldown_surface, cooldown_rect)

    def draw_shield_message(self):
        if self.spaceship.shield_cooldown <= 0:
            # Dibuja el texto
            shield_text = "S"
            shield_surface = self.font.render(shield_text, True, (255, 255, 255))
            shield_rect = shield_surface.get_rect(bottomleft=(10 + 50, SCREEN_HEIGHT - 10))
            self.screen.blit(shield_surface, shield_rect)
            
            # Dibuja la imagen del escudo
            shield_image = SHIELD
            shield_image_rect = shield_image.get_rect(bottomleft=(10, SCREEN_HEIGHT - 10))
            self.screen.blit(shield_image, shield_image_rect)