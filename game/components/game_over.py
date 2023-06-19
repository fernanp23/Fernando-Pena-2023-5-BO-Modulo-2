import pygame
from game.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, GAME_OVER, FONT_STYLE, RESET, GAME_OVER_SOUND

pygame.mixer.init()
pygame.init()

class GameOver:
    def __init__(self, screen, player_bullet_count, enemy_bullet_count, enemies_killed):
        self.screen = screen
        self.image = pygame.transform.scale(GAME_OVER, (300, 200))
        self.image_rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.font = pygame.font.Font(FONT_STYLE, 25)
        self.player_bullet_count = player_bullet_count
        self.enemy_bullet_count = enemy_bullet_count
        self.enemies_killed = enemies_killed
        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)
        self.game_over_sound.play()     

    def draw(self):
        self.screen.blit(self.image, self.image_rect)

        player_bullet_text = f'Player bullets: {self.player_bullet_count}'
        player_bullet_surface = self.font.render(player_bullet_text, True, (255, 255, 255))
        player_bullet_rect = player_bullet_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150))
        self.screen.blit(player_bullet_surface, player_bullet_rect)
        
        enemy_bullet_text = f'Enemy bullets: {self.enemy_bullet_count}'
        enemy_bullet_surface = self.font.render(enemy_bullet_text, True, (255, 255, 255))
        enemy_bullet_rect = enemy_bullet_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200))
        self.screen.blit(enemy_bullet_surface, enemy_bullet_rect)

        enemies_killed_text = f'Score: {self.enemies_killed}'
        enemies_killed_surface = self.font.render(enemies_killed_text, True, (255, 255, 255))
        enemies_killed_rect = enemies_killed_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 250))
        self.screen.blit(enemies_killed_surface, enemies_killed_rect)

        play_again_image = RESET
        self.play_again_rect = play_again_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 175))
        self.screen.blit(play_again_image, self.play_again_rect)
        
        pygame.display.update()
        # Espera a que el jugador presione el botón de "volver a jugar"
        while True:
            if self.handle_events():
                break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_rect.collidepoint(event.pos):
                    self.game_over_sound.stop()
                    return True
        return False