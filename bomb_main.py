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

class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._around_mine_count = -1
        self._status = TileStatus.idle
        self.set_value(value)
    
    def __repr__(self):
        return str(self._value)
    
    @property               #read
    def x(self):
        return self._x
    
    @x.setter               #write
    def x(self, x):
        self._x = x
    
    @property               #read
    def y(self):
        return self._y
    
    @y.setter               #write
    def y(self, y):
        self._y = y
    
    @property               #read
    def value(self):
        return self._value
    
    @value.setter           #write
    def value(self, value):
        self._value = 1 if value else 0
    
    @property               #read
    def around_mine_count(self):
        return self._around_mine_count
    
