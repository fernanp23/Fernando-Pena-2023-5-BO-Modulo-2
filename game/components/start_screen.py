import pygame
from game.utils.constants import START, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_STYLE

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.transform.scale(START, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(FONT_STYLE, 32)
        button_width = 100
        button_height = 50
        self.start_button = pygame.Rect(SCREEN_WIDTH / 2 - button_width / 2, SCREEN_HEIGHT - button_height, button_width, button_height)


    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), self.start_button)
        start_text = self.font.render("Start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    return True
        return False
