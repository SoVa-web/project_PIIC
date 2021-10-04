import os
#from functools import cache

import pygame
from os import path

def load_icon(filename):
    icon_path = path.join(path.dirname(__file__), '..', 'data', 'icon', filename)
    return pygame.image.load(icon_path)
