import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, ENEMY_1

from game.components.spaceship import SpaceShip

#Import enemy
from game.components.enemy import Enemy

# Game tiene un "Spaceship" - Por lo general esto es iniciliazar un objeto Spaceship en el __init__
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False  # variable de control para salir del ciclo
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0

        # Game tiene un "Spaceship"
        self.spaceship = SpaceShip()
        # Instancia objeto enemy
        self.enemy = Enemy(0, 0, 40, 60, ENEMY_1, 10, self.screen)



    def run(self):
        # Game loop: events - update - draw
        self.playing = True

        # while self.playing == True
        while self.playing: # Mientras el atributo playing (self.playing) sea true "repito"
            self.handle_events()
            self.update()
            self.draw()
        else:
            print("Something ocurred to quit the game!!!")
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        # Para un "event" (es un elemento) en la lista (secuencia) que me retorna el metodo get()
        for event in pygame.event.get():
            # si el "event" type es igual a pygame.QUIT entonces cambiamos playing a False
            if event.type == pygame.QUIT:
                self.playing = False
            #Si el tipo de evento es KEYDOWN (una tecla fue presionada)
            elif event.type == pygame.KEYDOWN:
                # Si la tecla presionada es la flecha derecha
                if event.key == pygame.K_RIGHT:
                    # Llamada al método move_right() del objeto spaceship
                    self.spaceship.move_right()
                # Si la tecla presionada es la flecha izquierda
                elif event.key == pygame.K_LEFT:
                    # Llamada al método move_left() del objeto spaceship
                    self.spaceship.move_left()
                #Nuevo, si las teclas de arriba y abajo son presionadas    
                elif event.key == pygame.K_UP:
                    self.spaceship.move_up()
                elif event.key == pygame.K_DOWN:
                    self.spaceship.move_down()

    def update(self):
        # pass
        self.spaceship.update()
        # Actualiza la posición del enemigo en cada iteración del bucle principal del juego
        self.enemy.update()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()


        # dibujamos el objeto en pantalla
        self.screen.blit(self.spaceship.image, self.spaceship.image_rect)

        #dibuja el enemigo
        self.enemy.draw()

        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed
