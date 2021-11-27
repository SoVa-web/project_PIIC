import random
import pygame
from typing import TYPE_CHECKING
from game_object import Vec2
from game_object.game_obj import GameObjectSprite
from config import WIDTH, HEIGHT, TIMER_EVENT_OPPONENT, TIMER_BULLET_OPPONENT
from game_object.bullet.bullet import Bullet


if TYPE_CHECKING:
    from game_object.field import Field
    

class OpponentSprite(GameObjectSprite):
    def __init__(self, pos: Vec2, sprite_filename: str, parent: 'Opponent'):
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

class Opponent:
    def __init__(self, parent: 'Field', img:str, pos: Vec2 = Vec2()):
        self.parent = parent
        self.pos = pos
        self.sprite = OpponentSprite(pos, img, parent=self)
        self.last_direction = Vec2(0, 1)
        self.dir_possible = [Vec2(x = +1, y = 0), Vec2(x = -1, y =0), Vec2(x = 0, y = +1), Vec2(x = 0, y = -1)]
        self.rand_dir = self.dir_possible[random.randint(0, 3)]
        self.timer = TIMER_EVENT_OPPONENT
        self.stupid_timer = TIMER_EVENT_OPPONENT
        self.timer_bul = TIMER_BULLET_OPPONENT

    def random_move(self, next_pos):#, draw_path
        self.timer -= 1
        if self.timer == 0:
            """rand_dir = self.dir_possible[random.randint(0, 3)]
            self.rand_dir = rand_dir
            next_pos = self.pos + self.rand_dir"""
            dir = Vec2((next_pos.x - self.pos.x), (next_pos.y - self.pos.y))
            if not dir == Vec2(0, 0):
                self.last_direction = dir
                self.random_shot()
            if self.parent.can_move_to_pos(next_pos) :
                self.pos = next_pos
                self.sprite.update_field_pos(self.pos)
            # else сменить направление#
            self.timer = TIMER_EVENT_OPPONENT
            #draw_path()

    def random_shot(self):
       self.timer_bul -= 1
       if self.timer_bul == 0:
            bullet = Bullet(self.parent, self.pos+self.last_direction, self.last_direction, "Opponent")
            bullet.sprite.update_field_pos(self.pos+self.last_direction)
            self.parent.bullets.append(bullet)
            self.parent.add_bullet_in_field(bullet)
            self.timer_bul = TIMER_BULLET_OPPONENT
    
    def move(self):
        self.stupid_timer -= 1
        if self.stupid_timer == 0:
            rand_dir = self.dir_possible[random.randint(0, 3)]
            self.rand_dir = rand_dir
            next_pos = self.pos + self.rand_dir
            if not self.rand_dir == Vec2(0, 0):
                self.last_direction = self.rand_dir
                self.random_shot()
            if self.parent.can_move_to_pos(next_pos) :
                self.pos = next_pos
            # else сменить направление#
            self.sprite.update_field_pos(self.pos) 
            self.stupid_timer = TIMER_EVENT_OPPONENT
        