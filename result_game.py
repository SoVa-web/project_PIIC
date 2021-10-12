from game_object.bullet.bullet import Bullet
import itertools
import random
from typing import List

import pygame

from config import WIDTH, HEIGHT

class Result:
    def __init__(self, screen, winner):
        self.screen = screen
        self.winner = winner

    def draw(self):
        self.screen.fill((130, 178, 137))
        font = pygame.font.Font(None, 25)
        text = font.render("Winner is " + self.winner + ". For continue press Enter ",True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.screen.blit(text, text_rect)
       