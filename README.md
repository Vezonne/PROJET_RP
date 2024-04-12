# Projet_RP


## Partie 1: Modélisation, instances et résolution par recharche arborescente

### Question 1.

état initial:\
R1=(x1,y1) *position du robot 1*\
...\
Rk=(xk,yk) *position du robot k* \
C=(xi,yi) *position de la case cible*\
avec 0 < (x1,...,xk,y1,...,yk,xi,yi) < n

Transition possible:

Déplacement de R1 vers le haut de a cases: ***(x1,y1+a)***\
Déplacement de R1 vers le bas de a cases: ***(x1,y1-a)***\
Déplacement de R1 vers la gauche de a cases: ***(x1-a,y1)***\
Déplacement de R1 vers la droite de a cases: ***(x1+a,y1)***

état final:

R1 = (xi,yi) = C

### Question 2.

Pour un plateau de taille n x n avec un seul robot on a :\
n<sup>2</sup> solutions

Pour un plateau de taille n x n avec deux robots on a :\
n<sup>2</sup> x (n-1)<sup>2</sup> solutions

Donc pour un plateau de taille n x n avec k robot on a :\
Multiple de i=0 à k-1 de (n<sup>2</sup>-1)

### Question 3.

Le nombre de successeur possible est 5<sup>k</sup>-1
car il y a k robots sur le plateau et chaque robot a 5 successeurs (haut, bas, droite, gauche, immobile) cependant le cas où tous les robots ne bougent pas n'est pas un successeur donc on enlève un cas. 


## Partie 2: Résolution par A*

### Question 8.

L'heuristique h<sub>1</sub> est coïncidente car il y a un seul état but qui est la case cible et l'heuristique de celle-ci est à 0.\
L'heuristique h<sub>1</sub> est monotone car dans tous les cas h(n)- h(m) <= k(n,m)\
par exemple si le robot se trouve sur une case d'heuristique h(n)=2 et qu'il effectue un mouvement vers une case m donc k(n,m)=1 l'heuristique de la case m est forcément égale à 1 ou 2 car on part d'une case où h(n)=2 donc h(n)-h(m) est focement inferieur ou egale à 1 donc c'est une heuristique monotone.

Donc l'heuristique h<sub>1</sub> est à la fois monotone et coïncidente don celle est aussi minorante.

## Partie 3: Résolution par A* bidirectionnel (optionnel)




