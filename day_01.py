import time

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def part_1(data):

    current = 50

    at_zero = 0

    for row in data:
        if row[0] == "R":
            turn = int(row[1:])
        else:
            turn = -int(row[1:])

        current  = (current + turn)%100

        if current == 0:
            at_zero += 1

    return at_zero

def part_2(data):

    current = 50

    at_zero = 0

    for row in data:
        direction  = row[0] 
        if direction == "R":
            turn = int(row[1:])
        else:
            turn = -int(row[1:])

        complete_turns = abs((current + turn)//100) + (-1 if current == 0  and direction == "L" else 0)
        current  = (current + turn)%100
        
        if current == 0 and direction == "L":
            at_zero += 1

        at_zero += complete_turns

        print(f"rotated {row}, to point at {current}. Number of complete turns {complete_turns}, total times pointing at zero {at_zero}")

    return at_zero

if __name__ == "__main__":

    DAY = "01"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")