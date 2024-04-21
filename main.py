import time
from utils import *
from test import *


def main(args=None):

    file = "log.txt"
    upper_bound = 20

    n=8
    k=4
    cellules,verticaux,horizontaux=generateRandomInstances(n,k)
    
    # n=8
    # k=3
    # cellules,verticaux,horizontaux=np.asarray(test_cellules),np.asarray(test_verticaux),np.asarray(test_horizontaux)
    
    # n=4
    # k=2
    # cellules,verticaux,horizontaux=np.asarray(test_cellules2),np.asarray(test_verticaux2),np.asarray(test_horizontaux2)

    # n, k, cellules, verticaux, horizontaux = generate_log_instance(file)
    
    # showgrid(n,cellules,verticaux,horizontaux)

    log_map(cellules,verticaux,horizontaux, file)

    position_cible = None
    position_robots = np.zeros(k, dtype=tuple)

    for i in range(len(cellules)):
        for j in range(len(cellules[i])):
            if cellules[i][j]==-1:
                position_cible=(i,j)
            elif cellules[i][j]>0:
                position_robots[cellules[i][j]-1] = (i,j)

    print("\nPositions initial des robots:", position_robots)
    print("Position de la cible:", position_cible)

    # position_robots[0] = move_line(position_robots[0], cellules, verticaux, horizontaux, "RIGHT")
    # showgrid(n,cellules,verticaux,horizontaux)
    
    start = time.time()
    shortest_path = deep_dive(cellules, verticaux, horizontaux, position_robots[0], position_cible, upper_bound)
    end = time.time()
    print(f"\nTime for deep dive: {end-start:.3}ms")
    if shortest_path <= upper_bound:
        print("Shortest path found with deep dive:", shortest_path)
    else:
        print(f"Shortest path not found with deep dive and an upper bound of {upper_bound}.")

    if shortest_path <= 6:
        start = time.time()
        shortest_multi_path = multi_dive(cellules, verticaux, horizontaux, position_robots, position_cible, shortest_path)
        end = time.time()
        print(f"\nTime for multi dive: {end-start:.3}ms")
        if shortest_multi_path <= upper_bound:
            print("Shortest path found with multi dive:", shortest_multi_path)
        else:
            print(f"Shortest path not found with multi dive and an upper bound of {upper_bound}.")

    h1=heuristic1(cellules)
    print("\nh1:")
    print(h1)

    h2 = heuristic2(cellules, verticaux, horizontaux)
    print("\nh2:")
    print(h2)

    if shortest_path <= upper_bound:
        start = time.time()
        path_h1 = a_star_search(position_robots[0], position_cible, 1, cellules, verticaux, horizontaux)
        end = time.time()
        print(f"\nTime for A*: {end-start:.3}ms")
        print("\nPath found with A* and h1:", path_h1)
        print("size:", len(path_h1) - 1)

        start = time.time()
        path_h2 = a_star_search(position_robots[0], position_cible, 2, cellules, verticaux, horizontaux)
        end = time.time()
        print(f"\nTime for A*: {end-start:.3}ms")
        print("\nPath found with A* and h2:", path_h2)
        print("size:", len(path_h2) - 1)

        log_path(path_h1, file)

        start = time.time()
        path = a_star_multi_robot(position_robots, position_cible, 1, cellules, verticaux, horizontaux, len(path_h1)-1)
        end = time.time()
        print(f"\nTime for multi A*: {end-start:.3}ms")
        print("\nPath found with multi A* and h1:", path)
        print("size:", len(path) - 1)

    showgrid(n,cellules,verticaux,horizontaux)

if __name__ == '__main__':
    main()