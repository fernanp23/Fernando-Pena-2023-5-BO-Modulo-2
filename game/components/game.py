import pygame
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, ENEMY_1, ENEMY_2, GAME_OVER, FONT_STYLE
from game.components.spaceship import SpaceShip
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
        self.spaceship = SpaceShip() # Game tiene un "Spaceship"
        self.enemies = pygame.sprite.Group() # Modificaciones para crear un grupo de enemigos
        for enemy in range(5): # Crea un grupo de 5 enemigos del tipo 1 y los añade al grupo de enemigos
            enemy = Enemy(0, 0, 40, 60, ENEMY_1, 5, self.screen, self)
            self.enemies.add(enemy)
        for enemy in range(5): # Crea un grupo de 5 enemigos del tipo 2 y los añade al grupo de enemigos
            enemy = Enemy(0, 0, 40, 60, ENEMY_2, 5, self.screen, self)
            self.enemies.add(enemy)
        # Crea grupos de balas del jugador y del enemigo y establece contadores de colisiones, muertes y vidas
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.bullet_count = 0
        self.death_count = 0
        self.collision_count = 0
        self.lives = 5
        self.font = pygame.font.Font(FONT_STYLE, 25)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.spaceship.move_right()
                elif event.key == pygame.K_LEFT:
                    self.spaceship.move_left()
                elif event.key == pygame.K_UP:
                    self.spaceship.move_up()
                elif event.key == pygame.K_DOWN:
                    self.spaceship.move_down()
                elif event.key == pygame.K_SPACE:
                    self.spaceship.shoot(self.bullets)


    def update(self):
        self.spaceship.update() # Actualiza la posición de la nave en cada iteración del bucle principal del juego
        self.enemies.update() # Actualiza la posición de los enemigos en cada iteración del bucle principal del juego
        for bullet in self.bullets:
            enemy_hit = pygame.sprite.spritecollideany(bullet, self.enemies) # Verifica si hay una colisión entre la bala y cualquier enemigo
            if enemy_hit: # Si hay una colisión
                bullet.kill() # Elimina la bala
                enemy_hit.kill() # Elimina el enemigo golpeado
        self.bullets.update() # Actualiza la posición de las balas en cada iteración del bucle principal del juego

        # Comprueba si la nave del jugador colisiona con alguna bala del enemigo
        if pygame.sprite.spritecollideany(self.spaceship, self.enemy_bullets):  # Si colisiona, incrementa el contador de balas recibidas
            self.bullet_count += 1

        # Si el contador de balas recibidas supera las 5, muestra la pantalla de Game Over
        if self.bullet_count > 5:
            self.game_over()
            self.death_count += 1
        
        # Comprueba si la nave del jugador colisiona con alguna bala del enemigo
        collision = pygame.sprite.spritecollideany(self.spaceship, self.enemy_bullets)
        if collision: # Si colisiona, elimina la bala, bajan las vidas del jugador y muestra la pantalla de Game Over si se quedó sin vidas
            collision.kill()
            self.collision_count += 1
            if self.collision_count >= 5:
                self.game_over()
            self.lives -= 1
        
        self.enemy_bullets.update() # Actualiza la posición de las balas del enemigo

        if not self.enemies: # Si no quedan enemigos, muestra la pantalla de Game Over
            self.game_over()
        
        # Comprueba si la nave del jugador colisiona con alguna bala del enemigo y si el jugador no tiene vidas restantes, muestra la pantalla de Game Over
        if pygame.sprite.spritecollideany(self.spaceship, self.enemy_bullets):
            if self.lives <= 0:
                self.game_over()




    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()


        # dibujamos el objeto en pantalla
        self.screen.blit(self.spaceship.image, self.spaceship.image_rect)

        # dibuja a los enemigos
        for enemy in self.enemies:
            enemy.draw()
        # dibuja las balas
        for bullet in self.bullets:
            bullet.draw(self.screen)

        self.enemy_bullets.draw(self.screen)

        lives_text = f'Lives: {self.lives}' # Crea un string Lives
        lives_surface = self.font.render(lives_text, True, (255, 255, 255)) # Renderiza el texto con color blanco
        lives_rect = lives_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10)) # Dibujar en el lado superior de la derecha
        self.screen.blit(lives_surface, lives_rect)

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

    def game_over(self):
        image = pygame.transform.scale(GAME_OVER, (400, 40)) # Escala la imagen
        image_rect = image.get_rect() # Obtiene el rectángulo de la imagen y la centra
        image_rect.centerx = SCREEN_WIDTH / 2
        image_rect.centery = SCREEN_HEIGHT / 2
        self.screen.blit(image, image_rect) # Dibuja la imagen
        pygame.display.update() # Actualiza la pantalla
        pygame.time.wait(5000) # Tiempo de espera
        self.playing = False # Finaliza el ciclo

