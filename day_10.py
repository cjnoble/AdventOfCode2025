import time
import numpy as np
import re

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def part_1(data):

    for row in data:

        row = row.split(" ")

        target_vector = []

        for i in row[0]:
            if i == "#":         
                target_vector.append(1)
            elif i == ".":
                target_vector.append(0)


        buttons = [[int(n) for n in re.findall(r"\d+", s)] for s in row[1:-1]]

        M = [[0 for i in range(len(target_vector))] for j in range(len(buttons))]

        for i, button in enumerate(buttons):
            for b in button:
                M[i][b] = 1

        target_vector = np.array(target_vector)
        M = np.array(M)

        print(f"V = {target_vector}")
        print(f"M = {M}")

        solution = np.linalg.lstsq(M.T, target_vector)

    return

def part_2(data):

    return

if __name__ == "__main__":

    DAY = "10"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")