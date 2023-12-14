import numpy as np
from itertools import combinations 
def generate_matrices(rows, constraints):
    if not rows or not constraints:
        return []

    def generate_helper(row_index, current_matrix):
        if row_index == len(rows):
            result.append(current_matrix.copy())
            return

        for combination in combinations(range(len(current_matrix[row_index])), constraints[row_index]):
            next_matrix = [row[:] for row in current_matrix]
            for index in combination:
                next_matrix[row_index][index] = 1
            generate_helper(row_index + 1, next_matrix)

    result = []
    generate_helper(0, [[0] * len(rows[0]) for _ in range(len(rows))])
    return result



# Example usage:
# binary_rows = [[0, 0, 1, 0, 1], [0, 1, 1, 1, 0], [1, 1, 0, 1, 1]]
# constraints = [2, 3, 4]
# matrices = generate_matrices(binary_rows, constraints)

