from typing import List
from typing import TYPE_CHECKING
import time
import sys
from heapq import heappush, heappop
import numpy
import math
import time

import pygame
from pygame.image import tostring

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
        self.init_matrix()
        self.transform_field_to_matrix()
        self.init_list()
        self.transform_field_to_list()

        
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
        self.set_nodes.reverse()

    
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
                       

    def dfs(self, start, target):
        self.visited = [0 for x in range(FIELD_H_SIZE*FIELD_W_SIZE)]
        self.prev = [-1 for x in range(FIELD_H_SIZE*FIELD_W_SIZE)]
        self.length = 0
        self.start = start
        self.end = target
        self.shortLength = sys.maxsize
        path = []
        self.dfs_algorithm(self.start)
        path = self.prev_dfs()
        if not  path == None:
            if len(path) > 2:
                path.pop(len(path)-1)
                path.pop(0) 
            else:
                path = []    
        return path

    def dfs_algorithm(self, vertex):
        self.visited[vertex] = 1
        for i in range(FIELD_H_SIZE*FIELD_W_SIZE):
            if self.matrix_adjacency[vertex][i] == 1 and self.visited[i] == 0:
                nbr = i
                self.prev[nbr] = vertex
                self.dfs_algorithm(nbr)

    def prev_dfs(self):
        vertex = self.end
        route = [] 
        while vertex != -1:
            route.append(self.set_nodes[vertex])
            vertex = self.prev[vertex]
        route.reverse()
        return route

    def bfs(self, start, target):
        path = self.bfs_algorithm(start, target)
        if path == None:
            path = []
        if len(path) > 2:
            path.pop(len(path)-1)
            path.pop(0) 
        else:
            path = []  
        for i in range(len(path)):
            path[i] = self.set_nodes[path[i]]
        #print(path)
        return path


    def bfs_algorithm(self, start, target):
        visited = []
        queue = [[start]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            #print(node)
            if node not in visited:
                neighbours = self.list_adjacency[node]
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    if neighbour == target:
                        #print(new_path)
                        return new_path
                visited.append(node)
        return []

                    
    def ucs(self, start, target):
        path = self.ucs_algorithm(start, target)
        if path == None:
            path = []
        if len(path) > 2:
            path.pop(len(path)-1)
            path.pop(0) 
        else:
            path = []  
        for i in range(len(path)):
            path[i] = self.set_nodes[path[i]]
        return path

    def ucs_algorithm(self, start, target):
        pass

    def shortestDistancesInStraightLine(self):
        sp = time.time()
        distances = []
        for i in range(FIELD_W_SIZE*FIELD_H_SIZE):
            distances.append(numpy.array([0 for x in range(FIELD_W_SIZE*FIELD_H_SIZE)]))
        for x in range(FIELD_W_SIZE*FIELD_H_SIZE):
            for y in range(FIELD_W_SIZE*FIELD_H_SIZE):
                distances[x][y] = math.sqrt(math.pow((self.set_nodes[x].x - self.set_nodes[y].x), 2) + math.pow((self.set_nodes[x].y - self.set_nodes[y].y), 2))
        print("Time hueristics : "+ str((time.time()-sp)) + "\n")
        return distances

        

    