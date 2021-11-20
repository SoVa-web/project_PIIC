import numpy
import random
import sys

from game_object.vec2 import Vec2

class Node:
        def __init__(self, number_node = None):
            self.node = number_node
            self.g = 0 
            self.previous = None

class Astare:
    def __init__(self, set_nodes, hueristics, numberNodes, target):
        self.numberNodes = numberNodes
        self.graph = None
        self.list_graph = None
        self.start = None
        self.target = Node(target)
        self.hueristics = hueristics
        self.set_nodes = set_nodes
        self.open = []
        self.closed = []
        self.counter = 0
        self.new_open = []
        self.new_open_node = []
        self.current_node = None

    def algorithm(self, graph, list_graph, start): 
        self.graph = graph
        self.list_graph = list_graph
        self.start = Node(start)
        self.open = [self.start]
        self.closed = []
        while self.open:
            self.current_node = self.choose_node()
            if self.current_node.node == self.target.node:
                return self.build_path(self.current_node)
            self.open.remove(self.current_node)
            self.closed.append(self.current_node)
            self.get_adjacent_nodes(self.current_node)
            for adjacent in self.new_open:
                if adjacent not in self.open:
                    self.open.append(adjacent)
                    adjacent.previous = self.current_node.node
                    adjacent.g = self.current_node.g + self.graph[self.current_node.node][adjacent.node]
                if self.current_node.g + 1  < adjacent.g: 
                    adjacent.previous = self.current_node.node
                    adjacent.g = self.current_node.g + 1
        return []

    def get_adjacent_nodes(self, current_node):
        self.new_open_node = []
        self.new_open = []
        for adjacent in range(self.numberNodes):
            if self.graph[current_node.node][adjacent] > 0:
                self.new_open_node.append(adjacent)
        for closed_node in self.closed:
            if closed_node.node in self.new_open_node:
                self.new_open_node.remove(closed_node.node)
        for node in self.new_open_node:
            self.new_open.append(Node(node))


    def build_path(self, to_node):
        path = []
        while to_node.previous != None:
            path.append(self.set_nodes[to_node.node])
            for node in self.closed:
                if to_node.previous == node.node:
                    to_node = node
        path.append(self.set_nodes[self.start.node])
        path.reverse()
        return path

    def  choose_node (self):
        min_cost = 500
        best_node = None
        for node in self.open:
            
            cost_start_to_node = node.g
            cost_node_to_goal = self.hueristics[node.node][self.target.node]
            total_cost = cost_start_to_node + cost_node_to_goal
            
            if min_cost > total_cost:
                min_cost = total_cost
                best_node = node

        return best_node