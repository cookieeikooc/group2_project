import sys
import time
import random
from enum import Enum
import pygame
from pygame.locals import *

# Constants
BLOCK_WIDTH = 10  # Adjust the width as necessary
BLOCK_HEIGHT = 10  # Adjust the height as necessary
SIZE = 20  # Adjust the block size as necessary
MINE_COUNT = 10  # Adjust the mine count as necessary
SCREEN_WIDTH = BLOCK_WIDTH * SIZE
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE

class BlockStatus(Enum):
    normal = 1  # not clicked
    opened = 2  # clicked
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
        self._status = BlockStatus.normal
        self.set_value(value)
    
    def __repr__(self):
        return str(self._value)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = 1 if value else 0
    
    @property
    def around_mine_count(self):
        return self._around_mine_count
    
    @around_mine_count.setter
    def around_mine_count(self, around_mine_count):
        self._around_mine_count = around_mine_count
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        self._status = value

class MineBlock:
    def __init__(self):
        self._block = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]
        self._set_mines()
    
    def _set_mines(self):
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1
    
    def getmine(self, x, y):
        return self._block[y][x]

    def open_mine(self, x, y):
        # touch bomb
        if self._block[y][x].value:
            self._block[y][x].status = BlockStatus.bomb
            return False
        self._block[y][x].status = BlockStatus.opened
        around = self._get_around(x, y)
        _sum = sum(1 for i, j in around if self._block[j][i].value)
        self._block[y][x].around_mine_count = _sum
        if _sum == 0:
            for i, j in around:
                if self._block[j][i].around_mine_count == -1:
                    self.open_mine(i, j)
        return True
    
    def double_mouse_button_down(self, x, y):
        if self._block[y][x].around_mine_count == 0:
            return True
        self._block[y][x].status = BlockStatus.double
        around = self._get_around(x, y)
        sumflag = sum(1 for i, j in around if self._block[j][i].status == BlockStatus.flag)
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
        for i, j in self._get_around(x, y):
            if self._block[j][i].status == BlockStatus.hint:
                self._block[j][i].status = BlockStatus.normal
    
    def _get_around(self, x, y):
        return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)
                for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]

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
    img_flag = pygame.transform.smoothscale(pygame.image.load('pictures/flag.bmp').convert(), (SIZE, SIZE))
    img_ask = pygame.transform.smoothscale(pygame.image.load('pictures/ask.bmp').convert(), (SIZE, SIZE))
    img_mine = pygame.transform.smoothscale(pygame.image.load('pictures/mine.bmp').convert(), (SIZE, SIZE))
    img_blood = pygame.transform.smoothscale(pygame.image.load('pictures/blood.bmp').convert(), (SIZE, SIZE))
    img_error = pygame.transform.smoothscale(pygame.image.load('pictures/error.bmp').convert(), (SIZE, SIZE))
    face_size = int(SIZE * 1.25)
    img_face_fail = pygame.transform.smoothscale(pygame.image.load('pictures/face_fail.bmp').convert(), (face_size, face_size))
    img_face_normal = pygame.transform.smoothscale(pygame.image.load('pictures/face_normal.bmp').convert(), (face_size, face_size))
    img_face_success = pygame.transform.smoothscale(pygame.image.load('resources/face_success.bmp').convert(), (face_size, face_size))
    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2
    
    bgcolor = (225, 225, 225)
    block = MineBlock()
    game_status = GameStatus.readied
    start_time = None
    elapsed_time = 0
    
    while True:
        screen.fill(bgcolor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                b1, b2, b3 = pygame.mouse.get_pressed()
                if game_status == GameStatus.started:
                    if b1 and b3:
                        mine = block.getmine(x, y)
                        if mine.status == BlockStatus.opened:
                            if not block.double_mouse_button_down(x, y):
                                game_status = GameStatus.over
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2

                if y < 0:
                    if face_pos_x <= mouse_x <= face_pos_x + face_size \
                            and face_pos_y <= mouse_y <= face_pos_y + face_size:
                        game_status = GameStatus.readied
                        block = MineBlock()
                        start_time = time.time()
                        elapsed_time = 0
                        continue

                if game_status == GameStatus.readied:
                    game_status = GameStatus.started
                    start_time = time.time()
                    elapsed_time = 0

                if game_status == GameStatus.started:
                    mine = block.getmine(x, y)
                    if b1 and not b3:
                        if mine.status == BlockStatus.normal:
                            if not block.open_mine(x, y):
                                game_status = GameStatus.over
                    elif not b1 and b3:
                        if mine.status == BlockStatus.normal:
                            mine.status = BlockStatus.flag
                        elif mine.status == BlockStatus.flag:
                            mine.status = BlockStatus.ask
                        elif mine.status == BlockStatus.ask:
                            mine.status = BlockStatus.normal
                    elif b1 and b3:
                        if mine.status == BlockStatus.double:
                            block.double_mouse_button_up(x, y)

        flag_count = 0
        opened_count = 0
        for row in block._block:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.status == BlockStatus.opened:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif mine.status == BlockStatus.double:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                elif mine.status == BlockStatus.bomb:
                    screen.blit(img_blood, pos)
                elif mine.status == BlockStatus.flag:
                    screen.blit(img_flag, pos)
                    flag_count += 1
                elif mine.status == BlockStatus.ask:
                    screen.blit(img_ask, pos)
                elif mine.status == BlockStatus.hint:
                    screen.blit(img_blank, pos)
                elif game_status == GameStatus.over and mine.value:
                    screen.blit(img_mine, pos)
                elif mine.value == 0 and mine.status == BlockStatus.flag:
                    screen.blit(img_error, pos)
                elif mine.status == BlockStatus.normal:
                    screen.blit(img_blank, pos)
        
        print_text(screen, font1, 30, (SIZE * 2 - fheight) // 2 - 2, '%02d' % (MINE_COUNT - flag_count), red)
        if game_status == GameStatus.started:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font1, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, red)
        
        if flag_count + opened_count == BLOCK_WIDTH * BLOCK_HEIGHT:
            game_status = GameStatus.win
        
        if game_status == GameStatus.over:
            screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        elif game_status == GameStatus.win:
            screen.blit(img_face_success, (face_pos_x, face_pos_y))
        else:
            screen.blit(img_face_normal, (face_pos_x, face_pos_y))
        
        pygame.display.update()

if __name__ == '__main__':
    main()

