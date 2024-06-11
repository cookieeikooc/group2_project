class BlockStatus(Enum):
    normal = 1  # not click
    opened = 2  # click
    mine = 3    # bomb
    flag = 4    # bomb mark
    ask = 5   # question mark
    bomb = 6    # hit the bomb
    hint = 7    # neighbor has bomb
    double = 8  # being clicked twice


