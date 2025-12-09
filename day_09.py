import time
import math as maths
from collections import deque, defaultdict
from useful_code import pairwise_cycle

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

def ccw(A, B, C):
    """
    Check the orientation of the ordered triplet (A, B, C).
    Returns a value:
    > 0: Counter-clockwise
    < 0: Clockwise
    = 0: Collinear
    """
    # Cross product calculation: (C.y - A.y) * (B.x - A.x) - (B.y - A.y) * (C.x - A.x)
    val = (C.y - A.y) * (B.x - A.x) - (B.y - A.y) * (C.x - A.x)
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else -1 # Clockwise or Counter-clockwise

def segments_intersect(A, B, C, D):
    """
    Check if line segment AB intersects line segment CD.
    Endpoints are Point objects.
    """
    # General case: Find the four orientations needed for general and special cases
    o1 = ccw(A, B, C)
    o2 = ccw(A, B, D)
    o3 = ccw(C, D, A)
    o4 = ccw(C, D, B)

    # General case: Segments intersect if and only if all orientations are different
    # This means C and D are on different sides of AB, and A and B are on different sides of CD
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases: Handle collinear points (o1 or o2 or o3 or o4 is 0)
    
    # # A, B and C are collinear and C lies on segment AB
    # if o1 == 0 and (min(A.x, B.x) <= C.x <= max(A.x, B.x) and min(A.y, B.y) <= C.y <= max(A.y, B.y)):
    #     return True
    # # A, B and D are collinear and D lies on segment AB
    # if o2 == 0 and (min(A.x, B.x) <= D.x <= max(A.x, B.x) and min(A.y, B.y) <= D.y <= max(A.y, B.y)):
    #     return True
    # # C, D and A are collinear and A lies on segment CD
    # if o3 == 0 and (min(C.x, D.x) <= A.x <= max(C.x, D.x) and min(C.y, D.y) <= A.y <= max(C.y, D.y)):
    #     return True
    # # C, D and B are collinear and B lies on segment CD
    # if o4 == 0 and (min(C.x, D.x) <= B.x <= max(C.x, D.x) and min(C.y, D.y) <= B.y <= max(C.y, D.y)):
    #     return True

    return False # Doesn't fall in any of the above cases

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
    
    def is_allowed(self, other, other_points):

        for p1, p2 in pairwise_cycle(other_points):

            # Edge 1
            if segments_intersect(Point(self.x, self.y), Point(other.x, self.y), p1, p2):
                return False

            # Edge 2
            if segments_intersect(Point(self.x, other.y), Point(other.x, other.y), p1, p2):
                return False

            # Edge 3
            if segments_intersect(Point(self.x, self.y), Point(self.x, other.y), p1, p2):
                return False

            # Edge 4
            if segments_intersect(Point(other.x, self.y), Point(other.x, other.y), p1, p2):
                return False

        return True

    def is_allowed_1(self, other, all_points):

        # Get all points on edges - but not the corners

        # Edge 1
        y = self.y
        for x in edge_range(self.x, other.x):
            point = str(Point(x, y))
            if point in all_points:
                if all_points[point].is_concave:
                    return False

        # Edge 2
        y = other.y
        for x in edge_range(self.x, other.x):
            point = str(Point(x, y))
            if point in all_points:
                if all_points[point].is_concave:
                    return False

        # Edge 3
        x = self.x
        for y in edge_range(self.y, other.y):
            point = str(Point(x, y))
            if point in all_points:
                if all_points[point].is_concave:
                    return False
        # Edge 4
        x = other.x
        for y in edge_range(self.y, other.y):
            point = str(Point(x, y))
            if point in all_points:
                if all_points[point].is_concave:
                    return False

        return True

# def part_1_2(data):

#     points = [Point.from_input(row) for row in data]

#     points_xmap = defaultdict(list)
#     points_ymap = defaultdict(list)

#     for p in points:
#         points_xmap[p.x].append(p)
#         points_ymap[p.y].append(p)

#     lim_x_max = max(points_xmap.keys())
#     lim_x_min = min(points_xmap.keys())
#     lim_y_max = max(points_ymap.keys())
#     lim_y_min = min(points_ymap.keys())

#     range_x = lim_x_max - lim_x_min
#     range_y = lim_y_max - lim_y_min

#     counter = 0
#     max_area = 0

#     y_min_test_points = list()
#     y_max_test_points = list()
#     x_min_test_points = list()
#     x_max_test_points = list()

#     while True:

#         min_x = lim_x_min + counter
#         min_y = lim_y_min + counter
#         max_x = lim_x_max - counter
#         max_y = lim_y_max - counter

#         # lhs_column = [[row[min_x]] for y, row in enumerate(data) if y >= min_y and y<max_y]
#         # rhs_column = [[row[max_x]] for y, row in enumerate(data) if y >= min_y and y<max_y]
        
#         # top_row = data[min_y][min_x:max_x]
#         # bottom_row = data[max_y-1][min_x:max_x]

#         y_min_test_points.extend(points_ymap[min_y])
#         y_max_test_points.extend(points_ymap[max_y])
#         x_min_test_points.extend(points_xmap[min_x])
#         x_max_test_points.extend(points_xmap[max_x])

#         residual_area = (1 + abs(max_x - min_x))*(1 + abs(max_y-min_y))

#         for point_y, point_x in zip(y_min_test_points, x_max_test_points):
#             area = point_y.area(point_x)
#             if area > max_area:
#                 max_area = area

#         for point_y, point_x in zip(y_max_test_points, x_min_test_points):
#             area = point_y.area(point_x)
#             if area > max_area:
#                 max_area = area

#         for point_y, point_x in zip(y_min_test_points, y_max_test_points):
#             area = point_y.area(point_x)
#             if area > max_area:
#                 max_area = area

#         for point_y, point_x in zip(x_max_test_points, x_min_test_points):
#             area = point_y.area(point_x)
#             if area > max_area:
#                 max_area = area

#         for point_y, point_x in zip(y_min_test_points, x_min_test_points):
#             area = point_y.area(point_x)
#             if area > max_area:
#                 max_area = area

#         for point_y, point_x in zip(y_max_test_points, x_max_test_points):
#             area = point_y.area(point_x)
#             if area > max_area:
#                 max_area = area

#         # for point_y, point_x in zip(y_min_test_points, y_min_test_points):
#         #     area = point_y.area(point_x)
#         #     if area > max_area:
#         #         max_area = area

#         # for point_y, point_x in zip(x_max_test_points, x_max_test_points):
#         #     area = point_y.area(point_x)
#         #     if area > max_area:
#         #         max_area = area

#         # for point_y, point_x in zip(y_max_test_points, y_max_test_points):
#         #     area = point_y.area(point_x)
#         #     if area > max_area:
#         #         max_area = area

#         # for point_y, point_x in zip(x_min_test_points, x_min_test_points):
#         #     area = point_y.area(point_x)
#         #     if area > max_area:
#         #         max_area = area

#         # if max_area > residual_area:
#         #     break

#         if counter > range_x and counter > range_y:
#             break

#         counter += 1

#     return max_area

def part_1(data):

    points = [Point.from_input(row) for row in data]

    max_area = 0

    for p1 in points:
        for p2 in points:
            area = p1.area(p2)
            if area > max_area:
                max_area = area

    return max_area

def part_2_2(data):

    points = [Point.from_input(row) for row in data]
    points_dict = {str(point): point for point in points}

    for i in range(len(points)):
        point = points[i]
        previous = points[i-1]
        next = points[(i+1)%len(points)]

        #Assume we are going clockwise

        if previous.y == point.y:
            # Same row
            if previous.x < point.x and next.y < point.y:
                point.is_concave = True
            elif previous.x > point.x and next.y < point.y:
                point.is_concave = True

        else:
            # same column
            if previous.y < point.y and next.x > point.x:
                point.is_concave = True
            elif previous.y > point.y and next.x < point.x:
                point.is_concave = True

    
    max_area = 0

    for i, p1 in enumerate(points):
        print(f"On p1 number {i} out of {len(points)}")
        for j, p2 in enumerate(points):
            area = p1.area(p2)
            if area > max_area:
                if p1.is_allowed(p2, points_dict):
                    max_area = area

    return max_area

def part_2(data):

    points = [Point.from_input(row) for row in data]
    points_dict = {str(point): point for point in points}

    for i in range(len(points)):
        point = points[i]
        previous = points[i-1]
        next = points[(i+1)%len(points)]

        #Assume we are going clockwise

        if previous.y == point.y:
            # Same row
            if previous.x < point.x and next.y < point.y:
                point.is_concave = True
            elif previous.x > point.x and next.y < point.y:
                point.is_concave = True

        else:
            # same column
            if previous.y < point.y and next.x > point.x:
                point.is_concave = True
            elif previous.y > point.y and next.x < point.x:
                point.is_concave = True

    
    max_area = 0

    for i, p1 in enumerate(points):
        print(f"On p1 number {i} out of {len(points)}")
        for j, p2 in enumerate(points):
            area = p1.area(p2)
            if area > max_area:
                if p1.is_allowed(p2, points):
                    max_area = area

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