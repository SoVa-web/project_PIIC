import itertools
import random
from typing import List
from typing import TYPE_CHECKING
import time

import pygame

from game_object.opponent.opponent import Opponent
from config import FIELD_W_SIZE, FIELD_H_SIZE
from game_object.field import Field
from game_object import Vec2

class Graph:
    def __init__(self, parent: "Field"):
        self.matrix_adjacency = []
        self.set_nodes = []
        self.num_rows = FIELD_H_SIZE*FIELD_W_SIZE
        self.num_columns = FIELD_H_SIZE*FIELD_W_SIZE
        self.parent = parent
        self.init_matrix()
        self.init_set()
        sp = time.time()
        self.transform_field_to_matrix()
        print(time.time()-sp)
        
    def init_matrix(self):
        self.matrix_adjacency = []
        while self.num_rows != 0:
            self.matrix_adjacency.append([])
            self.num_rows -= 1
        for i in self.matrix_adjacency:
            while self.num_columns != 0:
                i.append(0)
                self.num_columns -= 1
            self.num_columns = FIELD_H_SIZE*FIELD_W_SIZE

    #--columns - x, rows - y --
    def init_set(self):
        self.num_rows = FIELD_H_SIZE
        while self.num_rows > 0:
            self.num_columns = FIELD_W_SIZE
            self.num_rows -= 1
            while self.num_columns > 0:
                self.num_columns -= 1
                self.set_nodes.append(Vec2(self.num_columns, self.num_rows))

    
    #--We connect graph vertices with an edge only if they are adjacent and there is no barrier in both of them--
    def transform_field_to_matrix(self):
        iter = FIELD_W_SIZE*FIELD_H_SIZE
        dir = [Vec2(+1, 0), Vec2(-1, 0), Vec2(0, +1), Vec2(0, -1)]
        while iter > 0:
            iter -= 1
            for i in dir:
                if self.parent.can_draw_edge_graph(self.set_nodes[iter] + i):
                    index_adj = self.set_nodes.index((self.set_nodes[iter] + i))
                    if  self.parent.can_draw_edge_graph((self.set_nodes[iter])):
                        self.matrix_adjacency[iter][index_adj] = 1
                        self.matrix_adjacency[index_adj][iter] = 1
                    else:
                        self.matrix_adjacency[iter][index_adj] = 0
                        self.matrix_adjacency[index_adj][iter] = 0








    