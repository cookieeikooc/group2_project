import sys
import time
import random
from enum import Enum
import pygame
from pygame.locals import *

# Constants
TILE_WIDTH = 10  # Adjust the width as necessary
TILE_HIGHT = 10  # Adjust the height as necessary
SIZE = 20  # Adjust the tile size as necessary
MINE_COUNT = 10  # Adjust the mine count as necessary
SCREEN_WIDTH = TILE_WIDTH * SIZE
SCREEN_HEIGHT = (TILE_HIGHT + 2) * SIZE

class TileStatus(Enum):
    idle = 1  # not clicked
    clicked = 2  # clicked
    mine = 3    # bomb
    flag = 4    # bomb mark
    ask = 5     # question mark
    bomb = 6    # hit the bomb
    hint = 7    # neighbor has bomb
    double = 8  # being clicked twice   
