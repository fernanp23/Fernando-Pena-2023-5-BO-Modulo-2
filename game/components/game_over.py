import pygame
from game.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, GAME_OVER, FONT_STYLE

class GameOver:
    def __init__(self, screen, player_bullet_count, enemy_bullet_count):
        self.screen = screen
        self.font = pygame.font.Font(FONT_STYLE, 25)
        self.image = pygame.transform.scale(GAME_OVER, (400, 40))
        self.image_rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        
        # Agregamos los contadores de balas del jugador y del enemigo como atributos
        self.player_bullet_count = player_bullet_count
        self.enemy_bullet_count = enemy_bullet_count

# En la clase GameOver
    def draw(self):
        self.screen.blit(self.image, self.image_rect)
        
        # Mostramos los contadores de balas del jugador y del enemigo en la pantalla
        player_bullet_text = f'Player bullets: {self.player_bullet_count}'
        player_bullet_surface = self.font.render(player_bullet_text, True, (255, 255, 255))
        player_bullet_rect = player_bullet_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        self.screen.blit(player_bullet_surface, player_bullet_rect)
        
        enemy_bullet_text = f'Enemy bullets: {self.enemy_bullet_count}'
        enemy_bullet_surface = self.font.render(enemy_bullet_text, True, (255, 255, 255))
        enemy_bullet_rect = enemy_bullet_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))
        self.screen.blit(enemy_bullet_surface, enemy_bullet_rect)
        
        # Dibuja el botón de "volver a jugar"
        self.play_again_rect = pygame.draw.rect(self.screen, (0, 255, 0), (SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 + 150, 100, 50))
        play_again_text = self.font.render('Restart', True, (0, 0, 0))
        play_again_text_rect = play_again_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 175))
        self.screen.blit(play_again_text, play_again_text_rect)
        
        pygame.display.update()
        
        # Espera a que el jugador presione el botón de "volver a jugar"
        while True:
            if self.handle_events():
                break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si se hizo clic con el mouse dentro del rectángulo del botón de "volver a jugar"
                if self.play_again_rect.collidepoint(event.pos):
                    return True
        return False

