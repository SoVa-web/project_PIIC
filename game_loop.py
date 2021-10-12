from typing import Any
import pygame as pygame

import config
from config import WIDTH, HEIGHT, FPS
from game_object.field import Field
from result_game import Result

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

    def process_events(self):
        for event in pygame.event.get(): #--event queue--

            #--if we click "Close Window"--
            if event.type == pygame.QUIT:
                self.is_running = False

            #--if we pressed a key--
            if event.type == pygame.KEYDOWN:
                for player in self.field.players: #перевірити правильність, щоб не всі одночасно рухались 
                    player.key_processor.process_key_down_event(event)

            #--if we stopped pressing a key--
            if event.type == pygame.KEYUP:
                for player in self.field.players:
                    player.key_processor.process_key_up_event(event)
                if event.key == pygame.K_RETURN:
                    self.is_running = False
                    GameLoop().start()

            

    def start(self):
        self.is_running = True
        frame = 0
       
        while self.is_running:
            frame += 1
            self.clock.tick(FPS)
            self.process_events()
            self.field.draw(screen)
            
            if frame == config.MOVE_EVERY_NTH_FRAME:
                for player  in self.field.players:
                    player.move()
                for opponent in self.field.opponents:
                    opponent.random_move()
                for bullet in self.field.bullets:
                    bullet.bullet_move()
                for explosion in self.field.explosions:
                    explosion.delete()
                frame = 0
            if len(self.field.players) == 0 or len(self.field.opponents) == 0:
                self.is_running = False
            self.field.sprites.update()
            self.field.sprites.draw(screen)
            pygame.display.flip()

        screen_end = pygame.display.set_mode((WIDTH, HEIGHT))
        winner = ""
        if len(self.field.players) == 0:
            winner = "Opponent"
        if len(self.field.opponents) == 0:
            winner = "Player"
        result = Result(screen_end, winner)
        while not self.is_running:
            frame += 1
            self.clock.tick(FPS)
            self.process_events()
            result.draw()
            pygame.display.flip()

