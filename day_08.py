import time
import math as maths

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Point (object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dist = {}

    @classmethod
    def from_input(cls, input_row):
        x, y, z = input_row.split(",")
        return cls(int(x), int(y), int(z))
    
    def get_euclid_dist(self, other):
        return maths.sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)
    
    def __repr__(self):
        return repr((self.x, self.y, self.z))
    
    def __str__(self):
        return str((self.x, self.y, self.z))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def gen_distances(self, other_list):

        for other in other_list:
            if self is not other:
                if str(self) in other.dist:
                    self.dist[str(other)] = other.dist[str(self)]
                else:
                    self.dist[str(other)] = self.get_euclid_dist(other)


def part_1(data, COUNTER = 1000):

    points = [Point.from_input(row) for row in data]

    for point in points:
        point.gen_distances(points)
    
    point_pairs = []

    for point in points:
        for other_point in points:
            if point is not other_point:
                #if (other_point, point) not in point_pairs:
                point_pairs.append((point, other_point)) 

    point_pairs.sort(key= lambda x: x[0].dist[str(x[1])])
    point_pairs = [p for i, p in enumerate(point_pairs) if i%2 == 1]

    circuits = []

    for i in range(COUNTER):
        circuit_ref = None
        p1, p2 = point_pairs[i]

        if p2 == Point(984, 92, 344):
            print("Hi")

        for circuit_i, circuit in enumerate(circuits):
            if p1 in circuit:
                if circuit_ref:
                    circuits[circuit_ref] = circuits[circuit_ref].union(circuit)
                    circuits[circuit_i] = circuits[circuit_ref].union(circuit)
                else:
                    circuit.add(p2)
                    circuit_ref = circuit_i
            if p2 in circuit:
                if circuit_ref:
                    circuits[circuit_ref] = circuits[circuit_ref].union(circuit)
                    circuits[circuit_i] = circuits[circuit_ref].union(circuit)
                else:
                    circuit.add(p1)
                    circuit_ref = circuit_i

        if circuit_ref is None:
            circuits.append({p1, p2})

        new_circuits = []
        for circuit in circuits:
            if circuit not in new_circuits:
                new_circuits.append(circuit)

        circuits = new_circuits

    circuits.sort(key= lambda x: len(x), reverse=True)

    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])

def part_2(data):

    points = [Point.from_input(row) for row in data]

    for point in points:
        point.gen_distances(points)
    
    point_pairs = []

    for point in points:
        for other_point in points:
            if point is not other_point:
                #if (other_point, point) not in point_pairs:
                point_pairs.append((point, other_point)) 

    point_pairs.sort(key= lambda x: x[0].dist[str(x[1])])
    point_pairs = [p for i, p in enumerate(point_pairs) if i%2 == 1]

    circuits = []
    counter = 0

    while counter < len(point_pairs):
        circuit_ref = None
        p1, p2 = point_pairs[counter]

        if counter == 28:
            print("Hi")

        for circuit_i, circuit in enumerate(circuits):
            if p1 in circuit:
                if circuit_ref:
                    circuits[circuit_ref] = circuits[circuit_ref].union(circuit)
                    circuits[circuit_i] = circuits[circuit_ref].union(circuit)
                else:
                    circuit.add(p2)
                    circuit_ref = circuit_i
                    p_ref = (p1, p2)
            if p2 in circuit:
                if circuit_ref:
                    circuits[circuit_ref] = circuits[circuit_ref].union(circuit)
                    circuits[circuit_i] = circuits[circuit_ref].union(circuit)
                else:
                    circuit.add(p1)
                    circuit_ref = circuit_i
                    p_ref = (p1, p2)

        if circuit_ref is None:
            circuits.append({p1, p2})

        seen = set()
        new_circuits = []

        for circuit in circuits:
            f = frozenset(circuit)
            if f not in seen:
                seen.add(f)
                new_circuits.append(circuit)

        circuits = new_circuits

        if len(circuits[0]) == len(points):
            break

        counter += 1

    circuits.sort(key= lambda x: len(x), reverse=True)

    return p_ref[0].x * p_ref[1].x

if __name__ == "__main__":

    DAY = "08"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")