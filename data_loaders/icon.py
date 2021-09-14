import os
#from functools import cache

import pygame


def load_icon(filename):
    icon_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'icon', filename)
    return pygame.image.load(icon_path)
