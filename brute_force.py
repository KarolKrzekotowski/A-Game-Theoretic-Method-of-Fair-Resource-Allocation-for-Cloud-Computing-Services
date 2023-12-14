from nowy import GameTheory
from generator_a import generate_matrices
import sys
gra = GameTheory(
    3,
    5,
    [2, 3, 4],
    [1, 1.2, 1.5, 1.8, 2],
    [[6, 5, 4, 3.5, 3], [5, 4.2, 3.6, 3, 2.8], [4, 3.5, 3.2, 2.8, 2.4]],
    50,
    50,
    0.5,
    0.5,
    1,
)
B = [
    [0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1]
]
list_B = generate_matrices(B,[2, 3, 4],)


list_for_results = []
for i in list_B:
    good = gra.Funkcja_celu_Z(i)
    if good[2]:
        list_for_results.append((good[0],good[1]))
    
max = sys.maxsize
best_allocation = []
for good in list_for_results:
    if good[0]< max:
        max = good[0]
        best_allocation = good[1]
    
        
print(max, best_allocation)
# print(len(list_B))


# B = [[0, 0, 1, 0, 1], [0, 1, 1, 1, 0], [1, 1, 0, 1, 1]]
# print(gra.Funkcja_celu_Z(B))
