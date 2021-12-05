from typing import Any
import pygame 
import itertools
import sys
import csv
import math

import config
from config import WIDTH, HEIGHT, FPS, FIELD_W_SIZE, FIELD_H_SIZE
from game_object import vec2
from game_object.field import Field
from game_object.vec2 import Vec2
from result_game import Result
from game_object.graph.graph import Graph
import time
from game_object.astare.astare import Astare
import random
from game_object.alphabeta.alphabeta import MinimaxAlphaBeta
from game_object.expectimax.expectimax import Expectimax
pygame.init()


#displaying the logo and name of the game

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Танчики")
pygame.display.set_icon(pygame.image.load('data/icon/gamelogo.png'))


class GameLoop:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.end = False
        self.field = Field(config.FIELD_W_SIZE, config.FIELD_H_SIZE)
        self.graph = Graph(self.field)
        self.list_path_players = []
        self.list_path_opponents = []
        self.dir = [Vec2(0, 1), Vec2(0, -1), Vec2(1, 0), Vec2(-1, 0)]
        self.draw_path = self.draw_path_bfs
        self.strategyPlayerMove = self.strategyPlayer
        self.num_algoriyhm = 2
        self.hueristics = self.graph.shortestDistancesInStraightLine()
        self.astare = Astare(self.graph.set_nodes, self.hueristics, FIELD_H_SIZE*FIELD_W_SIZE)
        #self.targetPlayer = None
        #self.choosingTarget()
        self.strategyOpponents()

        self.filename = "result_games.csv"
        
    def process_events(self):
        for event in pygame.event.get(): #--event queue--

            #--if we click "Close Window"--
            if event.type == pygame.QUIT:
                self.end = False

            #--if we pressed a key--
            if event.type == pygame.KEYDOWN:
                for player in self.field.players: #перевірити правильність, щоб не всі одночасно рухались 
                    player.key_processor.process_key_down_event(event)
                if event.key == pygame.K_z:
                    self.num_algoriyhm -= 1
                    if self.num_algoriyhm == 1:
                        self.num_algoriyhm = 3
                        self.draw_path = self.draw_path_bfs
                        print("Using BFS")
                    if self.num_algoriyhm == 2:
                        self.draw_path = self.draw_path_dfs
                        print("Using DFS")

                    

            #--if we stopped pressing a key--
            if event.type == pygame.KEYUP:
                for player in self.field.players:
                    player.key_processor.process_key_up_event(event)
                if event.key == pygame.K_RETURN:
                    GameLoop().start()

            

    def start(self):
        tm_start = time.time()
        self.is_running = True
        self.end = True
        frame = 0
        while self.is_running and self.end:
            frame += 1
            self.clock.tick(FPS)
            self.process_events()
            self.field.draw(screen)
            if frame == config.MOVE_EVERY_NTH_FRAME:
                for player  in self.field.players:
                    #self.strategyPlayer(player)
                    self.minimax(player)
                for opponent in self.field.opponents:
                    self.strategyOpponents()
                for opponent in self.field.stupid_opponents:
                    opponent.move()
                for bullet in self.field.bullets:
                    bullet.bullet_move()
                for explosion in self.field.explosions:
                    explosion.delete(self.graph)
                frame = 0
            if len(self.field.players) == 0 or len(self.field.opponents + self.field.stupid_opponents) == 0:
                self.is_running = False
            self.field.sprites.update()
            self.field.sprites.draw(screen)
            pygame.display.flip()

        screen_end = pygame.display.set_mode((WIDTH, HEIGHT))
        winner = ""
        winner_index = 0
        if len(self.field.players) == 0:
            winner = "Opponent"
            winner_index = 0
        if len(self.field.opponents + self.field.stupid_opponents) == 0:
            winner = "Player"
            winner_index = 1

        tm_end = time.time() - tm_start
        with open(self.filename, "a", newline="") as file:
            #expectimax - 1, alphabeta - 0
            result = [winner_index, self.field.score_player, round(tm_end), 1]
            writer = csv.writer(file)
            writer.writerow(result)
        result = Result(screen_end, winner)
        GameLoop().start()
        """while self.end and not self.is_running:
            frame += 1
            self.clock.tick(FPS)
            self.process_events()
            result.draw()
            pygame.display.flip()"""

    def draw_path_dfs(self):
        self.list_path = []
        for player  in self.field.players:
            for opponent in self.field.opponents:
                path = self.graph.dfs(self.graph.set_nodes.index(player.pos), self.graph.set_nodes.index(opponent.pos))
                #self.list_path.append(path)
        
    def draw_path_bfs(self):
        self.list_path_opponents = []
        for opponent in self.field.opponents:
            for player  in self.field.players:
                path = self.graph.bfs(self.graph.set_nodes.index(opponent.pos), self.graph.set_nodes.index(player.pos))
                self.list_path_opponents.append(path)
                if len(path) > 0:
                    opponent.random_move(path[0])


    def strategyPlayer(self, player):
        self.list_path_players = []
        path = self.astare.algorithm(self.graph.matrix_adjacency, self.graph.set_nodes.index(player.pos), self.graph.set_nodes.index(self.targetPlayer) )
        self.list_path_players.append(path)
        if len(path) > 1:
            path.pop(0)
        if len(path) > 0:
            player.randomMove(path[0])
        if player.pos == path[-1]:
                self.choosingTarget()

    def strategyOpponents(self):
        self.list_path_opponents = []
        for op in self.field.opponents:
            path = self.astare.algorithm(self.graph.matrix_adjacency, self.graph.set_nodes.index(op.pos), self.graph.set_nodes.index(self.field.players[0].pos) )
            self.list_path_opponents.append(path)
            if len(path) > 1:
                path.pop(0)
            if len(path) > 0:
                op.random_move(path[0])
            else:
                op.move()
            

    #checking if we can get to the target
    def consist(self):
        self.list_path_players = []
        path = []
        for player  in self.field.players:
            path = self.astare.algorithm(self.graph.matrix_adjacency, self.graph.set_nodes.index(player.pos), self.graph.set_nodes.index(self.targetPlayer) )
            if len(path) == 0:
                return False
            if len(path) > 1:
                path.pop(0)
            if len(path) > 0:
                player.randomMove(path[0])
            else:
                player.randomMove(player.pos + self.dir[random.randint(0, 3)])
                print(player.pos + self.dir[random.randint(0, 3)])
                player.shot()
            if player.pos == path[-1]:
                self.choosingTarget()
        self.list_path_players.append(path)
        return True 

    #use it to select a new target
    def choosingTarget(self):
        self.targetPlayer = Vec2(random.randint(0, FIELD_W_SIZE-1), random.randint(0, FIELD_H_SIZE-1))
        while not self.field.can_move_to_pos(self.targetPlayer) or not self.consist():
            self.targetPlayer = Vec2(random.randint(0, FIELD_W_SIZE-1), random.randint(0, FIELD_H_SIZE-1))

    def minimax(self, player):
        tm = time.time()
        self.directions = [ 
            Vec2(x=-1, y=0),
            Vec2(x=+1, y=0),
            Vec2(x=0, y=+1),
            Vec2(x=0, y=-1)
        ]
        best_mov = None
        best_evl = - sys.maxsize
        op = [opponent.pos for opponent in (self.field.opponents + self.field.stupid_opponents)]
        for d in self.directions:
            best = player.pos + d
            #cur_evl = MinimaxAlphaBeta(self.field).minimax([best], op, 0, 1, False, -1000 , +1000 )
            cur_evl = Expectimax(self.field).expectimax([best], op, 0, 1, False)
            if cur_evl >= best_evl:
                best_evl = cur_evl
                best_mov = d
        player.randomMove(player.pos + best_mov)
        print("time")
        print(time.time() - tm)

