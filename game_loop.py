import pygame as pygame

import config
from config import WIDTH, HEIGHT, FPS
from game_object.field import Field

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Танчики")
pygame.display.set_icon(pygame.image.load('data/icon/gamelogo.png'))


class GameLoop:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.field = Field(config.FIELD_W_SIZE, config.FIELD_H_SIZE)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                for player in self.field.players:
                    player.key_processor.process_key_down_event(event)

            if event.type == pygame.KEYUP:
                for player in self.field.players:
                    player.key_processor.process_key_up_event(event)

    def start(self):
        self.is_running = True
        frame = 0

        while self.is_running:
            frame += 1
            self.clock.tick(FPS)
            self.process_events()
            self.field.draw(screen)
            if frame == config.MOVE_EVERY_NTH_FRAME:
                for player in self.field.players:
                    player.move()
                    player.shot()
                frame = 0
            self.field.sprites.update()
            self.field.sprites.draw(screen)
            pygame.display.flip()
