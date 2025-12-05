import time
from functools import reduce

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data



class FreshRange(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_fresh(self, ingredient):

        if ingredient < self.start:
            return False
        elif ingredient > self.end:
            return False
        else:
            return True
        
    @classmethod
    def from_string(cls, string):
        range = string.split("-")

        return cls(int(range[0]), int(range[1]))

    def len_range(self):

        return 1 + self.end - self.start
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
        
    def __repr__(self):
        return f"{self.start}, {self.end}"

    def __str__(self):
        return f"{self.start}, {self.end}"

def process_data(data):

    fresh_ranges = []
    ingredients = []

    for row in data:
        if "-" in row:
            fresh_ranges.append(FreshRange.from_string(row))
        elif row != "":
            ingredients.append(int(row))

    return fresh_ranges, ingredients

def part_1(data):

    fresh_ranges, ingredients = process_data(data)
    fresh = 0

    for ingredient in ingredients:
        
        if reduce(lambda x, y: x or y, [fresh_range.is_fresh(ingredient) for fresh_range in fresh_ranges]):
            fresh += 1

    return fresh

def part_2(data):

    fresh_ranges, _ = process_data(data)

    fresh_ranges.sort(key= lambda x: x.start)

    for range_1 in fresh_ranges:

        for range_2 in fresh_ranges:

            # Check for overlap
            if range_1.start <= range_2.start and range_2.start <= range_1.end:
                range_2.start = range_1.start

                range_1.end = max(range_1.end, range_2.end)
                range_2.end = range_1.end 

    ranges_considered = []
    count = 0

    for range_1 in fresh_ranges:
        if len(ranges_considered) ==0 or not reduce(lambda x, y: x or y, [range_1 == range for range in ranges_considered]):
            ranges_considered.append(range_1)
            print(range_1)
            count += range_1.len_range()
    return count

if __name__ == "__main__":

    DAY = "05"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")