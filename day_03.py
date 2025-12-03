import time

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def get_ith_digit(row, i, start):

    assert start <= len(row) - (i-1)

    if i == 1:
        sub_list = row[start:]
    else:
        sub_list = row[start:-(i-1)]

    i_th = max(sub_list)

    position = sub_list.index(i_th) + start

    return i_th, position

def part_1(data):

    sum_of_max_joltage = 0

    for row in data:
        row = [int(i) for i in row]

        first = max(row[:-1])
        i = row.index(first)

        second = max(row[i+1:])

        max_joltage = int(str(first) + str(second))

        sum_of_max_joltage += max_joltage

    return sum_of_max_joltage

def part_2(data):

    sum_of_max_joltage = 0

    DIGITS = 12

    for row in data:
        row = [int(i) for i in row]

        joltage = ""
        start_position = 0

        for i in range(DIGITS, 0, -1):
            jolt, start_position = get_ith_digit(row, i, start_position)
            joltage += str(jolt)
            start_position += 1

        max_joltage = int(joltage)

        sum_of_max_joltage += max_joltage

    return sum_of_max_joltage


if __name__ == "__main__":

    DAY = "03"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")