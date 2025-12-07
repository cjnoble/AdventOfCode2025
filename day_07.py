import time

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Beam(object):
    def __init__(self, x, y, timelines = 1):
        self.x = x
        self.y = y
        self.start_pos = (x, y)
        self.active = True
        self.timelines = timelines

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def move(self, grid):
        self.y += 1

        new_pos = grid[self.y][self.x] if self.y < len(grid) and self.x < len(grid[self.y]) else None

        return new_pos

    def split(self, data):
        self.active = False

        new_beams = []

        if self.x > 0:
            new_beams.append(Beam(self.x-1, self.y, self.timelines))

        if self.x < len(data) - 1:
            new_beams.append(Beam(self.x+1, self.y, self.timelines))

        return new_beams

    def __hash__(self):
        return (self.x, self.y).__hash__()

def part_1(data):
    beams = set()
    grid = [[s for s in row] for row in data.copy()]

    for y, row in enumerate(data):
        for x, pos in enumerate(row):
            if pos == "S":
                beams.add(Beam(x, y))

    split_counter = 0
    loop_counter = 0

    while True:
        loop_counter += 1
        next_beams = set()
        for beam in beams:
            if beam.active:
                new_pos = beam.move(data)
                if new_pos == "^":
                    split_counter += 1
                    for new_beam in beam.split(data):
                        next_beams.add(new_beam)
                        grid[new_beam.y][new_beam.x] = "|"

                elif new_pos is None:
                    beam.active = False

                else:
                    grid[beam.y][beam.x] = "|"

        beams = beams.union(next_beams)
        beams = {beam for beam in beams if beam.active}

        for beam in beams:
            if beam.active:
                assert beam.y == loop_counter

        print(f"Loop counter: {loop_counter}, Total splits: {split_counter}, active beams count {sum(beam.active for beam in beams)}")

        # for row in grid:
        #     print("".join(row))

        if any([b.active for b in beams]):
            continue
        else:
            break

    return split_counter

def part_2(data):
    beams = []
    grid = [[s for s in row] for row in data.copy()]

    for y, row in enumerate(data):
        for x, pos in enumerate(row):
            if pos == "S":
                beams.append(Beam(x, y))

    loop_counter = 0

    while True:
        loop_counter += 1
        next_beams = []
        for beam in beams:
            if beam.active:
                new_pos = beam.move(data)
                if new_pos == "^":
                    for new_beam in beam.split(data):
                        next_beams.append(new_beam)
                        grid[new_beam.y][new_beam.x] = "|"

                elif new_pos is None:
                    beam.active = False

                else:
                    grid[beam.y][beam.x] = "|"

        beams.extend(next_beams)
        
        for beam in beams:
            for other_beam in beams:
                if beam is other_beam:
                    continue
                else:
                    if beam == other_beam and beam.active:
                        beam.timelines += other_beam.timelines
                        other_beam.active = False

        if any([b.active for b in beams]):
            pass
        else:
            break

        timeline_counter = sum(beam.timelines for beam in beams if beam.active)
        beams = [beam for beam in beams if beam.active]

        for beam in beams:
            if beam.active:
                assert beam.y == loop_counter

        print(f"Loop counter: {loop_counter}, Total timelines: {timeline_counter}, active beams count {sum(beam.active for beam in beams)}")

        # for row in grid:
        #     print("".join(row))

    return timeline_counter

if __name__ == "__main__":

    DAY = "07"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")