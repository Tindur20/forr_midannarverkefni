import pygame as pg
vec = pg.math.Vector2

# litir til ad nota (R, G, B)
# því pygame er ekki með neina liti defined
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# settings fyrir leikinn ef ég myndi nota map sem er í texta formi ekki sem er gert
# í mað editor
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED=200
PLAYER_HEALTH = 200
CAR_BODY = 'car_black_small_3.png'
CAR_HIT_RECT = pg.Rect(0, 0, 60, 34)
SMOKE_OFFSET = vec(-32,-12)
CAR_DAMAGE = 60

# Car extra's
SMOKE_IMG = 'smoke.png'
SMOKE_SPEED = 10
SMOKE_LIFETIME = 100
SMOKE_RATE = 30
SMOKE_SPREAD = 10000



# mobs / enemies settings
MOB_IMG  = 'Zombie_model.png'
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_SPEED = 200
AVOIDE_RADIUS = 75
MOB_HEALTH = 150
MOB_KNOCKBACK = 20
MOB_DAMAGE = 10
