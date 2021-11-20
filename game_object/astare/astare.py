import numpy
import random
import sys

from game_object.vec2 import Vec2

"""class Node:
        def __init__(self, number_node = None):
            self.node = number_node
            self.g = 0 
            self.previous = None"""

class Astare:
    def __init__(self, set_nodes, hueristics, numberNodes, target):
        self.numberNodes = numberNodes
        self.g = [0 for i in range(self.numberNodes)]
        self.previous = [None for i in range(self.numberNodes)]
        self.graph = None
        self.start = None
        self.target = target
        self.hueristics = hueristics
        self.set_nodes = set_nodes
        self.open = []
        self.closed = []
        self.counter = 0
        self.new_open_node = []
        self.current_node = None

    def algorithm(self, graph, start): 
        self.g = [0 for i in range(self.numberNodes)]
        self.previous = [None for i in range(self.numberNodes)]
        self.graph = graph
        self.start = start
        self.open = [self.start]
        self.closed = []
        while self.open:
            self.current_node = self.choose_node()
            if self.current_node == self.target:
                return self.build_path(self.current_node)
            self.open.remove(self.current_node)
            self.closed.append(self.current_node)
            self.get_adjacent_nodes()
            for adjacent in self.new_open_node:
                if adjacent not in self.open:
                    self.open.append(adjacent)
                    self.previous[adjacent] = self.current_node
                    self.g[adjacent] = self.g[self.current_node] + self.graph[self.current_node][adjacent]
                if self.g[self.current_node] + 1  < self.g[adjacent]: 
                    self.previous[adjacent] = self.current_node
                    self.g[adjacent] = self.g[self.current_node] + 1
        return []

    def get_adjacent_nodes(self):
        self.new_open_node = []
        for adjacent in range(self.numberNodes):
            if self.graph[self.current_node][adjacent] > 0:
                self.new_open_node.append(adjacent)
        for closed_node in self.closed:
            if closed_node in self.new_open_node:
                self.new_open_node.remove(closed_node)


    def build_path(self, to_node):
        path = []
        while self.previous[to_node] != None:
            path.append(self.set_nodes[to_node])
            for node in self.closed:
                if self.previous[to_node] == node:
                    to_node = node
        path.append(self.set_nodes[self.start])
        path.reverse()
        return path

    def  choose_node (self):
        min_cost = 500
        best_node = None
        for node in self.open:
            
            cost_start_to_node = self.g[node]
            cost_node_to_goal = self.hueristics[node][self.target]
            total_cost = cost_start_to_node + cost_node_to_goal
            
            if min_cost > total_cost:
                min_cost = total_cost
                best_node = node

        return best_node