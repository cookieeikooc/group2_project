class BlockStatus(Enum):
    normal = 1  # not click
    opened = 2  # click
    mine = 3    # bomb
    flag = 4    # bomb mark
    ask = 5   # question mark
    bomb = 6    # hit the bomb
    hint = 7    # neighbor has bomb
    double = 8  # being clicked twice
class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._around_mine_count = -1
        self._status = BlockStatus.normal
        self.set_value(value)
    def __repr__(self):
        return str(self._value)
    def get_x(self):
        return self._x
    def set_x(self, x):
        self._x = x
    x = property(fget=get_x, fset=set_x)
    def get_y(self):
        return self._y
    def set_y(self, y):
        self._y = y
    y = property(fget=get_y, fset=set_y)
    def get_value(self):
        return self._value
    def set_value(self, value):
        if value:
            self._value = 1
        else:
            self._value = 0
    value = property(fget=get_value, fset=set_value, doc='0:非地雷 1:雷')
    def get_around_mine_count(self):
        return self._around_mine_count
    def set_around_mine_count(self, around_mine_count):
        self._around_mine_count = around_mine_count
    around_mine_count = property(fget=get_around_mine_count, fset=set_around_mine_count, doc='四周地雷数量')
    def get_status(self):
        return self._status
    def set_status(self, value):
        self._status = value
    status = property(fget=get_status, fset=set_status, doc='BlockStatus')
class MineBlock:
    def __init__(self):
        self._block = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]
        #set bomb
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1
class MineBlock:
　　def open_mine(self, x, y):
        # touch bomb
        if self._block[y][x].value:
            self._block[y][x].status = BlockStatus.bomb
            return False
        self._block[y][x].status = BlockStatus.opened
        around = _get_around(x, y)
        _sum = 0
        for i, j in around:
            if self._block[j][i].value:
                _sum += 1
        self._block[y][x].around_mine_count = _sum
        if _sum == 0:
            for i, j in around:
                if self._block[j][i].around_mine_count == -1:
                    self.open_mine(i, j)
        return True
def _get_around(x, y):
    return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]
class MineBlock:
    def double_mouse_button_down(self, x, y):
        if self._block[y][x].around_mine_count == 0:
            return True
        self._block[y][x].status = BlockStatus.double
        around = _get_around(x, y)
        sumflag = 0 # num of marked bomb
        for i, j in _get_around(x, y):
            if self._block[j][i].status == BlockStatus.flag:
                sumflag += 1
        result = True
        if sumflag == self._block[y][x].around_mine_count:
            for i, j in around:
                if self._block[j][i].status == BlockStatus.normal:
                    if not self.open_mine(i, j):
                        result = False
        else:
            for i, j in around:
                if self._block[j][i].status == BlockStatus.normal:
                    self._block[j][i].status = BlockStatus.hint
        return result
    def double_mouse_button_up(self, x, y):
        self._block[y][x].status = BlockStatus.opened
        for i, j in _get_around(x, y):
            if self._block[j][i].status == BlockStatus.hint:
                self._block[j][i].status = BlockStatus.normal
import sys
import time
from enum import Enum
import pygame
from pygame.locals import *
from mineblock import *
SCREEN_WIDTH = BLOCK_WIDTH * SIZE
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE
