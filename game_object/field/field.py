from game_object.bullet.bullet import Bullet
import itertools
import random
from typing import List

import pygame

from game_object import Vec2
from game_object.barrier.wall import Wall
from game_object.player import Player
from config import FIELD_W_SIZE, FIELD_H_SIZE

line_color = (0, 255, 127)


class Field:
    def __init__(self, w_size, h_size):
        self.sprites = pygame.sprite.Group()
        self.w_size = w_size
        self.h_size = h_size
        self.players: List[Player] = [Player(self)]
        self.barriers = []
        self.num_block = 150
        self.bullets = []

        #--generating barriers positions--
        while self.num_block!=0:
             self.num_block-=1
             self.barriers.append(Wall(Vec2(random.randint(1, FIELD_W_SIZE), random.randint(1, FIELD_H_SIZE))))

        #--adding players to sprites on the field--
        for player in self.players:
            self.sprites.add(player.sprite)

        #--adding barriers to sprites on the field--
        for barrier in self.barriers:
            self.sprites.add(barrier.sprite)


        self.cell_size = 0
        self.w_padding = 0
        self.h_padding = 0

    def add_bullet_in_field(self, bullet):
        self.sprites.add(bullet.sprite)

    #--"Can the player move to this cell?"--
    def can_move_to_pos(self, pos: Vec2):
        #--if the cell is outside the field, you cannot move there--
        if not (0 <= pos.x < self.w_size and 0 <= pos.y < self.h_size):
            return False
        #--if there is an obstacle or a player in the cell, then you cannot move there--
        for game_obj in itertools.chain(self.players, self.barriers):
            if game_obj.pos == pos:
                return False
        return True

    def draw_grid(self, screen):
        width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
        if width < height:
            #--divide the width of the monitor by the number of cells--
            self.cell_size = width // self.w_size 
        else:
            #--divide the height of the monitor by the number of cells--
            self.cell_size = height // self.h_size
        field_size = min(width, height)
        self.w_padding = (width - field_size) // 2
        self.h_padding = (height - field_size) // 2

    
        #--grid lines--
        for x in range(self.w_size + 1):
            dot1 = Vec2(x=self.w_padding + x * self.cell_size, y=self.h_padding)
            dot2 = Vec2(x=self.w_padding + x * self.cell_size, y=self.h_padding + field_size)
            pygame.draw.line(screen, line_color, dot1, dot2)

        for y in range(self.h_size + 1):
            dot1 = Vec2(y=self.h_padding + y * self.cell_size, x=self.w_padding)
            dot2 = Vec2(y=self.h_padding + y * self.cell_size, x=self.w_padding + field_size)
            pygame.draw.line(screen, line_color, dot1, dot2)

    def draw(self, screen):
        screen.fill((130, 178, 137))
        self.draw_grid(screen)
        for game_obj in itertools.chain(self.players, self.barriers, self.bullets):
            game_obj.sprite.set_field_size_info(self.cell_size, self.w_padding, self.h_padding)
