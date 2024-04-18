from utils import *
from test import *


def main(args=None):

    file = "log.txt"

    n=10
    k=4

    cellules,verticaux,horizontaux=generateRandomInstances(n,k)
    # cellules,verticaux,horizontaux=np.asarray(test_cellules),np.asarray(test_verticaux),np.asarray(test_horizontaux)
    # n=8
    # k=3
    # n, k, cellules, verticaux, horizontaux = generate_instance(file)
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

    shortest_path = deep_dive(cellules, verticaux, horizontaux, position_robots[0], position_cible, 15)
    print("\nShortest path found with deep dive:", shortest_path)

    if shortest_path <= 5:
        shortest_path = multi_dive(cellules, verticaux, horizontaux, position_robots, position_cible, shortest_path)
        print("Shortest path found with multi dive:", shortest_path)

    h1=heuristic1(cellules)
    print("\nh1:")
    print(h1)

    h2 = heuristic2(cellules, verticaux, horizontaux)
    print("\nh2:")
    print(h2)

    path = a_star_search(position_robots[0], position_cible, 1, cellules, verticaux, horizontaux)
    print("\nPath found with A* and h1:", path)
    print("size:", len(path) - 1)

    path = a_star_search(position_robots[0], position_cible, 2, cellules, verticaux, horizontaux)
    print("\nPath found with A* and h2:", path)
    print("size:", len(path) - 1)

    log_path(path, file)

    showgrid(n,cellules,verticaux,horizontaux)

if __name__ == '__main__':
    main()