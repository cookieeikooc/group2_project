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

