import pygame
from typing import TYPE_CHECKING
from game_object import Vec2
from game_object.game_obj import GameObjectSprite
from config import TIMER_EXPLOSION


if TYPE_CHECKING:
    from game_object.field import Field

class ExplosionSprite(GameObjectSprite):
    def __init__(self, pos: Vec2, sprite_filename: str, parent:'Explosion'):
        super().__init__(pos,  sprite_filename)
        self.parent = parent
        self.pos = pos

class Explosion:
    def __init__(self, parent: 'Field', pos: Vec2 = Vec2()):
        self.parent = parent
        self.pos = pos
        self.sprite = ExplosionSprite(self.pos, 'explosion4.png', parent=self)
        self.timer = TIMER_EXPLOSION

    def delete(self, update_matrix, draw_path):
        self.timer -= 1
        if self.timer == 0:
            self.parent.parent.explosions.remove(self)
            self.sprite.kill()
            #update_matrix()
            #draw_path()