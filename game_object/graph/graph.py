from typing import List
from typing import TYPE_CHECKING
import time
import sys
import numpy

import pygame

from game_object.opponent.opponent import Opponent
from config import FIELD_W_SIZE, FIELD_H_SIZE
from game_object.field import Field
from game_object import Vec2

class Graph:
    def __init__(self, parent: "Field"):
        self.matrix_adjacency = []
        self.list_adjacency = numpy.array([])
        self.set_nodes = []
        self.num_rows = FIELD_H_SIZE*FIELD_W_SIZE
        self.num_columns = FIELD_H_SIZE*FIELD_W_SIZE
        self.parent = parent
        self.init_set()
        sp = time.time()
        self.init_matrix()
        self.transform_field_to_matrix()
        print(time.time()-sp)

        
    def init_matrix(self):
        self.matrix_adjacency = []
        self.num_rows = FIELD_H_SIZE*FIELD_W_SIZE
        self.num_columns = FIELD_H_SIZE*FIELD_W_SIZE
        """while self.num_rows != 0:
            self.num_rows -= 1"""
        for i in range(self.num_rows):
            self.matrix_adjacency.append(numpy.array([0 for x in range(self.num_columns)]))

    def init_list(self):
        self.list_adjacency = []
        self.num_rows = FIELD_H_SIZE*FIELD_W_SIZE
        while self.num_rows != 0:
            self.num_rows -= 1
            self.list_adjacency.append([])

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
        #iter = FIELD_W_SIZE*FIELD_H_SIZE
        num = FIELD_W_SIZE*FIELD_H_SIZE
        dir = [Vec2(+1, 0), Vec2(-1, 0), Vec2(0, +1), Vec2(0, -1)]
        """while iter > 0:
            iter-=1"""
        for i in dir:
             for iter in range(num):
                if self.parent.can_draw_edge_graph(self.set_nodes[iter] + i):
                        index_adj = self.set_nodes.index((self.set_nodes[iter] + i))
                        if self.parent.can_draw_edge_graph((self.set_nodes[iter])) and iter != index_adj:
                            self.matrix_adjacency[iter][index_adj] = self.matrix_adjacency[index_adj][iter] = 1

    def transform_field_to_list(self):
        iter = FIELD_W_SIZE*FIELD_H_SIZE
        dir = [Vec2(+1, 0), Vec2(-1, 0), Vec2(0, +1), Vec2(0, -1)]
        while iter > 0:
            iter -= 1
            for i in dir:
                if self.parent.can_draw_edge_graph(self.set_nodes[iter] + i):
                    index_adj = self.set_nodes.index((self.set_nodes[iter] + i))
                    if  self.parent.can_draw_edge_graph((self.set_nodes[iter])):
                        self.list_adjacency[iter].append(index_adj)
        print(self.list_adjacency)
                       

    def dfs(self, start, target):
        self.N = len(self.set_nodes)
        self.visited = [0 for x in range(self.N)]
        self.prev = [-1 for x in range(self.N)]
        self.length = 0
        self.start = start
        self.end = target
        self.shortLength = sys.maxsize
        path = []
        if not  self.findPath() == None:
            path = self.findPath()
            if len(path) > 2:
                path.pop(len(path)-1)
                path.pop(0)     
        return path

    def dfs_algorithm(self, vertex):
        self.length +=1
        if self.length > self.shortLength:
            return
        if vertex == self.end:
            self.shortLength = self.length
            return
        self.visited[vertex] = 1
        for i in range(self.N):
            if self.matrix_adjacency[vertex][i] == 1 and self.visited[i] == 0:
                nbr = i
                self.prev[nbr] = vertex
                self.dfs_algorithm(nbr)
        self.length -=1

    def findPath(self):
        self.dfs_algorithm(self.start)
        path = self.trace_route()
        return path

    def trace_route(self):
        vertex = self.end
        route = [] 
        while vertex != -1:
            route.append(self.set_nodes[vertex])
            vertex = self.prev[vertex]
        route.reverse()
        return route



    def bfs(self):
        pass


    def ucs(self):
        self.init_matrix()
        sp = time.time()
        self.transform_field_to_matrix()
        print(time.time()-sp)

    




    