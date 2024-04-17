import numpy as np
import random
import heapq as hq
from matplotlib import pyplot as plt


def generateRandomInstances(n,k):
    if not type(n) is int or not type(k) is int:
        raise TypeError("Seulement des entiers sont permis") 
    if k <= 0 or k>5:
        raise Exception("Le nombre de robots doit être un entier compris entre 1 et 5") 
    if n<4:
        raise Exception("La taille du plateau doit être supérieure ou égale à 4") 
    if n%2!=0:
        raise Exception("La taille du plateau doit être paire") 
        
    cellules = np.zeros((n,n), dtype=int)
    verticaux = np.zeros((n,n-1), dtype=int)
    horizontaux = np.zeros((n-1,n), dtype=int)
    
    #on place des murs verticaux sur la première et dernière ligne (on en place n/4 aléatoirement)
    
    nb=n//4
    
    lv=random.sample(range(0,n-1), nb)
    for i in range(nb):
        verticaux[0,lv[i]]=1
        
    lv=random.sample(range(0,n-1), nb)  
    for i in range(nb):
        verticaux[n-1,lv[i]]=1 
        
    #on place des murs horizontaux sur la première et dernière colonne (on en place n/4 aléatoirement)
    
    lv=random.sample(range(0,n-1), nb)
    for i in range(nb):
        horizontaux[lv[i],0]=1
        
    lv=random.sample(range(0,n-1), nb)
    for i in range(nb):
        horizontaux[lv[i],n-1]=1
        
    
    #on place les doubles murs. On en place 1 pour 1 sous-ensemble de carré de 4 cellules sur deux (sans compter les lignes et colonnes du bord)
        
    #on parcourt les coins supérieurs gauches de chacun des carrés de 4 cellules
    
    l = [i for i in range(1,n-2) if (i-1)%4==0]
    
    for  i in l:
        for j in l:
            choixh=random.randint(0,1)
            choixv=random.randint(0,1)
            choixa=random.randint(0,1)
            if choixa==0:
                horizontaux[i+choixv-1,j+choixh]=1
                verticaux[i+choixv,j+choixh-1]=1
            else:
                horizontaux[i+choixv,j+choixh]=1
                verticaux[i+choixv,j+choixh]=1
                    
    if n==4: #pas d'ilot central
        #on place k robots au hasard (noté 1,2,...,k). Le robot 1 sera le robot devant atteindre la cible but.
        for i in range(1,k+1):
            posok=False
            while not posok:
                abs=random.randint(0,n-1)
                ord=random.randint(0,n-1)
                if cellules[abs,ord]==0:
                    cellules[abs,ord]=i
                    posok=True
                
        #choix d'une cible but

        posok=False
        while not posok:
            butx=random.randint(1,n-2)
            buty=random.randint(1,n-2)
            if cellules[butx,butx]==0:  #un robot n'est pas sur la cible but
                #on vérifie que l'on est dans un "coin"
                if (((horizontaux[butx-1,buty]==1) or (horizontaux[butx,buty]==1)) and ((verticaux[butx,buty-1]==1) or (verticaux[butx,buty]==1))):
                    cellules[butx,buty]=-1
                    posok=True
                
                
    else:
        #on ajoute un ilot central

        horizontaux[n//2-2,n//2-1]=1
        horizontaux[n//2-2,n//2]=1
        horizontaux[n//2,n//2-1]=1
        horizontaux[n//2,n//2]=1
        verticaux[n//2-1,n//2-2]=1
        verticaux[n//2,n//2-2]=1
        verticaux[n//2-1,n//2]=1
        verticaux[n//2,n//2]=1
        
        #on place k robots au hasard (noté 1,2,...,k), mais pas dans l'ilot central. Le robot 1 sera le robot devant atteindre la cible but.
    
        for i in range(1,k+1):
            posok=False
            while not posok:
                abs=random.randint(0,n-1)
                ord=random.randint(0,n-1)
                #pas dans l'ilot central
                if not((abs==(n//2-1) and ord==(n//2-1)) or (abs==(n//2-1) and ord==(n//2)) or (abs==(n//2) and ord==(n//2-1)) or (abs==(n//2) and ord==(n//2))):
                    if (cellules[abs,ord]==0):
                        cellules[abs,ord]=i
                        posok=True
                
        #choix d'une cible but

        posok=False
        while not posok:
            butx=random.randint(1,n-2)
            buty=random.randint(1,n-2)
            #pas dans l'ilot central
            if not((butx==(n//2-1) and buty==(n//2-1)) or (butx==(n//2-1) and buty==(n//2)) or (butx==(n//2) and buty==(n//2-1)) or (butx==(n//2) and buty==(n//2))):
                if cellules[butx,butx]==0:  #un robot n'est pas sur la cible but
                    #on vérifie que l'on est dans un "coin"
                    if (((horizontaux[butx-1,buty]==1) or (horizontaux[butx,buty]==1)) and ((verticaux[butx,buty-1]==1) or (verticaux[butx,buty]==1))):
                        cellules[butx,buty]=-1
                        posok=True
        
    #print("murs verticaux =")
    #print(verticaux)
    #print("murs horizontaux =")
    #print(horizontaux)
    #print("cases du jeu = ")
    #print(cellules)
    
    return cellules,verticaux,horizontaux
    
def showgrid(n,cellules,verticaux,horizontaux):         
    plt.grid()    

    plt.xlim([0, n])
    plt.ylim([0, n])
   
    plt.xticks(range(n+1))
    plt.yticks(range(n+1))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    
    scolor=["blue","black","green","yellow","red"]
 
    for i in range(n):
        for j in range(n):
            s=""
            if cellules[i][j]>0:
                s=s+'r'+str(cellules[i][j]) 
                plt.text(j,n-i-1,s, fontsize=220//n,color=scolor[cellules[i,j]-1])
            elif cellules[i][j]==-1:                
                plt.text(j,n-i-1,'t', fontsize=220//n,color='blue')
    
    for i in range(n):
        for j in range(n-1):
            if verticaux[i][j]==1:
                p1=[j+1,j+1]
                p2=[n-i,n-i-1]
                plt.plot(p1,p2,color='black',linewidth=3)
                
    for i in range(n-1):
        for j in range(n):
            if horizontaux[i][j]==1:
                p1=[j,j+1]
                p2=[n-i-1,n-i-1]
                plt.plot(p1,p2,color='black',linewidth=3)
                
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    plt.grid(True)
                
    plt.show()
    #plt.savefig('exemple.png')
     

#--------------- DÉPLACEMENTS DU ROBOT -----------------#

def move_one(robot_pos, cellules, verticaux, horizontaux, side, ignore_bots=False):
    """
    Déplace le robot d'une case dans la direction spécifiée.

    Args:
        robot_pos (tuple): La position actuelle du robot sous forme de tuple (x, y).
        cellules (list): Une liste 2D représentant la grille des cellules.
        horizontaux (list): Une liste 2D représentant les murs horizontaux.
        verticaux (list): Une liste 2D représentant les murs verticaux.
        side (str): La direction dans laquelle le robot doit se déplacer. Peut être "UP", "DOWN", "LEFT" ou "RIGHT".

    Returns:
        tuple: La nouvelle position du robot après le déplacement sous forme de tuple (x, y).
    """

    x = robot_pos[0]
    y = robot_pos[1]

    match side:
        case "UP":
            if x != 0 and horizontaux[x-1][y] == 0 and (cellules[x-1][y] <= 0 or ignore_bots):
                cellules[x][y] = 0
                cellules[x-1][y] = 1
                x = x-1
            return (x, y)
        
        case "DOWN":
            if x != len(cellules)-1 and horizontaux[x][y] == 0 and (cellules[x+1][y] <= 0 or ignore_bots):
                cellules[x][y] = 0
                cellules[x+1][y] = 1
                x = x+1
            return (x, y)
        
        case "LEFT":
            if y != 0 and verticaux[x][y-1] == 0 and (cellules[x][y-1] <= 0 or ignore_bots):
                cellules[x][y] = 0
                cellules[x][y-1] = 1
                y = y-1
            return (x, y)
        
        case "RIGHT":
            if y != len(cellules)-1 and verticaux[x][y] == 0 and (cellules[x][y+1] <= 0 or ignore_bots):
                cellules[x][y] = 0
                cellules[x][y+1] = 1
                y = y+1
            return (x, y)
        
def move_line(robot_pos, cellules, verticaux, horizontaux, side):
    """
    Déplace le robot sur la ligne jusqu'à ce qu'il ne puisse plus bouger.

    Args:
        robot_pos (tuple): La position actuelle du robot (x, y).
        cellules (list): La liste des cellules du plateau de jeu.
        horizontaux (list): La liste des murs horizontaux du plateau de jeu.
        verticaux (list): La liste des murs verticaux du plateau de jeu.
        robot_pos (tuple): La position actuelle du robot (x, y).
        side (int): La taille du côté du plateau de jeu.

    Returns:
        tuple: La nouvelle position du robot après le déplacement (x, y).
    """

    x = robot_pos[0]
    y = robot_pos[1]
    has_moved = True

    while has_moved:
        nx, ny = move_one((x, y), cellules, verticaux, horizontaux, side)
        if nx == x and ny == y:
            has_moved = False
        else:
            x = nx
            y = ny
            
    robot_pos = (x, y)
    return robot_pos

#--------------- RECHERCHE DU CHEMIN LE PLUS COURT -----------------#

#------ RECHERCHE EN PROFONDEUR ------#

def deep_dive(cellules, verticaux, horizontaux, robot_pos, cible_pos, m=10, i=0, d=0):
    """
    Cette fonction utilise une recherche en profondeur pour trouver le chemin le plus court vers une cible.

    Args:
        cellules (list): Une grille représentant l'espace de travail du robot.
        verticaux (list): Une grille représentant les murs ou les obstacles verticaux.
        horizontaux (list): Une grille représentant les murs ou les obstacles horizontaux.
        robot_pos (tuple): La position actuelle du robot.
        cible_pos (tuple): La position de la cible.
        m (int, optional): Le nombre maximum de mouvements que le robot peut effectuer. Defaults to 10.
        i (int, optional): Le nombre de mouvements que le robot a déjà effectués. Defaults to 0.
        d (int, optional): La direction du dernier mouvement du robot (0 = aucune, 1 = horizontal, 2 = vertical). Defaults to 0.

    Returns:
        int: Le nombre minimum de mouvements pour atteindre la cible.
    """

    if robot_pos == cible_pos:
        return i
        
    if i == m:
        return m+1
    
    i += 1
    res = []

    match d:
        case 0: #up, down, left, right

            for side in ["UP", "DOWN", "LEFT", "RIGHT"]:
                
                cel_cp = cellules.copy()
                new_pos = move_line(robot_pos, cel_cp, verticaux, horizontaux, side)
                res.append(deep_dive(cel_cp, verticaux, horizontaux, new_pos, cible_pos, m, i, 1 if side in ["LEFT", "RIGHT"] else 2))

        case 1: #up or down
            
            for side in ["UP", "DOWN"]:

                cel_cp = cellules.copy()
                new_pos = move_line(robot_pos, cel_cp, verticaux, horizontaux, side)
                res.append(deep_dive(cel_cp, verticaux, horizontaux, new_pos, cible_pos, m, i, 2))

        case 2: #left or right
            
            for side in ["LEFT", "RIGHT"]:
                
                cel_cp = cellules.copy()
                new_pos = move_line(robot_pos, cel_cp, verticaux, horizontaux, side)
                res.append(deep_dive(cel_cp, verticaux, horizontaux, new_pos, cible_pos, m, i, 1))

    return min(res)
        
def multi_dive(cellules, verticaux, horizontaux, robots_pos, cible_pos, m=10, i=0):
    """
    Fonction récursive qui effectue une recherche multi-profondeur pour trouver le nombre minimum de mouvements nécessaires pour que les robots atteignent la position cible.

    Paramètres:
    - cellules (list): Liste des cellules dans la grille.
    - verticaux (list): Liste des murs verticaux dans la grille.
    - horizontaux (list): Liste des murs horizontaux dans la grille.
    - robots_pos (list): Liste des positions actuelles des robots.
    - cible_pos (tuple): Position cible.
    - m (int): Nombre maximum de mouvements autorisés.
    - i (int): Nombre actuel de mouvements.

    Retourne:
    - int: Nombre minimum de mouvements nécessaires pour atteindre la position cible, ou m+1 si la position cible ne peut pas être atteinte en m mouvements.
    """

    if robots_pos[0] == cible_pos:
        return i
    
    if i == m:
        return m+1
    
    i += 1

    res = []
    
    for r in range(len(robots_pos)):
        
        for side in ["UP", "DOWN", "LEFT", "RIGHT"]:

            cel_cp = cellules.copy()
            new_pos = move_line(robots_pos[r], cel_cp, verticaux, horizontaux, side)
            res.append(multi_dive(cel_cp, verticaux, horizontaux, [new_pos], cible_pos, m, i))
    
    return min(res)

#------ A* ------#

def heuristic(cellules, verticaux, horizontaux, h):
    match h:
        case 1:
            return heuristic1(cellules)
        case 2:
            return heuristic2(cellules, verticaux, horizontaux)

def heuristic1(cellules):
    """
    Calcule l'heuristique pour chaque cellule dans une grille.

    Args:
        cellules (numpy.ndarray): La grille de cellules.

    Returns:
        numpy.ndarray: La grille de cellules avec les valeurs de l'heuristique calculées.
    """

    h = cellules.copy()
    tmp_i = np.where(cellules == -1)[0][0]
    tmp_j = np.where(cellules == -1)[1][0]

    for i in range(len(h)):
        for j in range(len(h)):
            if i != tmp_i and j != tmp_j:
                h[i][j] = 2
            else:
                h[i][j] = 1
        h[tmp_i][tmp_j] = 0

    return h

def heuristic2(cellules,verticaux, horizontaux):

    evalH2 = np.zeros((len(cellules), len(cellules)))
    position = np.where(cellules == 1)
    copCellules = np.copy(cellules)
    n = len(cellules)
    r = 1

    i = 0

    evalH2 = explore_hautH2(n, r, position[0][0], position[1][0], copCellules, verticaux, horizontaux, evalH2, i)
    evalH2 = explore_basH2(n, r, position[0][0], position[1][0], copCellules, verticaux, horizontaux, evalH2, i)
    evalH2 = explore_gaucheH2(n, r, position[0][0], position[1][0], copCellules, verticaux, horizontaux, evalH2, i)
    evalH2 = explore_droiteH2(n, r, position[0][0], position[1][0], copCellules, verticaux, horizontaux, evalH2, i)

    while i<10:
        i+=1

        dev = np.where(evalH2 == i)

        for pos_x, pos_y in zip(dev[0], dev[1]):
            evalH2 = explore_hautH2(n, r, pos_x, pos_y, copCellules, verticaux, horizontaux, evalH2, i)
            evalH2 = explore_basH2(n, r, pos_x, pos_y, copCellules, verticaux, horizontaux, evalH2, i)
            evalH2 = explore_gaucheH2(n, r, pos_x, pos_y, copCellules, verticaux, horizontaux, evalH2, i)
            evalH2 = explore_droiteH2(n, r, pos_x, pos_y, copCellules, verticaux, horizontaux, evalH2, i)
            

    evalH2[position[0][0]][position[1][0]] = 0
    

    return evalH2

def successors(robot_pos, cellules, verticaux, horizontaux, h):

    match h:
        case 1:
            return successors_h1(robot_pos, cellules, verticaux, horizontaux)
        case 2:
            return successors_h2(robot_pos, cellules, verticaux, horizontaux)

def successors_h1(robot_pos, cellules, verticaux, horizontaux):
    """
    Retourne une liste des positions successeurs possibles à partir de la position actuelle du robot.

    Args:
        ropot_pos (tuple): La position actuelle du robot.
        cellules (list): La liste des cellules du plateau.
        verticaux (list): La liste des murs verticaux du plateau.
        horizontaux (list): La liste des murs horizontaux du plateau.

    Returns:
        list: Une liste des positions successeurs possibles.
    """

    res = []
    for side in ["UP", "DOWN", "LEFT", "RIGHT"]:
        cel_cp = cellules.copy()
        new_pos = move_line(robot_pos, cel_cp, verticaux, horizontaux, side)
        res.append(new_pos)

    return res

def multi_successors_h1(robots_pos, cellules, verticaux, horizontaux):
    """
    Retourne une liste de positions possibles pour chaque robot après un déplacement dans les quatre directions possibles.
    
    Args:
        robots_pos (list): Liste des positions actuelles des robots.
        cellules (list): Liste des cellules du plateau de jeu.
        verticaux (list): Liste des murs verticaux du plateau de jeu.
        horizontaux (list): Liste des murs horizontaux du plateau de jeu.
    
    Returns:
        list: Liste des positions possibles pour chaque robot après un déplacement dans les quatre directions possibles.
    """

    res = []
    for r in range(len(robots_pos)):
        for side in ["UP", "DOWN", "LEFT", "RIGHT"]:
            cel_cp = cellules.copy()
            new_pos = move_line(robots_pos[r], cel_cp, horizontaux, verticaux, side)
            res.append(new_pos)
    
    return res

def successors_h2(robot_pos, cellules, verticaux, horizontaux):

    res = []
    for side in ["UP", "DOWN", "LEFT", "RIGHT"]:

        cel_cp = cellules.copy()
        pos = robot_pos
        has_moved = True

        while has_moved:
            new_pos = move_one(robot_pos, cel_cp, horizontaux, verticaux, side, ignore_bots=True)
            if new_pos == pos:
                has_moved = False
            else:
                pos = new_pos
                res.append(new_pos)

    return res

def a_star_search(robot_pos, cible_pos, h, cellules, verticaux, horizontaux):
    
    heuristique = heuristic(cellules, verticaux, horizontaux, h)

    frontier = []
    hq.heappush(frontier, (0, robot_pos))
    came_from = {robot_pos: None}
    cost_so_far = {robot_pos: 0}

    while frontier:
        current = hq.heappop(frontier)[1]

        if current == cible_pos:
            break

        for next in successors(current, cellules, verticaux, horizontaux, h):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristique[next[0]][next[1]]
                hq.heappush(frontier, (priority, next))
                came_from[next] = current

    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    if path[-1] != cible_pos:
         return []

    return path

