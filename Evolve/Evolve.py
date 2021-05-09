import copy
import random


def ft_naissance(grid, x, y, z, espece, etat):
    """ ft_naissance fait apparaitre un individu d'une espece données à une case précise de la grille donnée en argument """
    try:
        grid[z][x][y]["espece"] = espece
    except:
        pass
    try:
        grid[z][x][y]["etat"] = etat.copy()
    except:
        pass

def ft_scan(grid, x, y, z):
    """ cherche les cases environnantes à celle donnée en argument """
    D2 = len(grid) == 1
    res = []
    for mod_y in range(-1,2):
        for mod_x in range(-1,2):
            if not (x + mod_x == -1 or x + mod_x == len(grid[0]) or y + mod_y== -1 or y + mod_y== len(grid[0])):
                if mod_x != 0 or mod_y != 0: 
                    res.append([grid[0][x + mod_x][y + mod_y], (mod_x, mod_y)])
    return res

def ft_copy_grid(grid):
    """ effectue un copie profonde de la carte """
    res = []
    for z in range(len(grid)):
        res.append([])
        for x in range(len(grid[0])):
            res[z].append([])
            for y in range(len(grid[0][0])):
                res[z][x].append({"espece" : grid[z][x][y]["espece"], "milieu" : grid[z][x][y]["milieu"].copy(), "etat" : grid[z][x][y]["etat"].copy()})
    return res

def ft_actualize(Config):
    """ Calcule la carte de la n+1-ième génération en itérant horizontalement puis verticalement dans la carte """
    D2 = Config["2D"]
    taille = Config["Size"]
    grid = ft_copy_grid(Config["Grid"])

    #Boucle copiée deux fois ci dessous pour Optimisation
    if Config["DonePercent"] == True:
        i = 0
        to_do = taille ** 2
        if D2 == True:
            for y in range(taille):
                for x in range(taille):
                    i += 1
                    print(round((i / to_do) * 100, 2))
                    case = grid[0][x][y]
                    espece = Config["EspeceList"][case["espece"]]
                    grid[0][x][y] = espece.ft_vie(case["etat"], case["milieu"], Config["Grid"], grid, x, y, 0, Config["EspeceList"])
        
    else:
        if D2 == True:
            for y in range(taille):
                for x in range(taille):
                    case = grid[0][x][y]
                    espece = Config["EspeceList"][case["espece"]]
                    grid[0][x][y] = espece.ft_vie(case["etat"], case["milieu"], Config["Grid"], grid, x, y, 0, Config["EspeceList"])
    Config["Grid"] = ft_copy_grid(grid)

def ft_random_actualize(Config):
    """ Calcule la carte de la n+1-ième génération en itérant aléatoirement dans la carte """
    D2 = Config["2D"]
    taille = Config["Size"]
    grid = ft_copy_grid(Config["Grid"])
    list_x = list(range(taille))
    list_y = list(range(taille))
    random.shuffle(list_x)
    random.shuffle(list_y)

    #Boucle copiée deux fois ci dessous pour Optimisation
    if Config["DonePercent"] == True:
        i = 0
        to_do = taille ** 2
        if D2 == True:
            for y in list_y:
                for x in list_x:
                    i += 1
                    print(round((i / to_do) * 100, 2))
                    case = grid[0][x][y]
                    espece = Config["EspeceList"][case["espece"]]
                    grid[0][x][y] = espece.ft_vie(case["etat"], case["milieu"], Config["Grid"], grid, x, y, 0, Config["EspeceList"])
        
    else:
        if D2 == True:
            for y in list_x:
                for x in list_y:
                    case = grid[0][x][y]
                    espece = Config["EspeceList"][case["espece"]]
                    grid[0][x][y] = espece.ft_vie(case["etat"], case["milieu"], Config["Grid"], grid, x, y, 0, Config["EspeceList"])
    Config["Grid"] = ft_copy_grid(grid)

