from game_object import Vec2
from game_object.game_obj import GameObjectSprite

class BulletSprite(GameObjectSprite):
    pass

class Bullet:
    def __init__(self, pos: Vec2):
        self.pos = pos
        self.sprite = BulletSprite(self.pos, sprite_filename='shotOrange.png')