import time
from utils import *
from test import *

def mean_time(n,k,ite):
    temps = np.zeros((5, ite))
    resultat= np.zeros((5, ite))

    i=0
    upper_bound=20
    while i<ite:
        print(f"iteration: {i}")
        cellules,verticaux,horizontaux=generateRandomInstances(n,k)
        position_cible = None
        position_robots = np.zeros(k, dtype=tuple)

        for r in range(k):
            r_x = np.where(cellules == r+1)[0][0]
            r_y = np.where(cellules == r+1)[1][0]
            position_robots[r] = (r_x,r_y)

        c_x = np.where(cellules == -1)[0][0]
        c_y = np.where(cellules == -1)[1][0]
        position_cible = (c_x,c_y)

        # ___DEEP_DIVE____
        start = time.time()
        deep_path = deep_dive(cellules, verticaux, horizontaux, position_robots[0], position_cible, upper_bound)
        end = time.time()

        if deep_path > upper_bound:
            continue

        print("Chemin trouvé:", deep_path)
        print(f"Temps pour trouver le chemin: {end-start: .3}s")

        temps[0][i] = end-start
        resultat[0][i] = deep_path

        # ___MULTI_DIVE___
        start = time.time()
        multi_path = multi_dive(cellules, verticaux, horizontaux, position_robots, position_cible, deep_path)
        end = time.time()

        print("Chemin  multi trouvé:", multi_path)
        print(f"Temps pour trouver le chemin multi: {end-start: .3}s")

        temps[1][i] = end-start
        resultat[1][i] = multi_path

        # ___A_STAR_H1___
        start = time.time()
        a_star_h1_path = a_star_search(position_robots[0], position_cible, 1, cellules, verticaux, horizontaux, deep_path)
        end = time.time()

        print("Chemin A* h1 trouvé:", len(a_star_h1_path)-1)
        print(f"Temps pour A* h1: {end-start:.3}s")

        temps[2][i] = end-start
        resultat[2][i] = len(a_star_h1_path)-1

        # # ___A_STAR_H2___
        # start = time.time()
        # a_star_h2_path = a_star_search(position_robots[0], position_cible, 2, cellules, verticaux, horizontaux, deep_path)
        # end = time.time()

        # print("Chemin A* h2 trouvé:", len(a_star_h2_path)-1)
        # print(f"Temps pour A* h2: {end-start:.3}s")

        # temps[3][i] = end-start
        # resultat[3][i] = len(a_star_h2_path)-1

        # ___A_STAR_MULTI___
        start = time.time()
        a_star_multi_path = a_star_multi_robot(position_robots, position_cible, 1, cellules, verticaux, horizontaux, len(a_star_h1_path)-1)
        end = time.time()

        print("Chemin A* multi trouvé:", len(a_star_multi_path)-1)
        print(f"Temps pour A* multi: {end-start:.3}s\n")

        temps[4][i] = end-start
        resultat[4][i] = len(a_star_multi_path)-1

        i+=1
    
    return temps, resultat

def presentation():

    file = "log.txt"
    upper_bound = 20

    n=8
    k=3
    cellules,verticaux,horizontaux=generateRandomInstances(n,k)
    
    # n=8
    # k=3
    # cellules,verticaux,horizontaux=np.asarray(test_cellules),np.asarray(test_verticaux),np.asarray(test_horizontaux)
    
    #n=4
    #k=2
    #cellules,verticaux,horizontaux=np.asarray(test_cellules2),np.asarray(test_verticaux2),np.asarray(test_horizontaux2)

    # n, k, cellules, verticaux, horizontaux = generate_log_instance(file)
    
    # showgrid(n,cellules,verticaux,horizontaux)

    log_map(cellules,verticaux,horizontaux, file)

    position_cible = None
    position_robots = np.zeros(k, dtype=tuple)

    for r in range(k):
        r_x = np.where(cellules == r+1)[0][0]
        r_y = np.where(cellules == r+1)[1][0]
        position_robots[r] = (r_x,r_y)

    c_x = np.where(cellules == -1)[0][0]
    c_y = np.where(cellules == -1)[1][0]
    position_cible = (c_x,c_y)

    print("\nPositions initial des robots:", position_robots)
    print("Position de la cible:", position_cible)

    # position_robots[0] = move_line(position_robots[0], cellules, verticaux, horizontaux, "RIGHT")
    # showgrid(n,cellules,verticaux,horizontaux)

    start = time.time()
    shortest_path = deep_dive(cellules, verticaux, horizontaux, position_robots[0], position_cible, upper_bound)
    end = time.time()
    print(f"\nTime for deep dive: {end-start:.3}s")
    if shortest_path <= upper_bound:
        print("Shortest path found with deep dive:", shortest_path)
    else:
        print(f"Shortest path not found with deep dive and an upper bound of {upper_bound}.")

    if shortest_path <= upper_bound:
        start = time.time()
        shortest_multi_path = multi_dive(cellules, verticaux, horizontaux, position_robots, position_cible, shortest_path)
        end = time.time()
        print(f"\nTime for multi dive: {end-start:.3}s")
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
        print(f"\nTime for A*: {end-start:.3}s")
        print("\nPath found with A* and h1:", path_h1)
        print("size:", len(path_h1) - 1)

        # cel_cp = cellules.copy()
        # pos_cp = position_robots.copy()
        # for i in range(len(path_h1)):
        #     cel_cp[pos_cp[0][0]][pos_cp[0][1]] = 0
        #     cel_cp[path_h1[i][0]][path_h1[i][1]] = 1
        #     pos_cp[0] = path_h1[i]
        #     showgrid(n,cel_cp,verticaux,horizontaux)

        start = time.time()
        path_h2 = a_star_search(position_robots[0], position_cible, 2, cellules, verticaux, horizontaux)
        end = time.time()
        print(f"\nTime for A*: {end-start:.3}s")
        print("\nPath found with A* and h2:", path_h2)
        print("size:", len(path_h2) - 1)

        log_path(path_h1, file)

        start = time.time()
        path = a_star_multi_robot(position_robots, position_cible, 1, cellules, verticaux, horizontaux, len(path_h1)-1)
        end = time.time()
        print(f"\nTime for multi A*: {end-start:.3}s")
        print("\nPath found with multi A* and h1:", path)
        print("size:", len(path) - 1)

        # for pos in path:
        #     for r in range(k):
        #         cellules[position_robots[r][0]][position_robots[r][1]] = 0
        #         cellules[pos[r][0]][pos[r][1]] = r + 1
        #     position_robots = pos
        #     showgrid(n,cellules,verticaux,horizontaux)

    showgrid(n,cellules,verticaux,horizontaux)

def main(args=None):
    n = 16
    k = 3
    ite = 10

    start = time.time()
    temps, res=mean_time(n,k,ite)
    end = time.time()

    print()
    print(f"Taille moyen des résultats trouvé trouvé sur {ite} instances de deep dive: {np.mean(res[0]): .1f}")
    print(f"Temps moyen d'execution sur {ite} instances deep dive: {np.mean(temps[0]): .3}s")
    
    print(f"Taille moyen des résultats trouvé trouvé sur {ite} instances de multi dive: {np.mean(res[1]): .1f}")
    print(f"Temps moyen d'execution sur {ite} instances multi dive: {np.mean(temps[1]): .3}s")

    print(f"Taille moyen des résultats trouvé trouvé sur {ite} instances de A* h1: {np.mean(res[2]): .1f}")
    print(f"Temps moyen d'execution sur {ite} instances A* h1: {np.mean(temps[2]): .3}s")

    print(f"Taille moyen des résultats trouvé trouvé sur {ite} instances de A* h2: {np.mean(res[3]): .1f}")
    print(f"Temps moyen d'execution sur {ite} instances A* h2: {np.mean(temps[3]): .3}s")

    print(f"Taille moyen des résultats trouvé trouvé sur {ite} instances de A* multi: {np.mean(res[4]): .1f}")
    print(f"Temps moyen d'execution sur {ite} instances A* multi: {np.mean(temps[4]): .3}s")

    print(f"Temps d'execution total: {end-start: .3}s")

if __name__ == '__main__':
    main()