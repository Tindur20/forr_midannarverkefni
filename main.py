import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col= RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 3)

#def draw_barrel


# hér er basic breytur fyrir glugan sem opnast þegar leikurinn er spilaður og
# breyta til að loada gögnum
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    # hér er loadað gögn t.d. map og objects
    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'myndir')
        map_folder = path.join(map_folder, 'map')
        self.map = TiledMap(path.join(map_folder, 'map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.car_body = pg.image.load(path.join(img_folder, CAR_BODY)).convert_alpha()
        self.smoke_img = pg.image.load(path.join(img_folder, SMOKE_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()

    # frumstilla allar breytur og gera allt skipulag fyrir nýjan leik
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.car = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.smoke = pg.sprite.Group()
        self.barrel = pg.sprite.Group()
        # Þetta er fyrir tiledmap ekki map sem er gert í tiled editor
        #for row, tiles in enumerate(self.map.data):
        #    for col, tile in enumerate(tiles):
        #         if tile == '1':
        #            Wall(self, col, row)
        #         if tile == 'M':
        #            Mob(self, col, row)
        #         if tile == 'P':
        #            self.player = Player(self, col, row)

        # hér er spawnað inn objects t.d. player, veggi og fleyra
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player =Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

# Þetta keyrir leikinn / game loop
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

# þetta er fyrir að stopa leikinn
    def quit(self):
        pg.quit()
        sys.exit()

    # uppfæra / update  hluti af game loop
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        # enemies hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        # hér er þegar playerinn er damage af enemies þá mun hann knockast smá til bakka
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # player hits enemies
        hits = pg.sprite.groupcollide(self.mobs, self.car, False, False)
        for hit in hits:
            hit.health -= CAR_DAMAGE
            hit.vel = vec(0,0)
    # teiknar grid system þegar playerinn var bara kassi og hann var bara að hreyfa sig einn kassa í einu
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        #Þetta fyrir neðan loadar tiled mapið ekki texta skjal mapið
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)

        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    # ef þú vilt hæta í leiknum geturu ýtt á escape og þá slekur leikurinn á sér
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
