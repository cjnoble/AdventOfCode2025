import time
import math as maths
from collections import deque, defaultdict
from useful_code import pairwise_cycle
import matplotlib.pyplot as plt

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

def plot_polygon_and_rectangle(points, rect_points):
    # Polygon
    poly_x = [p.x for p in points] + [points[0].x]  # close the polygon
    poly_y = [p.y for p in points] + [points[0].y]

    plt.plot(poly_x, poly_y, 'b-o', label='Polygon')

    # Rectangle
    if rect_points:
        p1, p2 = rect_points
        min_x = min(p1.x, p2.x)
        max_x = max(p1.x, p2.x)
        min_y = min(p1.y, p2.y)
        max_y = max(p1.y, p2.y)

        rect_x = [min_x, max_x, max_x, min_x, min_x]
        rect_y = [min_y, min_y, max_y, max_y, min_y]

        plt.plot(rect_x, rect_y, 'r-', linewidth=2, label='Max Rectangle')
        plt.fill(rect_x, rect_y, color='red', alpha=0.2)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()

def classify_polygon_edges(points):
    """Return lists of axis-aligned horizontal and vertical edges."""
    horiz = []
    vert = []

    for p1, p2 in pairwise_cycle(points):
        if p1.y == p2.y:
            # horizontal edge
            if p1.x <= p2.x:
                horiz.append((p1, p2))
            else:
                horiz.append((p2, p1))
        else:
            # vertical edge
            if p1.y <= p2.y:
                vert.append((p1, p2))
            else:
                vert.append((p2, p1))

    return horiz, vert


def is_concave_vertex(prev, point, nxt):
    """
    Determine whether a vertex is concave.
    For axis-aligned polygons, this reduces to a simple 2D cross product sign.
    """
    dx1 = point.x - prev.x
    dy1 = point.y - prev.y
    dx2 = nxt.x - point.x
    dy2 = nxt.y - point.y

    # Orthogonal edges only: (dx1,dy1) and (dx2,dy2)
    # Cross product z-component: dx1*dy2 - dy1*dx2
    cross = dx1 * dy2 - dy1 * dx2

    # For clockwise ordering, concave is where cross > 0.
    return cross > 0


def rectangle_edges(p1, p2):
    """
    Return the four axis-aligned rectangle edges between p1 and p2
    in canonical min/max form.
    """
    min_x = min(p1.x, p2.x)
    max_x = max(p1.x, p2.x)
    min_y = min(p1.y, p2.y)
    max_y = max(p1.y, p2.y)

    bl = Point(min_x, min_y)
    br = Point(max_x, min_y)
    tr = Point(max_x, max_y)
    tl = Point(min_x, max_y)

    # Each is a pair (p1, p2)
    # Horizontal bottom, top
    bottom = (bl, br)
    top = (tl, tr)

    # Vertical left, right
    left = (bl, tl)
    right = (br, tr)

    return bottom, top, left, right


def horizontal_vertical_intersect(h, v):
    """
    Fast intersection test:
    h = ((hx1, hy), (hx2, hy)) horizontal edge
    v = ((vx, vy1), (vx, vy2)) vertical edge
    """
    (h1, h2) = h
    (v1, v2) = v

    return (
        min(h1.x, h2.x) < v1.x < max(h1.x, h2.x) and
        min(v1.y, v2.y) < h1.y < max(v1.y, v2.y)
    )


def rectangle_intersects_polygon(p1, p2, horiz_edges, vert_edges):
    """
    Check whether rectangle defined by p1 and p2 intersects polygon edges.
    Using only axis-aligned HV or VH comparisons.
    """
    bottom, top, left, right = rectangle_edges(p1, p2)

    # Check horizontal rectangle edges against vertical polygon edges
    for h_edge in (bottom, top):
        for v_edge in vert_edges:
            if horizontal_vertical_intersect(h_edge, v_edge):
                return True

    # Check vertical rectangle edges against horizontal polygon edges
    for v_edge in (left, right):
        for h_edge in horiz_edges:
            if horizontal_vertical_intersect(h_edge, v_edge):
                return True

    return False


def concave_point_on_rectangle_boundary(p, p1, p2):
    """
    A concave vertex invalidates the rectangle only when lying exactly on rectangle boundary.
    """
    min_x = min(p1.x, p2.x)
    max_x = max(p1.x, p2.x)
    min_y = min(p1.y, p2.y)
    max_y = max(p1.y, p2.y)

    # On left or right boundary
    if p.x == min_x or p.x == max_x:
        if min_y < p.y < max_y:
            return True

    # On top or bottom boundary
    if p.y == min_y or p.y == max_y:
        if min_x < p.x < max_x:
            return True

    return False

def edge_range(start, stop):

    if start > stop:
        return range(stop + 1, start)
    else:
        return range(start + 1, stop)

class Point (object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_concave = False

    @classmethod
    def from_input(cls, input_row):
        x, y = input_row.split(",")
        return cls(int(x), int(y))
        
    def __repr__(self):
        return repr((self.x, self.y))
    
    def __str__(self):
        return str((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def area(self, other):
        return (1+ abs(self.x - other.x)) * (1+ abs(self.y - other.y))
    

def part_1(data):

    points = [Point.from_input(row) for row in data]

    max_area = 0

    for p1 in points:
        for p2 in points:
            area = p1.area(p2)
            if area > max_area:
                max_area = area

    return max_area

def inside_rectangle(p1, p2, points):

    for point in points:
        if point != p1 and point != p2:

            if min(p1.x, p2.x) < point.x and max(p1.x, p2.x) > point.x and min(p1.y, p2.y) < point.y and max(p1.y, p2.y) > point.y:
                return True

    return False

def part_2(data):
    points = [Point.from_input(row) for row in data]
    N = len(points)

    # Determine concavity
    for i in range(N):
        prev = points[i - 1]
        point = points[i]
        nxt = points[(i + 1) % N]
        point.is_concave = is_concave_vertex(prev, point, nxt)

    # Pre-classify polygon edges
    horiz_edges, vert_edges = classify_polygon_edges(points)

    # Solve
    max_area = 0
    best_rect = None

    for i, p1 in enumerate(points):
        print(f"p1: {i+1}/{N}")

        for p2 in points:
            if p1 is p2:
                continue

            test_area = p1.area(p2)
            if test_area <= max_area:
                continue

            # Check rectangle vs polygon intersection
            if rectangle_intersects_polygon(p1, p2, horiz_edges, vert_edges):
                continue

            # Check no concave point lies on boundary
            boundary_ok = True
            for cp in points:
                if cp.is_concave and concave_point_on_rectangle_boundary(cp, p1, p2):
                    boundary_ok = False
                    break

            if not boundary_ok:
                continue

            if inside_rectangle(p1, p2, points):
                continue

            max_area = test_area
            best_rect = (p1, p2) 

    plot_polygon_and_rectangle(points, best_rect)

    return max_area

if __name__ == "__main__":

    DAY = "09"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")