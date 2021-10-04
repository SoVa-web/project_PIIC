import pygame
from typing import TYPE_CHECKING
from game_object import Vec2
from game_object.game_obj import GameObjectSprite
from config import WIDTH, HEIGHT


if TYPE_CHECKING:
    from game_object.field import Field


class BulletSprite(GameObjectSprite):
    def __init__(self, pos: Vec2, dir:Vec2, sprite_filename: str, parent:'Bullet'):
        super().__init__(pos,  sprite_filename)
        self.image = self.orig_image = pygame.transform.rotate(self.orig_image, 180)
        if dir == Vec2(0, 1):
            self.image = self.orig_image = pygame.transform.rotate(self.orig_image, 0)
        if dir == Vec2(0, -1):
            self.image = self.orig_image = pygame.transform.rotate(self.orig_image, 180)
        if dir == Vec2(1, 0):
            self.image = self.orig_image = pygame.transform.rotate(self.orig_image, 90)
        if dir == Vec2(-1, 0):
            self.image = self.orig_image = pygame.transform.rotate(self.orig_image, 270)
        self.parent = parent

        self.view_directions = {}
        self.view_direction_angle = 0

        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = pos
        self.dir = dir

    

class Bullet:
    def __init__(self, parent: 'Field', pos: Vec2 = Vec2(), dir:Vec2 = Vec2()):
        self.parent = parent
        self.pos = pos
        self.dir = dir
        self.sprite = BulletSprite(self.pos, self.dir, 'shotOrange.png', parent=self)


#    def update(self):

#аналогічна реалізація що і в гравцеві
