import time
import operator
from functools import reduce
from itertools import zip_longest

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def parse_input_part_1(data):

    data = zip_longest(*data, fillvalue=" ")

    current = []
    out = []
    row_out = []

    while True:
        try:
            next_item = next(data)

            if all([i == " " for i in next_item]):

                row_out = parse_row_part_1(current)
                out.append(row_out)
                row_out = []
                current = []
            
            else:
                current.append(next_item)       

        except StopIteration:
            row_out = parse_row_part_1(current)
            out.append(row_out)
            row_out = []
            current = []
            break
 
    return out

def parse_row_part_1(current):
    row_out = ["" for s in current[0][:-1]]

    for row in current:
        for i, num in enumerate(row):
            if num == " ":
                pass
            elif num == "+":
                op = operator.add
            elif num == "*":
                op = operator.mul
            else:
                row_out[i] += num
            
    row_out = [int(i) for i in row_out]
    row_out.append(op)

    return row_out

def parse_row_part_2(current):
    row_out = []

    for row in current:
        current_num = ""
        for i, num in enumerate(row):
            if num == " ":
                pass
            elif num == "+":
                op = operator.add
            elif num == "*":
                op = operator.mul
            else:
                current_num += num
            
        row_out.append(int(current_num))

    row_out.append(op)

    return row_out

def parse_input_part_2(data):

    data = zip_longest(*data, fillvalue=" ")

    current = []
    out = []

    while True:
        try:
            next_item = next(data)

            if all([i == " " for i in next_item]):

                row_out = parse_row_part_2(current)
                out.append(row_out)
                current = []
            
            else:
                current.append(next_item)       

        except StopIteration:
            row_out = parse_row_part_2(current)
            out.append(row_out)
            current = []
            break
 
    return out

def part_1(data):

    data = parse_input_part_1(data)
    total = 0

    for row in data:
        total += reduce(row[-1], row[:-1])

    return total

def part_2(data):

    data = parse_input_part_2(data)
    total = 0

    for row in data:
        total += reduce(row[-1], row[:-1])

    return total

if __name__ == "__main__":

    DAY = "06"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")