import pygame
import os

# Global Constants
TITLE = "Spaceships Game"
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
FPS = 30
IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
SOUND_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")


# Assets Constants
ICON = pygame.image.load(os.path.join(IMG_DIR, "Spaceship/spaceship.png"))

SHIELD = pygame.image.load(os.path.join(IMG_DIR, 'Other/shield.png'))

BG = pygame.image.load(os.path.join(IMG_DIR, 'Other/Track.png'))

HEART = pygame.image.load(os.path.join(IMG_DIR, 'Other/Heart.png'))

DEFAULT_TYPE = "default"
SHIELD_TYPE = 'shield'

SPACESHIP = pygame.image.load(os.path.join(IMG_DIR, "Spaceship/spaceship.png"))
SPACESHIP_SHIELD = pygame.image.load(os.path.join(IMG_DIR, "Spaceship/spaceship_shield.png"))
BULLET = pygame.image.load(os.path.join(IMG_DIR, "Bullet/bullet_1.png"))

BULLET_ENEMY = pygame.image.load(os.path.join(IMG_DIR, "Bullet/bullet_2.png"))
ENEMY_1 = pygame.image.load(os.path.join(IMG_DIR, "Enemy/enemy_1.png"))
ENEMY_2 = pygame.image.load(os.path.join(IMG_DIR, "Enemy/enemy_2.png"))
START = pygame.image.load(os.path.join(IMG_DIR, "Other/Start.png"))
GAME_OVER = pygame.image.load(os.path.join(IMG_DIR, "Other/GameOverNew.png"))
VICTORY_SCREEN = pygame.image.load(os.path.join(IMG_DIR, "Other/VictoryScreen.png"))
RESET = pygame.image.load(os.path.join(IMG_DIR, "Other/Reset.png"))

START_SOUND = os.path.join(SOUND_DIR, "StartSound.wav")
SHOOT_SOUND = os.path.join(SOUND_DIR, "ShootSound.wav")
GAME_SOUND = os.path.join(SOUND_DIR, "GameSound.wav")
GAME_OVER_SOUND = os.path.join(SOUND_DIR, "GameOverSound.wav")
VICTORY_SOUND = os.path.join(SOUND_DIR, "VictorySound.wav")

FONT_STYLE = 'freesansbold.ttf'
