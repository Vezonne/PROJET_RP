import numpy as np
import random
from matplotlib import pyplot as plt



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

def deplacement_haut(robot_pos):
    global cellules
    
    pos=robot_pos[0]
    if pos!=0 and horizontaux[pos-1][robot_pos[1]]==0 and cellules[pos-1][robot_pos[1]]<=0:
        cellules[pos][robot_pos[1]]=0
        cellules[pos-1][robot_pos[1]]=1
        deplacement_haut((pos-1,robot_pos[1]))
        
    else:
        return ((pos,robot_pos[1]))
    
def deplacement_bas(robot_pos):
    global cellules
    
    pos=robot_pos[0]
    if pos!=n-1 and horizontaux[pos][robot_pos[1]]==0 and cellules[pos+1][robot_pos[1]]<=0:
        cellules[pos][robot_pos[1]]=0
        cellules[pos+1][robot_pos[1]]=1
        deplacement_bas((pos+1,robot_pos[1]))
        
    else:
        return ((pos,robot_pos[1]))
    
def deplacement_gauche(robot_pos):
    global cellules
    pos=robot_pos[1]
    if pos!=0 and verticaux[robot_pos[0]][pos-1]==0 and cellules[robot_pos[0]][pos-1]<=0:
        cellules[robot_pos[0]][pos]=0
        cellules[robot_pos[0]][pos-1]=1
        deplacement_gauche((robot_pos[0],pos-1))
        
    else:
        return ((robot_pos[0],pos))
    
def deplacement_droite(robot_pos):
    global cellules
    pos=robot_pos[1]
    if pos!=n-1 and verticaux[robot_pos[0]][pos]==0 and cellules[robot_pos[0]][pos+1]<=0:
        cellules[robot_pos[0]][pos]=0
        cellules[robot_pos[0]][pos+1]=1
        deplacement_droite((robot_pos[0],pos+1))
        
    else:
        return ((robot_pos[0],pos))
    
n=6
k=3

cellules,verticaux,horizontaux=generateRandomInstances(n,k)

print(position_debut_robot)
print(position_cible)
showgrid(n,cellules,verticaux,horizontaux)
#deplacement_haut(position_debut_robot[0])
#deplacement_bas(position_debut_robot[0])
#deplacement_gauche(position_debut_robot[0])
deplacement_droite(position_debut_robot[0])

showgrid(n,cellules,verticaux,horizontaux)


position_debut_robot=[]

"""n=16
k=5

cellules,verticaux,horizontaux=generateRandomInstances(n,k)

print(position_debut_robot)
print(position_cible)
position_debut_robot=[]

showgrid(n,cellules,verticaux,horizontaux)"""












