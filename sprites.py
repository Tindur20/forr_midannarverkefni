import pygame as pg
from random import uniform
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

# collider fyrir veggi
def collide_with_walls(sprite, group, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y

# class fyrir playerinn
class Player(pg.sprite.Sprite):
    #
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.car
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.car_body
        self.rect = self.image.get_rect()
        self.hit_rect = CAR_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        #þetta þarf ef það myndi vera nota map sem er í texta skjalli
        #self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.health = PLAYER_HEALTH
        self.last_smoke = 0
        self.last_barrel = 0

    # nær í lyklana annað hvort a w s d eða örva takana til að láta playerinn hreyfa sig
    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        mx,my = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            #  þetta er fyrir reykinn sem kemur úr bílnum þegar hann er að keyra
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            now = pg.time.get_ticks()
            if now - self.last_smoke > SMOKE_RATE:
                self.last_smoke = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + SMOKE_OFFSET.rotate(-self.rot)
                Smoke(self.game, pos, dir)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.car_body, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

# þetta var fyrir byssu sem ég ætlaði að festa á bíllinn en ég náði ekki að láta hann
# byrta á bílnum
class Gun(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.barrel
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.barrel_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, 0)

    def update(self):
        self.rect = self.image.get_rect()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.barrel_draw = pg.Rect(0, 0, 60, 20)
        pg.draw.rect(self.image, BLACK, self.image)


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health  <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 80:
            col = GREEN
        elif self.health > 40:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pg.Rect(0, 0, width, 7)
        pg.draw.rect(self.image, col, self.health_bar)



class Smoke(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.smoke
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.smoke_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-SMOKE_SPREAD, SMOKE_SPREAD)
        self.vel = dir.rotate(spread) * SMOKE_SPEED
        self.spawn_time = pg.time.get_ticks()


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if  pg.time.get_ticks() - self.spawn_time > SMOKE_LIFETIME:
            self.kill()

#Þetta er til að geta loadað tiled mað í text editor en ekki map editor
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Obstacles fyrir mapið sem er gert í tiled editorinum
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
