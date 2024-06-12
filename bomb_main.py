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
    
    @around_mine_count.setter   #write
    def around_mine_count(self, around_mine_count):
        self._around_mine_count = around_mine_count
    
    @property               #read
    def status(self):
        return self._status
    
    @status.setter          #write
    def status(self, value):
        self._status = value

class MineTile:
    def __init__(self):
        self._tile = [[Mine(i, j) for i in range(TILE_WIDTH)] for j in range(TILE_HIGHT)]
        self._set_mines()
    
    def _set_mines(self):
        for i in random.sample(range(TILE_WIDTH * TILE_HIGHT), MINE_COUNT):
            self._tile[i // TILE_WIDTH][i % TILE_WIDTH].value = 1
    
    def getmine(self, x, y):
        return self._tile[y][x]

    def open_mine(self, x, y):
        # touch bomb
        if self._tile[y][x].value:
            self._tile[y][x].status = TileStatus.bomb
            return False
        self._tile[y][x].status = TileStatus.clicked
        around = self._get_around(x, y)
        _sum = sum(1 for i, j in around if self._tile[j][i].value)
        self._tile[y][x].around_mine_count = _sum
        if _sum == 0:
            for i, j in around:
                if self._tile[j][i].around_mine_count == -1:
                    self.open_mine(i, j)
        return True
    
    def double_mouse_button_down(self, x, y):
        if self._tile[y][x].around_mine_count == 0:
            return True
        self._tile[y][x].status = TileStatus.double
        around = self._get_around(x, y)
        sumflag = sum(1 for i, j in around if self._tile[j][i].status == TileStatus.flag)
        result = True
        if sumflag == self._tile[y][x].around_mine_count:
            for i, j in around:
                if self._tile[j][i].status == TileStatus.idle:
                    if not self.open_mine(i, j):
                        result = False
        else:
            for i, j in around:
                if self._tile[j][i].status == TileStatus.idle:
                    self._tile[j][i].status = TileStatus.hint
        return result
    
    def double_mouse_button_up(self, x, y):
        self._tile[y][x].status = TileStatus.clicked
        for i, j in self._get_around(x, y):
            if self._tile[j][i].status == TileStatus.hint:
                self._tile[j][i].status = TileStatus.idle
    
    def _get_around(self, x, y):
        return [(i, j) for i in range(max(0, x - 1), min(TILE_WIDTH - 1, x + 1) + 1)
                for j in range(max(0, y - 1), min(TILE_HIGHT - 1, y + 1) + 1) if i != x or j != y]

class GameStatus(Enum):
    readied = 1,
    started = 2,
    over = 3,
    win = 4

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('扫雷')

    font1 = pygame.font.Font('No.019-Sounso-Quality-2.ttf', SIZE * 2)
    fwidth, fheight = font1.size('999')
    red = (200, 40, 40) 
    img_dict = {
        i: pygame.transform.smoothscale(pygame.image.load(f'pictures/{i}.bmp').convert(), (SIZE, SIZE)) for i in range(9)
    }
    
    img_blank = pygame.transform.smoothscale(pygame.image.load('pictures/blank.bmp').convert(), (SIZE, SIZE))
    img_start = pygame.transform.smoothscale(pygame.image.load('pictures/start.bmp').convert(), (SIZE, SIZE))
    img_ask = pygame.transform.smoothscale(pygame.image.load('pictures/ask.bmp').convert(), (SIZE, SIZE))
