import time
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
import re
from functools import reduce
from itertools import product
import concurrent.futures

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def part_1(data):

    solution_sum = 0

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
        M = np.array(M).T

        print(f"V = {target_vector}")
        print(f"M = {M}")

        # Augmented_matrix
        Aug = np.hstack((M, target_vector.reshape(-1, 1))) # reshape forces numpy to understand that this is a column vector
        
        #print(f"Aug = {Aug}")

        # Forward elimination
        current_row_index = 0
        for col_index in range(M.shape[1]):
            # Find the "pivot" in the column
            pivot = -1
            for row_index in range(current_row_index, M.shape[0]):
                row = Aug[row_index]
                val = row[col_index]
                if val == 1:
                    #This is the pivot
                    pivot = row_index
                    break
            
            if pivot == -1:
                # Free variable
                continue

            # Swap current row and pivot
            # Aug[[i, j]] = Aug[[j, i]]
            Aug[[current_row_index, pivot]] = Aug[[pivot, current_row_index]]

            # Eliminate below
            for r in range(current_row_index + 1, M.shape[0]):
                if Aug[r][col_index] == 1:
                    Aug[r] = Aug[r] ^ Aug[current_row_index]

            current_row_index += 1

        #print(f"Aug = {Aug}")

        # Look at each pivot
        pivot_cols = []
        for pivot_index in range(Aug.shape[0]):
            row = Aug[pivot_index, :Aug.shape[1]-1]
            ones = np.flatnonzero(row)
            if len(ones) > 0:
                pivot_cols.append(ones[0])

        print(f"Pivot columns {pivot_cols}")

        #Find free variables
        all_columns = set(range(Aug.shape[1]-1))
        free_vars = list(all_columns - set(pivot_cols))

        print(f"Free variables {free_vars}")
        number_free_variables = len(free_vars)
        print(f"Number of free variables {number_free_variables}")
        number_solutions = 2**number_free_variables
        print(f"Number of solutions {number_solutions}")

        # Find each solution
        solutions = []
        for combination in range(number_solutions):
            x_free = [(combination >> k) & 1 for k in range(number_free_variables)] #Extract each bit

            x = np.zeros(Aug.shape[1]-1,dtype=np.int64)
            x[free_vars] = x_free

            # Back substitution
            # From bottom row to top

            for row_index in range(len(pivot_cols)-1, -1, -1):

                row = Aug[row_index]
                pivot_col = pivot_cols[row_index]

                # Only columns to the right that have 1 in this row
                cols_to_xor = np.flatnonzero(row[pivot_col+1:-1]) + (pivot_col + 1)  # adjust indices
                known_values = x[cols_to_xor]

                rhs = Aug[row_index, Aug.shape[1]-1]

                x[pivot_col] = rhs ^ reduce(lambda x, y: x ^ y, known_values) if known_values.size > 0 else rhs

            print(x)
            solutions.append(x)

        solution_sum += min([sum(solution) for solution in solutions])

    return solution_sum


def solve_row_part_2(row):
    row = row.split(" ")

    target_vector = [int(n) for n in re.findall(r"\d+", row[-1])]

    buttons = [[int(n) for n in re.findall(r"\d+", s)] for s in row[1:-1]]

    M = np.zeros((len(target_vector), len(buttons)), dtype=int)
    for j, button in enumerate(buttons):
        for counter_idx in button:
            M[counter_idx, j] = 1  # button j affects counter_idx

    target_vector = np.array(target_vector)

    # Objective: minimize sum of x
    c = np.ones(M.shape[1])

    # Solve linear program
    # Linear equality constraints
    lc = LinearConstraint(M, target_vector, target_vector)

    # Solve integer problem
    assert M.shape[0] == target_vector.shape[0]
    bounds = Bounds(0, np.inf)  # x_i >= 0
    res = milp(c, constraints=[lc], bounds=bounds, integrality=np.ones_like(c))

    if not res.success:
        raise Exception("No integer solution found")

    # Check solution
    x_solution = np.round(res.x).astype(int)  # round to integer for safety
    if not np.allclose(M @ x_solution, target_vector, atol=1e-8):
        raise Exception("MILP solution does not satisfy target")

    print(x_solution)

    assert test_x_candidate(M, target_vector, x_solution ) != float('inf')

    return int(np.sum(x_solution))  # total number of button presses

def test_x_candidate(M, target_vector, x_candidate):
    print(f"Testing {x_candidate}")
    x_candidate = np.array(x_candidate)
    print("Starting")
    if np.array_equal(M @ x_candidate , target_vector):  # satisfies target
        print("End 1")
        return x_candidate.sum()
    else:
        print("End 2")
        return float('inf')


def part_2(data):
    
    solution_sum = 0

    solution_sum = sum(solve_row_part_2(row) for row in data)

    return solution_sum

if __name__ == "__main__":

    DAY = "10"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")