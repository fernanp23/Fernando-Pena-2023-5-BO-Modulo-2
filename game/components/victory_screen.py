import pygame
from game.utils.constants import VICTORY_SCREEN, VICTORY_SOUND, SCREEN_WIDTH, SCREEN_HEIGHT, RESET, FONT_STYLE

pygame.mixer.init()
pygame.init()

class VictoryScreen:
    def __init__(self, screen, player_bullet_count, enemy_bullet_count):
        self.screen = screen
        self.image = pygame.transform.scale(VICTORY_SCREEN, (300, 200))
        self.image_rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.back_button = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 150, 100, 50)
        self.back_button_image = RESET
        self.back_button_image_rect = self.back_button_image.get_rect(center=self.back_button.center)
        self.player_bullet_count = player_bullet_count
        self.enemy_bullet_count = enemy_bullet_count
        self.font = pygame.font.Font(FONT_STYLE, 32)
        self.victory_sound = pygame.mixer.Sound(VICTORY_SOUND)

    def draw(self):
        self.screen.blit(self.image, self.image_rect)

        self.screen.blit(self.back_button_image, self.back_button_image_rect)
        player_bullet_text = f'Player bullets: {self.player_bullet_count}'
        player_bullet_surface = self.font.render(player_bullet_text, True, (255, 255, 255))
        player_bullet_rect = player_bullet_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200))
        self.screen.blit(player_bullet_surface, player_bullet_rect)

        enemy_bullet_text = f'Enemy bullets: {self.enemy_bullet_count}'
        enemy_bullet_surface = self.font.render(enemy_bullet_text, True, (255, 255, 255))
        enemy_bullet_rect = enemy_bullet_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 250))
        self.screen.blit(enemy_bullet_surface, enemy_bullet_rect)
        
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.victory_sound.stop()
                    return True
        return False