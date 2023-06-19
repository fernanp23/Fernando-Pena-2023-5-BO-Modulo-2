import pygame
import random
from game.utils.constants import ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, ENEMY_1, ENEMY_2, FONT_STYLE, GAME_SOUND
from game.components.spaceship import SpaceShip
from game.components.enemy import Enemy
from game.components.game_over import GameOver
from game.components.game_renderer import GameRenderer
from game.components.start_screen import StartScreen
from game.components.victory_screen import VictoryScreen

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
        self.spaceship = SpaceShip()
        self.enemies = pygame.sprite.Group()
        self.create_enemies()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.bullet_count = 0
        self.death_count = 0
        self.collision_count = 0
        self.lives = 5
        self.font = pygame.font.Font(FONT_STYLE, 25)
        self.player_bullet_count = 0
        self.enemy_bullet_count = 0
        self.enemy_spawn_time = 5 * FPS  # Aparece un nuevo enemigo cada 5 segundos
        self.enemy_spawn_cooldown = 0
        self.start_screen = StartScreen(self.screen)
        # Instancia de GameRenderer para manejar el dibujo en pantalla
        self.renderer = GameRenderer(self, self.screen, self.font, self.spaceship, self.enemies, self.bullets, self.enemy_bullets, self.game_speed)
        self.game_sound = pygame.mixer.Sound(GAME_SOUND)

    def create_enemies(self):
        # Crea grupos de enemigos y los añade al grupo de enemigos
        self.create_enemy_group(5, ENEMY_1)
        self.create_enemy_group(5, ENEMY_2)

    def create_enemy_group(self, num_enemies, enemy_type):
        # Crea un grupo de enemigos y los añade al grupo de enemigos
        for i in range(num_enemies):
            enemy = Enemy(0, 0, 40, 60, enemy_type, 5, self.screen, self)
            self.enemies.add(enemy)

    def run(self):
        # Muestra la pantalla de inicio hasta que el usuario haga clic en el botón de inicio
        while not self.start_screen.handle_events():
            self.start_screen.draw()
        self.game_sound.play(loops=-1)

        # Inicia el bucle principal del juego
        self.playing = True
        while self.playing:
            self.handle_events()
            self.update()
            self.draw()
        else:
            print("Something ocurred to quit the game!!!")
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
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
                elif event.key == pygame.K_s:
                    self.spaceship.activate_shield()
                elif event.key == pygame.K_SPACE:
                    # Incrementamos el contador de balas del jugador cada vez que dispara una bala
                    self.player_bullet_count += 1
                    self.spaceship.shoot(self.bullets)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                # Si se hizo clic con el mouse dentro del rectángulo del botón de "Restart"
                    if self.play_again_rect.collidepoint(event.pos):
                        return True
                return False

    def update(self):
        self.update_spaceship()
        self.update_enemies()
        self.update_bullets()
        self.check_enemy_bullet_collisions()
        self.check_collisions()
        self.update_enemy_bullets()
        self.check_game_over()
        self.spawn_enemies()

    def update_spaceship(self):
        self.spaceship.update()

    def update_enemies(self):
        # Incrementamos el contador de balas del enemigo cada vez que un enemigo dispara una bala
        for enemy in self.enemies:
            if enemy.shoot(self.enemy_bullets):
                self.enemy_bullet_count += 1
        self.enemies.update()

    def update_bullets(self):
        for bullet in self.bullets:
            enemy_hit = pygame.sprite.spritecollideany(bullet, self.enemies)
            if enemy_hit:
                bullet.kill()
                enemy_hit.kill()
        self.bullets.update()

    def check_enemy_bullet_collisions(self):
        if pygame.sprite.spritecollideany(self.spaceship, self.enemy_bullets) and not self.spaceship.shield_active:
            self.bullet_count += 1

    def check_collisions(self):
        collision = pygame.sprite.spritecollideany(self.spaceship, self.enemy_bullets)
        if collision:
            if not self.spaceship.shield_active:
                collision.kill()
                self.collision_count += 1
                if self.collision_count >= 5:
                    self.game_over()
                self.lives -= 1

    def update_enemy_bullets(self):
        self.enemy_bullets.update()

    def check_game_over(self):
        if not self.enemies:
            self.game_sound.stop()
            self.show_victory_screen()
            self.__init__()
            self.run()
        if self.bullet_count > 5 and not self.spaceship.shield_active:
                self.game_over()
                self.death_count += 1

    def spawn_enemies(self):
        if self.enemy_spawn_cooldown <= 0:
            # Crea un nuevo enemigo de un tipo aleatorio y lo agrega al grupo de enemigos
            enemy_type = random.choice([ENEMY_1, ENEMY_2])
            enemy = Enemy(0, 0, 40, 60, enemy_type, 5, self.screen, self)
            self.enemies.add(enemy)
            # Reinicia el tiempo de enfriamiento para la próxima aparición de un enemigo
            self.enemy_spawn_cooldown = self.enemy_spawn_time
        else:
            # Reduce el tiempo de enfriamiento hasta la próxima aparición de un enemigo
            self.enemy_spawn_cooldown -= 1

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.renderer.draw_background()
        self.renderer.draw_spaceship()
        self.renderer.draw_enemies()
        self.renderer.draw_bullets()
        self.renderer.draw_enemy_bullets()
        self.renderer.draw_lives_counter()
        self.renderer.draw_shield_cooldown()
        self.renderer.draw_shield_message()
        self.renderer.draw_enemies_remaining()
        pygame.display.update()
        pygame.display.flip()

    def game_over(self):
        self.playing = False
        self.game_sound.stop()
        self.show_game_over_screen()
        self.__init__()
        self.run()

    def show_game_over_screen(self):
        # Mostramos los contadores de balas del jugador y del enemigo en la pantalla de "game over"
        game_over_screen = GameOver(self.screen, self.player_bullet_count, self.enemy_bullet_count)
        game_over_screen.draw()

    def show_victory_screen(self):
        self.victory_screen = VictoryScreen(self.screen, self.player_bullet_count, self.enemy_bullet_count)
        self.victory_screen.victory_sound.play(loops=0)
        # Muestra la pantalla de victoria hasta que el usuario haga clic en la pantalla
        while not self.victory_screen.handle_events():
            self.victory_screen.draw()