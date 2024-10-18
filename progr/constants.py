"""
Les constantes nécessaires au fonctionnement du jeu
"""

# TECHNICAL

# sounds

PATH_SOUNDS = "../ress/sounds/"
PATH_MUSICS = "../ress/musics/"

SOUND_ENNEMI_HIT = PATH_SOUNDS+"explosion_short1.mp3"
SOUND_PLAYER_HIT = PATH_SOUNDS+"explosion_short1.mp3"
SOUND_SHOOT = PATH_SOUNDS+"lazer1.mp3"
SOUND_ROCKET_FIRE = PATH_SOUNDS+"rocket_fire.mp3"
SOUND_ROCKET_FLIGHT = PATH_SOUNDS+"rocket_flight1.mp3"
SOUND_EXPLOSION_DESTROY = PATH_SOUNDS+"explosion_long1.mp3"
SOUND_LASERBEAM_LOAD = PATH_SOUNDS+"lazerbeam_charge1.mp3"
SOUND_LASERBEAM_FIRE = PATH_SOUNDS+"lazerbeam.mp3"

SOUND_PLAYER_BASE_DESTROYED = PATH_SOUNDS+"explosion_long2.mp3"

MUSIC_WIN = PATH_SOUNDS+"win.mp3"
MUSIC_LOSE = PATH_SOUNDS+"defeat1.mp3"
MUSIC_MENU1 = PATH_MUSICS+"waiting_(theme1).mp3"
MUSIC_GAME2 = PATH_MUSICS+"defender_(theme2).mp3"
MUSIC_GAME_BOSS1 = PATH_MUSICS+"hard_pass_(theme1).mp3"

# screen mesures

SCREEN_WIDTH = 256+0 # bust be improved before
GAME_SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
GAME_SCREEN_HEIGHT = 256
GAME_SCREEN_WIDTH_START = SCREEN_WIDTH-GAME_SCREEN_WIDTH

# images

PATH_IMAGES = "../ress/img/"
LOGO_STUDIO = PATH_IMAGES+"logo_dicescreen_pyxel.pyxres"

# colors

COLOR_TITLE_SPACE = 7
COLOR_TITLE_DEFENDER = 10

# player pos

START_POSITION_X = GAME_SCREEN_WIDTH_START + GAME_SCREEN_WIDTH//2
START_POSITION_Y = 200

# LEVELS

SCORE_DESTROYER = 50 # bouclier
SCORE_DRONE_ALONE1, SCORE_ROCKET = 100, 100
SCORE_DRONE_SPEED1, SCORE_DOUBLE_TIR = 200, 200
SCORE_CRUISER = 300
SCORE_DRONE_ALONE2, SCORE_DOUBLE_ROCKET = 400, 400
SCORE_DRONE_SPEED2, SCORE_LAZERBEAM = 500, 500
# victoire niveau 1
SCORE_SPIDRONE = 800 # detecteur
SCORE_DESTROYER_FIRE_RATE, SCORE_TRIPLE_TIR = 1000, 1000
SCORE_DRONE_SPEED3, SCORE_BOOSTER = 1200, 1200
# victoire niveau 2
SCORE_FRIGAT, SCORE_LOCKER = 1400, 1400
SCORE_DRONE_SPEED4 = 1600
SCORE_CRUISER_FIRE_RATE = 1800

SCORE_VICTOIRE = 650 # multiplié par le niveau en cours
#SCORE_DREADNOUGHT = SCORE_VICTOIRE - 50 must be calculated for each level

# SYSTEM SETTINGS

BASE_LIFE = 30

PLAYER_LIFE = 6
PLAYER_SPEED = 2

DESTROYER_LIFE = 8
DESTROYER_FIRE_RATE = 20
DESTROYER_SPAWN_RATE = 20

CRUISER_HEALTH = 27
CRUISER_FIRE_RATE = 8
CRUISER_SPAWN_RATE = 15

SHIELD_POWER = 4
SHIELD_DURATION = 20
SHIELD_RELOAD = 40

DURATION_STIMS = 10

ROCKET_RELOAD = 5
BOOSTER_RELOAD = 30
LAZERBEAM_RELOAD = 50

MAX_DETECTOR_DURATION = 30

GAME_SPEED = 1 # never put under 0.5
