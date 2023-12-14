import numpy as np

def generate_matrices(p, K, M, matrix=None, row=0, result=None):
    if matrix is None:
        matrix = np.zeros((K, M), dtype=int)
    if result is None:
        result = []

    if row == K:
        result.append(matrix.copy())
        return result

    for j in range(M - p[row] + 1):
        if not any(matrix[row, j:j+p[row]]):
            matrix[row, j:j+p[row]] = 1
            generate_matrices(p, K, M, matrix, row + 1, result)
            matrix[row, j:j+p[row]] = 0

    return result
# te co nie zgadzają się z granicami wynocha
#ale granice sa pojebane to chuj wie co
def exclude_bad_matrixes():

    ...
# Example usage:
p = [2, 3, 4]
K = 3
M = 5

result_matrices = generate_matrices(p, K, M)
for matrix in result_matrices:
    print(matrix)

