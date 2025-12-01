from itertools import tee

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

def sign(x):

    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
    
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_data(self, grid):

        if self.in_bounds(grid):
            return grid[self.y][self.x]
        
        else:
            raise Exception("Not in bounds")

    def in_bounds(self, grid):
        if self.x < 0 or self.y < 0 :
            return False
        
        if self.y >= len(grid) or self.x >= len(grid[self.y]):
            return False
        
        return True

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))