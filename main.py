import numpy as np
import random
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
     
# Ces fonctions permettent de déplacer un robot dans une grille en 2D.
# Chaque fonction vérifie si le mouvement est possible, puis effectue le mouvement et renvoie la nouvelle position du robot.

def move_up(robot_pos, cellules):
    # Récupère les coordonnées du robot
    x = robot_pos[0]
    y = robot_pos[1]
    # Vérifie si le robot peut se déplacer vers le haut
    if x!=0 and horizontaux[x-1][y]==0 and cellules[x-1][y]<=0:
        # Effectue le mouvement
        cellules[x][y]=0
        cellules[x-1][y]=1
        # Récursivement, continue à se déplacer vers le haut
        (x,y) = move_up((x-1,y), cellules)
    # Renvoie la nouvelle position du robot
    return (x,y)

# Les fonctions move_down, move_left et move_right fonctionnent de la même manière que move_up, mais pour les autres directions.


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
    # Cette fonction utilise une recherche en profondeur pour trouver le chemin le plus court vers une cible.
    # cellules est une grille représentant l'espace de travail du robot.
    # verticaux et horizontaux sont des grilles représentant les murs ou les obstacles.
    # robot_pos est la position actuelle du robot.
    # cible_pos est la position de la cible.
    # m est le nombre maximum de mouvements que le robot peut effectuer.
    # i est le nombre de mouvements que le robot a déjà effectués.
    # d est la direction du dernier mouvement du robot (0 = aucune, 1 = horizontal, 2 = vertical).

    if robot_pos == cible_pos:
        # Si le robot a atteint la cible, renvoie le nombre de mouvements effectués.
        return i
        
    if i == m:
        # Si le robot a atteint le nombre maximum de mouvements, renvoie m+1.
        return m+1
    
    i += 1
    # Incrémente le nombre de mouvements.

    res = []
    # Initialise une liste pour stocker les résultats des mouvements possibles.

    match d:
        # Selon la direction précédente, le robot peut se déplacer soit verticalement, soit horizontalement, soit dans toutes les directions.
        case 0: #up, down, left, right
            # Pour chaque direction possible, la fonction effectue le mouvement, puis appelle récursivement deep_dive avec la nouvelle position et le nouveau nombre de mouvements.
            # Les résultats sont stockés dans la liste res.
            # Notez que cellules est copié avant chaque mouvement pour éviter de modifier la grille originale.
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
            # Si le dernier mouvement était horizontal, le robot peut seulement se déplacer verticalement.
            ucel = cellules.copy()
            dcel = cellules.copy()

            upos = move_up(robot_pos, ucel)
            dpos = move_down(robot_pos, dcel)

            res.append(deep_dive(ucel, verticaux, horizontaux, upos, cible_pos, m, i, 2))
            res.append(deep_dive(dcel, verticaux, horizontaux, dpos, cible_pos, m, i, 2))
        case 2: #left or right
            # Si le dernier mouvement était vertical, le robot peut seulement se déplacer horizontalement.
            lcel = cellules.copy()
            rcel = cellules.copy()
            
            lpos = move_left(robot_pos, lcel)
            rpos = move_right(robot_pos, rcel)
            
            res.append(deep_dive(lcel, verticaux, horizontaux, lpos, cible_pos, m, i, 1))
            res.append(deep_dive(rcel, verticaux, horizontaux, rpos, cible_pos, m, i, 1))

    return min(res)
    # Finalement, la fonction renvoie le minimum de res, qui est le nombre minimum de mouvements pour atteindre la cible.
        
n=8
k=3

# cellules,verticaux,horizontaux=generateRandomInstances(n,k)
cellules,verticaux,horizontaux=np.asarray(test_cellules),np.asarray(test_verticaux),np.asarray(test_horizontaux)

position_cible = None
position_robots = dict()

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

showgrid(n,cellules,verticaux,horizontaux)
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