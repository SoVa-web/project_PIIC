from typing import TYPE_CHECKING

import pygame

FPS = 60
WIDTH = 700
HEIGHT = 700
MOVE_EVERY_NTH_FRAME = 6
FIELD_W_SIZE = 20
FIELD_H_SIZE = 20


#from config import WIDTH, HEIGHT
from game_object.game_obj import GameObjectSprite
from game_object.vec2 import Vec2
from game_object.bullet.bullet import Bullet

if TYPE_CHECKING:
    from game_object.field import Field


class PlayerSprite(GameObjectSprite):
    def __init__(self, pos: Vec2, sprite_filename: str, parent: 'Player'):
        super().__init__(pos, sprite_filename)
        self.image = self.orig_image = pygame.transform.rotate(self.orig_image, 180)
        self.parent = parent

        self.view_directions = {}
        self.view_direction_angle = 0

        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = pos

    def scale_image(self):
        image = pygame.transform.scale(self.orig_image, (self.cell_size, self.cell_size))
        for angle in range(0, 360, 45):
            self.view_directions[angle] = pygame.transform.rotate(image, -angle)

    def get_view_direction_image(self):
        vec = self.parent.key_processor.get_vector()
        if vec == Vec2(0, 0):
            return
        view_direction_angle = {
            Vec2(x=0, y=-1): 0,
            Vec2(x=1, y=-1): 45,
            Vec2(x=1, y=0): 90,
            Vec2(x=1, y=+1): 135,
            Vec2(x=0, y=+1): 180,
            Vec2(x=-1, y=+1): 225,
            Vec2(x=-1, y=0): 270,
            Vec2(x=-1, y=-1): 315,
        }[vec]
        self.scaled_image = self.view_directions[view_direction_angle]

    def update(self):
        self.get_view_direction_image()
        super().update()


class PlayerKeyProcessor:
    def __init__(self, parent: 'Player'):
        self.parent = parent
        self.directions = {
            pygame.K_LEFT: Vec2(x=-1, y=0),
            pygame.K_UP: Vec2(x=0, y=-1),
            pygame.K_RIGHT: Vec2(x=+1, y=0),
            pygame.K_DOWN: Vec2(x=-0, y=+1)
        }
        self.is_key_pressed = {}
        self.is_space_pressed = False
        

    def process_key_down_event(self, event):
        print(event.key)
        self.is_key_pressed[event.key] = True
        if event.key == 32:
            self.is_space_pressed = True

    def process_key_up_event(self, event):
        self.is_key_pressed[event.key] = False

    def get_vector(self):
        res = Vec2()
        for key, direction in self.directions.items():
            if self.is_key_pressed.get(key, False):
                res += direction
        return res


class Player:
    def __init__(self, parent: 'Field', pos: Vec2 = Vec2(), hp=10):
        self.parent = parent
        self.hp = hp
        self.pos = pos
        self.sprite = PlayerSprite(Vec2(1, 1), 'player.png', parent=self)
        self.key_processor = PlayerKeyProcessor(parent=self)
        self.bullets =  []

    def move(self):
        next_pos = self.pos + self.key_processor.get_vector()
        if self.parent.can_move_to_pos(next_pos):
            self.pos = next_pos
        self.sprite.update_field_pos(self.pos)

    def shot(self):
        if self.key_processor.is_space_pressed:
            self.bullets.append(Bullet(Vec2(self.pos.x+1, self.pos.y+1)))



