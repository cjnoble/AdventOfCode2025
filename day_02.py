import time
import math as maths
from functools import cache

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def get_ranges(data):

    ranges = data[0].split(",")
    out = []

    for rang in ranges:
        rang = rang.split("-")
        start = int(rang[0])
        end = int(rang[1]) + 1
        out.append((start, end))

    return out

def split_ID(ID, chuncks=2):

    IDstring = str(ID)

    chunk_size = len(IDstring)//chuncks

    return [IDstring[i*chunk_size:(i+1)*chunk_size] for i in range(chuncks)]

@cache
def get_factors(n):

    factors = []

    for test_factor in range(2, int(maths.sqrt(n))):
        if n % test_factor == 0:
            factors.append(test_factor)

    return factors

def part_1(data):

    ranges = get_ranges(data)
    invalidIDs = 0

    for IDrange in ranges:
        for ID in range(IDrange[0], IDrange[1]):
            
            if len(str(ID))%2 == 0:

                IDstart, IDend = split_ID(ID)

                if IDstart == IDend:
                    invalidIDs += ID

    return invalidIDs

def part_2(data):

    ranges = get_ranges(data)
    invalidIDs = 0

    for IDrange in ranges:
        for ID in range(IDrange[0], IDrange[1]):

            n = len(str(ID))

            factors = get_factors(n)

            for factor in factors:
            
                if n%factor == 0:

                    IDstart, IDend = split_ID(ID)

                    if IDstart == IDend:
                        invalidIDs += ID
                        break

    return invalidIDs

if __name__ == "__main__":

    DAY = "02"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")