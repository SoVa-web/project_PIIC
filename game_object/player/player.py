from typing import TYPE_CHECKING

import pygame
import itertools

import random
from config import WIDTH, HEIGHT, TIMER_EVENT_PLAYER, FPS
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
        for angle in range(0, 360, 90):
            self.view_directions[angle] = pygame.transform.rotate(image, -angle)

    def get_view_direction_image(self):
        vec = self.parent.last_direction
        for v in ([Vec2(1, 1), Vec2(-1, -1), Vec2(-1, 1), Vec2(1, -1), Vec2(0, 0)]):
            if v == vec:
                return 
        view_direction_angle = {
            Vec2(x=0, y=-1): 0,
            Vec2(x=+1, y=0): 270,
            Vec2(x=0, y=+1): 180,
            Vec2(x=-1, y=0): 90,
        }[vec]
        self.scaled_image = pygame.transform.rotate(self.orig_image, view_direction_angle)

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
        

    def process_key_down_event(self, event):
        self.is_key_pressed[event.key] = True
        if event.key == pygame.K_SPACE:
            self.parent.shot()

    def process_key_up_event(self, event):
        self.is_key_pressed[event.key] = False

    def get_vector(self):
        res = Vec2()
        for key, direction in self.directions.items():
            if self.is_key_pressed.get(key, False):
                res += direction
        return res


class Player:
    def __init__(self, parent: 'Field', pos: Vec2 = Vec2()):
        self.parent = parent
        self.pos = pos
        self.sprite = PlayerSprite(pos, 'player.png', parent=self)
        self.key_processor = PlayerKeyProcessor(parent=self)
        self.last_direction = Vec2(0, 1)
        self.dir_possible = [Vec2(x = +1, y = 0), Vec2(x = -1, y =0), Vec2(x = 0, y = +1), Vec2(x = 0, y = -1)]
        self.timer = TIMER_EVENT_PLAYER
        

    def move(self, strategyPlayer): #draw_path in args
        #--we forbid moving diagonally--
        for vec in ([Vec2(1, 1), Vec2(-1, -1), Vec2(-1, 1), Vec2(1, -1)]):
            if vec == self.key_processor.get_vector():
                return 
        next_pos = self.pos + self.key_processor.get_vector()
        if not self.key_processor.get_vector() == Vec2(0, 0):
            self.last_direction = self.key_processor.get_vector()
        if self.parent.can_move_to_pos(next_pos) :
            self.pos = next_pos
            #draw_path()
            strategyPlayer(self)
        # else сменить направление#
        self.sprite.update_field_pos(self.pos)


    def shot(self):
        bullet = Bullet(self.parent, self.pos+self.last_direction, self.last_direction, "Player")
        bullet.sprite.update_field_pos(self.pos+self.last_direction)
        self.parent.bullets.append(bullet)
        self.parent.add_bullet_in_field(bullet)

    def randomMove(self, nextPos):
            self.timer -= 1
            if self.timer == 0:
                dirMove = Vec2((nextPos.x - self.pos.x), (nextPos.y - self.pos.y))
                if not dirMove == Vec2(0, 0):
                    self.last_direction = dirMove
                if self.parent.can_move_to_pos(nextPos) :
                    self.pos = nextPos
                    self.sprite.update_field_pos(self.pos)
                for op in itertools.chain(self.parent.opponents, self.parent.stupid_opponents):
                    if op.pos.x == self.pos.x and self.last_direction.x == 0: 
                        if op.pos.y >= self.pos.y:
                            self.last_direction = Vec2(0, 1)
                            self.sprite.update_field_pos(self.pos)
                            self.shot()
                        if op.pos.y < self.pos.y:
                            self.last_direction = Vec2(0, -1)
                            self.sprite.update_field_pos(self.pos)
                            self.shot()
                    if op.pos.y == self.pos.y and self.last_direction.y == 0:
                        if op.pos.x >= self.pos.x:
                            self.last_direction = Vec2(1, 0)
                            self.sprite.update_field_pos(self.pos)
                            self.shot()
                        if op.pos.x < self.pos.x:
                            self.last_direction = Vec2(-1, 0)
                            self.sprite.update_field_pos(self.pos)
                            self.shot()
                self.timer = TIMER_EVENT_PLAYER
    
""" def move(self):
        for vec in ([Vec2(1, 1), Vec2(-1, -1), Vec2(-1, 1), Vec2(1, -1)]):
            if vec == self.last_direction:
                return 
        next_pos = self.pos + self.last_direction
        if self.parent.can_move_to_pos(next_pos) :
            self.pos = next_pos
        # else сменить направление#
        self.sprite.update_field_pos(self.pos)
        
"""

        
            



