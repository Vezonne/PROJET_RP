import numpy as np
import random
import heapq as hq
from matplotlib import pyplot as plt
from test import *



position_debut_robot=[]
position_cible=None

def generateRandomInstances(n,k):
    global position_cible
    global position_debut_robot
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
                    position_debut_robot.append((abs,ord))
                
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
                    position_cible=(butx,buty)
                
                
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
                        position_debut_robot.append((abs,ord))
                
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
                        position_cible=(butx,buty)
        
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
     

def move_up(robot_pos, cellules):
    """
    Déplace la position du robot vers le haut d'une cellule si possible.

    Args:
        robot_pos (tuple): La position actuelle du robot sous forme de tuple (x, y).
        cellules (list): Une liste 2D représentant la grille de cellules.

    Returns:
        tuple: La nouvelle position du robot après le déplacement vers le haut, sous forme de tuple (x, y).
    """
    x = robot_pos[0]
    y = robot_pos[1]
    if x != 0 and horizontaux[x-1][y] == 0 and cellules[x-1][y] <= 0:
        cellules[x][y] = 0
        cellules[x-1][y] = 1
        (x, y) = move_up((x-1, y), cellules)
    return (x, y)

def move_down(robot_pos, cellules):

    x = robot_pos[0]
    y = robot_pos[1]
    if x!=len(cellules)-1 and horizontaux[x][y]==0 and cellules[x+1][y]<=0:
        cellules[x][y]=0
        cellules[x+1][y]=1
        (x,y) = move_down((x+1,y), cellules)
    return (x,y)

def move_left(robot_pos, cellules):

    x = robot_pos[0]
    y = robot_pos[1]
    if y!=0 and verticaux[x][y-1]==0 and cellules[x][y-1]<=0:
        cellules[x][y]=0
        cellules[x][y-1]=1
        (x,y) = move_left((x,y-1), cellules)
    return (x,y)

def move_right(robot_pos, cellules):

    x = robot_pos[0]
    y = robot_pos[1]
    if y!=len(cellules)-1 and verticaux[x][y]==0 and cellules[x][y+1]<=0:
        cellules[x][y]=0
        cellules[x][y+1]=1
        (x,y) = move_right((x,y+1), cellules)
    return (x,y)

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
            ucel = cellules.copy()
            dcel = cellules.copy()
            lcel = cellules.copy()
            rcel = cellules.copy()

            upos = move_up(robot_pos, ucel)
            dpos = move_down(robot_pos, dcel)
            lpos = move_left(robot_pos, lcel)
            rpos = move_right(robot_pos, rcel)

            res.append(deep_dive(ucel, verticaux, horizontaux, upos, cible_pos, m, i, 2))
            res.append(deep_dive(dcel, verticaux, horizontaux, dpos, cible_pos, m, i, 2))
            res.append(deep_dive(lcel, verticaux, horizontaux, lpos, cible_pos, m, i, 1))
            res.append(deep_dive(rcel, verticaux, horizontaux, rpos, cible_pos, m, i, 1))
        case 1: #up or down
            ucel = cellules.copy()
            dcel = cellules.copy()

            upos = move_up(robot_pos, ucel)
            dpos = move_down(robot_pos, dcel)

            res.append(deep_dive(ucel, verticaux, horizontaux, upos, cible_pos, m, i, 2))
            res.append(deep_dive(dcel, verticaux, horizontaux, dpos, cible_pos, m, i, 2))
        case 2: #left or right
            lcel = cellules.copy()
            rcel = cellules.copy()
            
            lpos = move_left(robot_pos, lcel)
            rpos = move_right(robot_pos, rcel)
            
            res.append(deep_dive(lcel, verticaux, horizontaux, lpos, cible_pos, m, i, 1))
            res.append(deep_dive(rcel, verticaux, horizontaux, rpos, cible_pos, m, i, 1))

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
        ucel = cellules.copy()
        dcel = cellules.copy()
        lcel = cellules.copy()
        rcel = cellules.copy()

        robot = robots_pos[r]

        ulist = robots_pos.copy()
        ulist[r] = move_up(robot, ucel)

        dlist = robots_pos.copy()
        dlist[r] = move_down(robot, dcel)

        llist = robots_pos.copy()
        llist[r] = move_left(robot, lcel)

        rlist = robots_pos.copy()
        rlist[r] = move_right(robot, rcel)

        res.append(multi_dive(ucel, verticaux, horizontaux, ulist, cible_pos, m, i))
        res.append(multi_dive(dcel, verticaux, horizontaux, dlist, cible_pos, m, i))
        res.append(multi_dive(lcel, verticaux, horizontaux, llist, cible_pos, m, i))
        res.append(multi_dive(rcel, verticaux, horizontaux, rlist, cible_pos, m, i))
    
    return min(res)

n=10
k=4

cellules,verticaux,horizontaux=generateRandomInstances(n,k)
# cellules,verticaux,horizontaux=np.asarray(test_cellules),np.asarray(test_verticaux),np.asarray(test_horizontaux)

position_cible = None
position_robots = np.zeros(k, dtype=tuple)

for i in range(len(cellules)):
    for j in range(len(cellules[i])):
        if cellules[i][j]==-1:
            position_cible=(i,j)
        elif cellules[i][j]>0:
            position_robots[cellules[i][j]-1] = (i,j)

print(position_robots)
print(position_cible)

shortest_path = deep_dive(cellules, verticaux, horizontaux, position_robots[0], position_cible)
print(shortest_path)

# shortest_path = multi_dive(cellules, verticaux, horizontaux, position_robots, position_cible, shortest_path)
# print(shortest_path)

# showgrid(n,cellules,verticaux,horizontaux)
#move_up(position_debut_robot[0])
#move_down(position_debut_robot[0])
#move_left(position_debut_robot[0])
#move_right(position_debut_robot[0])

position_debut_robot=[]

# n=16
# k=5

# cellules,verticaux,horizontaux=generateRandomInstances(n,k)

# print(position_debut_robot)
# print(position_cible)
# position_debut_robot=[]

# showgrid(n,cellules,verticaux,horizontaux)



def heuristique(cellules):
    h=cellules.copy()
    tmp_i=np.where(cellules==-1)[0][0]
    tmp_j=np.where(cellules==-1)[1][0]

    for i in range (len(h)):
        for j in range(len(h)):
            if i!=tmp_i and j!= tmp_j:
                h[i][j]=2
            else:
                h[i][j]=1
        h[tmp_i][tmp_j]=0

    return h

def heuristique2(cellules,verticaux, horizontaux):
    h=np.zeros((len(cellules),len(cellules)))
    pos_initial=(np.where(cellules==1)[0][0],np.where(cellules==1)[1][0])

    h[pos_initial[0]][pos_initial[1]]=0
    a=move_down(pos_initial,cellules)
    b=move_up(pos_initial,cellules)
    c=move_left(pos_initial,cellules)
    d=move_right(pos_initial,cellules)


    return h


h=heuristique2(cellules,verticaux,horizontaux)
print(h)



def successeurs(ropot_pos, cellules):
    return [move_down(ropot_pos,cellules.copy()),
            move_up(ropot_pos,cellules.copy()),
            move_left(ropot_pos,cellules.copy()),
            move_right(ropot_pos,cellules.copy())]

def multi_successuers(robots_pos, cellules):
    res = []
    for r in range(len(robots_pos)):
        ucel = cellules.copy()
        dcel = cellules.copy()
        lcel = cellules.copy()
        rcel = cellules.copy()

        robot = robots_pos[r]

        ulist = robots_pos.copy()
        ulist[r] = move_up(robot, ucel)

        dlist = robots_pos.copy()
        dlist[r] = move_down(robot, dcel)

        llist = robots_pos.copy()
        llist[r] = move_left(robot, lcel)

        rlist = robots_pos.copy()
        rlist[r] = move_right(robot, rcel)

        res.append(ulist)
        res.append(dlist)
        res.append(llist)
        res.append(rlist)
    
    return res

"""
def recherche_A_etoile(robot_pos,cible_pos,cellules,h):
    
    Ouvert=[(0,robot_pos)]
    Fermer=[]
    choisi=(0, robot_pos)

    while Ouvert!=[]:
        s=successeurs(choisi,cellules)
        Ouvert.remove(choisi)
        Fermer.append(choisi)
        for i in s:
            if i==cible_pos:
                return i[0]
            else:
                if i not in Fermer:
                    Ouvert.append(i)

        choisi=Ouvert[0]
        
        for o in Ouvert:
            if (h[o[1][0]][o[1][1]] + o[0]) < (h[choisi[1][0]][choisi[1][1]] + choisi[0]):
                choisi=o
"""

# a=recherche_A_etoile(position_robots[0],position_cible,cellules,heuristique(cellules))
# print(a)


def a_star_search_single(cellules, robot_pos, cible_pos, heuristique):

    frontier = []
    hq.heappush(frontier, (0, robot_pos))
    came_from = {robot_pos: None}
    cost_so_far = {robot_pos: 0}

    while frontier:
        current = hq.heappop(frontier)[1]

        if current == cible_pos:
            break

        for next in successeurs(current, cellules):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristique[next[0]][next[1]]
                hq.heappush(frontier, (priority, next))
                came_from[next] = current

    path = []
    if current[0] != cible_pos:
        return path
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path

path = a_star_search_single(cellules, position_robots[0], position_cible, heuristique(cellules))
print(path)
print(len(path) - 1)

def a_star_search_multi(cellules, robots_pos, cible_pos, heuristique):
    
    frontier = []
    hq.heappush(frontier, (0, robots_pos))
    came_from = {(0, robots_pos[0]): None}
    cost_so_far = {(0, robots_pos[0]): 0}

    while frontier:
        current = hq.heappop(frontier)[1]

        if current[0][1] == cible_pos:
            break

        for next in multi_successuers(current, cellules):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristique[next[0][0]][next[0][1]]
                hq.heappush(frontier, (priority, next))
                came_from[next] = current

    path = []
    if current[0] != cible_pos:
        return path
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path

"""path = a_star_search_multi(cellules, position_robots, position_cible, heuristique(cellules))
print(path)
print(len(path) - 1)"""

showgrid(n,cellules,verticaux,horizontaux)
