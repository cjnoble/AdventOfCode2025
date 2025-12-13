import time
import re

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Shape(object):
    def __init__(self, index, shape):
        self.index = index
        self.shape = shape
        self.area = sum(s == "#" for row in self.shape for s in row )

def part_1(data):

    shapes = {}
    working = 0

    for row in data:
        if re.match(r"\d:", row):
            shape_index = int(row[:-1])
            shape = []
        elif "#" in row or "." in row:
            shape.append(row)
        elif row == "":
            shapes[shape_index] = Shape(shape_index, shape)

        elif re.match(r"\d+x\d+:\s*.*", row):
            row = row.split(":")
            b, d = row[0].split("x")

            shape_list = row[1].split(" ")
            shape_list = [int(i) for i in shape_list if len(i)>0]

            area = int(b)*int(d)

            min_shape_area = sum(shapes[i].area*number for i, number in enumerate(shape_list))
            max_shape_area = sum(9*number for i, number in enumerate(shape_list))

            print(f"{area} {max_shape_area} {min_shape_area}")

            if area < min_shape_area:
                working += 0
            elif area >= max_shape_area:
                working += 1
            else:
                raise Exception("Undecidable")

    return working


def part_2(data):

    return

if __name__ == "__main__":

    DAY = "12"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")