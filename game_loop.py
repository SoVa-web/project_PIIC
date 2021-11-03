from typing import Any
import pygame 

import config
from config import WIDTH, HEIGHT, FPS, FIELD_W_SIZE, FIELD_H_SIZE
from game_object.field import Field
from game_object.vec2 import Vec2
from result_game import Result
from game_object.graph.graph import Graph
import time

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
        self.list_path = []
        self.draw_path = self.draw_path_dfs
        print("Using DFS")
        self.num_algoriyhm = 2

    def process_events(self):
        for event in pygame.event.get(): #--event queue--

            #--if we click "Close Window"--
            if event.type == pygame.QUIT:
                self.is_running = False
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
                    """ if self.num_algoriyhm == 3:
                        self.draw_path = self.draw_path_ucs
                        print(3)
                    """

                    

            #--if we stopped pressing a key--
            if event.type == pygame.KEYUP:
                for player in self.field.players:
                    player.key_processor.process_key_up_event(event)
                if event.key == pygame.K_RETURN:
                    self.is_running = False
                    GameLoop().start()

            

    def start(self):
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
                    player.move( self.draw_path)
                for opponent in self.field.opponents:
                    opponent.random_move( self.draw_path)
                for bullet in self.field.bullets:
                    bullet.bullet_move()
                for explosion in self.field.explosions:
                    explosion.delete(self.graph, self.draw_path)
                frame = 0
            if len(self.field.players) == 0 or len(self.field.opponents) == 0:
                self.is_running = False
            self.field.sprites.update()
            self.field.sprites.draw(screen)
            for path in self.list_path:
                for ver in path:
                    screen.blit(self.field.surface1, ((ver.x*(WIDTH//FIELD_W_SIZE)), (ver.y*(HEIGHT//FIELD_H_SIZE))))
            pygame.display.flip()

        screen_end = pygame.display.set_mode((WIDTH, HEIGHT))
        winner = ""
        if len(self.field.players) == 0:
            winner = "Opponent"
        if len(self.field.opponents) == 0:
            winner = "Player"
        result = Result(screen_end, winner)
        while self.end and not self.is_running:
            frame += 1
            self.clock.tick(FPS)
            self.process_events()
            result.draw()
            pygame.display.flip()

    def draw_path_dfs(self):
        #sp = time.time()

        self.list_path = []
        for player  in self.field.players:
            for opponent in self.field.opponents:
                path = self.graph.dfs(self.graph.set_nodes.index(player.pos), self.graph.set_nodes.index(opponent.pos))
                self.list_path.append(path)

        #print(time.time()-sp)
        
    def draw_path_bfs(self):
        #sp = time.time()

        self.list_path = []
        for player  in self.field.players:
            for opponent in self.field.opponents:
                path = self.graph.bfs(self.graph.set_nodes.index(player.pos), self.graph.set_nodes.index(opponent.pos))
                self.list_path.append(path)

        #print(time.time()-sp)

    def draw_path_ucs(self):
        #sp = time.time()

        self.list_path = []
        for player  in self.field.players:
            for opponent in self.field.opponents:
                path = self.graph.ucs(self.graph.set_nodes.index(player.pos), self.graph.set_nodes.index(opponent.pos))
                self.list_path.append(path)

        #print(time.time()-sp)

