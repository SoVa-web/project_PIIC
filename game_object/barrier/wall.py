from game_object import Vec2
from game_object.game_obj import GameObjectSprite


class WallSprite(GameObjectSprite):
    pass


class Wall:
    def __init__(self, pos: Vec2):
        self.pos = pos
        self.sprite = WallSprite(self.pos, sprite_filename='brick_wall.png')
