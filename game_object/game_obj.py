import pygame

from data_loaders import icon
from game_object import Vec2


class GameObjectSprite(pygame.sprite.Sprite):
    def __init__(self, pos: Vec2, sprite_filename: str):
        super().__init__()
        self.pos = pos
        self.image = self.scaled_image = self.orig_image = icon.load_icon(sprite_filename)
        self.rect = self.image.get_rect()
        self.cell_size = 0
        self.w_padding = 0
        self.h_padding = 0

    def scale_image(self):
        self.scaled_image = pygame.transform.scale(self.orig_image, (self.cell_size, self.cell_size))

    def update_field_pos(self, pos: Vec2):
        self.pos = pos

    def update(self):
        if self.scaled_image.get_rect() != (self.cell_size, self.cell_size):
            self.scale_image()
        self.rect.x = self.w_padding + (self.cell_size * (self.pos.x + 0.5)) - self.scaled_image.get_width() // 2
        self.rect.y = self.h_padding + (self.cell_size * (self.pos.y + 0.5)) - self.scaled_image.get_height() // 2
        self.image = self.scaled_image

    def set_field_size_info(self, cell_size, w_padding, h_padding):
        self.cell_size = cell_size
        self.w_padding = w_padding
        self.h_padding = h_padding
