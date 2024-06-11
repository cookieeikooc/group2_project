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

    font1 = pygame.font.Font('resources/a.TTF', SIZE * 2)
    fwidth, fheight = font1.size('999')
    red = (200, 40, 40)
    img0 = pygame.image.load('resources/0.bmp').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('resources/1.bmp').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('resources/2.bmp').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('resources/3.bmp').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('resources/4.bmp').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('resources/5.bmp').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('resources/6.bmp').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('resources/7.bmp').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('resources/8.bmp').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('resources/blank.bmp').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('resources/flag.bmp').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
    img_ask = pygame.image.load('resources/ask.bmp').convert()
    img_ask = pygame.transform.smoothscale(img_ask, (SIZE, SIZE))
    img_mine = pygame.image.load('resources/mine.bmp').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('resources/blood.bmp').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('resources/error.bmp').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))
    face_size = int(SIZE * 1.25)
    img_face_fail = pygame.image.load('resources/face_fail.bmp').convert()
    img_face_fail = pygame.transform.smoothscale(img_face_fail, (face_size, face_size))
    img_face_normal = pygame.image.load('resources/face_normal.bmp').convert()
    img_face_normal = pygame.transform.smoothscale(img_face_normal, (face_size, face_size))
    img_face_success = pygame.image.load('resources/face_success.bmp').convert()
    img_face_success = pygame.transform.smoothscale(img_face_success, (face_size, face_size))
    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2
    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8
    }
    bgcolor = (225, 225, 225)
    block = MineBlock()
    game_status = GameStatus.readied
    start_time = None
    elapsed_time = 0    
