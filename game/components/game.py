import pygame
import random
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, ENEMY_1, ENEMY_2, FONT_STYLE, SHIELD, HEART
from game.components.spaceship import SpaceShip
from game.components.enemy import Enemy
from game.components.game_over import GameOver

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
        # Game loop: events - update - draw
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
                # Si se hizo clic con el mouse dentro del rectángulo del botón de "volver a jugar"
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
            self.game_over()
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
        self.draw_background()
        self.draw_spaceship()
        self.draw_enemies()
        self.draw_bullets()
        self.draw_enemy_bullets()
        self.draw_lives_counter()
        self.draw_shield_cooldown()
        self.draw_shield_message()
        self.draw_enemies_remaining()
        pygame.display.update()
        pygame.display.flip()

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
        lives_text = f'{self.lives}'
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

    def game_over(self):
        self.playing = False
        self.show_game_over_screen()
    
        # Reinicia el juego después de mostrar la pantalla de "game over"
        self.__init__()
        self.run()

    def show_game_over_screen(self):
        # Mostramos los contadores de balas del jugador y del enemigo en la pantalla de "game over"
        game_over_screen = GameOver(self.screen, self.player_bullet_count, self.enemy_bullet_count)
        game_over_screen.draw()

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


    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed


