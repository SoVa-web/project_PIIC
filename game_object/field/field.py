from game_object.bullet.bullet import Bullet
import itertools
import random
from typing import List

import pygame
import numpy

from game_object import Vec2
from game_object.barrier.wall import Wall
from game_object.opponent.opponent import Opponent
from game_object.player import Player
from config import FIELD_W_SIZE, FIELD_H_SIZE, WIDTH, HEIGHT

line_color = (0, 255, 127)


class Field:
    def __init__(self, w_size, h_size):
        self.sprites = pygame.sprite.Group()
        self.w_size = w_size
        self.h_size = h_size
        self.players = []
        self.opponents = []
        self.stupid_opponents = []
        self.barriers = []
        self.num_chain_block = 16
        self.num_opponents = 1
        self.num_stupid_opponents = 1
        self.bullets = []
        self.explosions = []
        self.surface_player = pygame.Surface((WIDTH//FIELD_W_SIZE, HEIGHT//FIELD_H_SIZE))
        self.surface_player.fill((255, 203, 219))
        self.surface_player.set_alpha(150)
        self.surface_opponent = pygame.Surface((WIDTH//FIELD_W_SIZE, HEIGHT//FIELD_H_SIZE))
        self.surface_opponent.fill((0, 0, 0))
        self.surface_opponent.set_alpha(150)
        self.score_player = 0
        self.score_opponent = 0


        #--add player--
        self.players.append(Player(self, Vec2(random.randint(0, FIELD_W_SIZE-1), random.randint(0, FIELD_H_SIZE-1))))
        
        #--add opponents--
        while self.num_opponents!=0:
            vec = Vec2(random.randint(0, FIELD_W_SIZE-1), random.randint(0, FIELD_H_SIZE-1))
            if self.can_move_to_pos(vec):
                self.num_opponents-=1
                self.opponents.append(Opponent(self, 'opponent.png', vec))

        while self.num_stupid_opponents!=0:
            vec = Vec2(random.randint(0, FIELD_W_SIZE-1), random.randint(0, FIELD_H_SIZE-1))
            if self.can_move_to_pos(vec):
                self.num_stupid_opponents-=1
                self.stupid_opponents.append(Opponent(self, 'tank_green.png', vec))
             
        #--generating barriers positions--
        while self.num_chain_block != 0:
             vec = Vec2(random.randint(0, FIELD_W_SIZE-1), random.randint(0, FIELD_H_SIZE-1))
             length_bar_1 = random.randint(1, FIELD_W_SIZE-10)
             dir_1 = random.randint(0, 1)
             length_bar_2 = random.randint(1, FIELD_W_SIZE-10)
             dir_2 = random.randint(0, 1)
             set_dir_1 = [Vec2(+1, 0), Vec2(-1, 0)]
             set_dir_2 = [Vec2(0, -1), Vec2(0, +1)]
             if self.can_move_to_pos(vec):
                self.num_chain_block -= 1
                self.barriers.append(Wall(vec))
             while length_bar_1 > 0:
                vec = vec + set_dir_1[dir_1]
                length_bar_1 -= 1
                if self.can_move_to_pos(vec):
                    self.barriers.append(Wall(vec))
             while length_bar_2 > 0:
                vec = vec + set_dir_2[dir_2]
                length_bar_2 -= 1
                if self.can_move_to_pos(vec):
                    self.barriers.append(Wall(vec))

                
             

        #--adding players to sprites on the field--
        for player in self.players:
            self.sprites.add(player.sprite)

        #--adding opponents to sprites on the field--
        for opponent in self.opponents:
            self.sprites.add(opponent.sprite)

        for opponent in self.stupid_opponents:
            self.sprites.add(opponent.sprite)

        #--adding barriers to sprites on the field--
        for barrier in self.barriers:
            self.sprites.add(barrier.sprite)


        self.cell_size = 0
        self.w_padding = 0
        self.h_padding = 0

    def add_bullet_in_field(self, bullet):
        self.sprites.add(bullet.sprite)

    def add_explosion(self, explosion):
        self.sprites.add(explosion.sprite)

    #--"Can the player move to this cell?"--
    def can_move_to_pos(self, pos: Vec2):
        #--if the cell is outside the field, you cannot move there--
        if not (0 <= pos.x < self.w_size and 0 <= pos.y < self.h_size):
            return False
        #--if there is an obstacle or a player in the cell, then you cannot move there--
        for game_obj in itertools.chain(self.players, self.opponents, self.stupid_opponents,  self.barriers):
            if game_obj.pos == pos:
                return False
        return True

    #--"Can the bullet explosion this cell?"--
    def can_explosion_this(self, pos: Vec2):
        for game_obj in itertools.chain(self.opponents, self.stupid_opponents, self.barriers, self.players):
            if game_obj.pos == pos:
                return True
        return False

    #--"Can we draw an edge of the graph?"--
    def can_draw_edge_graph(self, pos: Vec2):
        if not (0 <= pos.x < self.w_size and 0 <= pos.y < self.h_size):
            return False
        for game_obj in itertools.chain(self.barriers):
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
        for game_obj in itertools.chain(self.players, self.barriers, self.bullets, self.explosions, self.opponents, self.stupid_opponents):
            game_obj.sprite.set_field_size_info(self.cell_size, self.w_padding, self.h_padding)
            


