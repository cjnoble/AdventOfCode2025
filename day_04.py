import time

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data



def get_paper_roll(data, i ,j):

    if (i < 0 or j < 0):
        return False
    elif j>=len(data) or i>=len(data[j]):
            return False
    else:
         return data[j][i] == "@"


def count_adjacent_paper_rolls(data, x, y):

    paper_rolls = 0

    for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
         
        paper_rolls += 1 if get_paper_roll(data, x+i, y+j) else 0

    return paper_rolls

def part_1(data:list):

    accessible_paper = 0
    out_grid = data.copy()

    for y in range (len(data)):
        for x in range(len(data[y])):

            if data[y][x] == "@":
                print(count_adjacent_paper_rolls(data, x, y))
                if count_adjacent_paper_rolls(data, x, y) < 4:
                    out_grid[y] = out_grid[y][:x] + "x" + out_grid[y][x+1:] 
                    accessible_paper += 1

    for row in out_grid:
        print(row)

    return accessible_paper


def part_2(data):

    total_accessible_paper = 0
    next_grid = data.copy()


    while True:
        accessible_paper = 0
        data = next_grid

        next_grid = data.copy()

        for y in range (len(data)):
            for x in range(len(data[y])):

                if data[y][x] == "@":
                    #print(count_adjacent_paper_rolls(data, x, y))
                    if count_adjacent_paper_rolls(data, x, y) < 4:
                        next_grid[y] = next_grid[y][:x] + "." + next_grid[y][x+1:] 
                        accessible_paper += 1

        if accessible_paper == 0:
            break
        else:
            total_accessible_paper += accessible_paper

    return total_accessible_paper

if __name__ == "__main__":

    DAY = "04"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")