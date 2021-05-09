def ft_conclude(Pattern, especes_possibles):
    """Retourne un dictionnaire de la liste des cases pouvant être en haut à droite du pattern si la case de coords x,y est de type 'type'; espece_possible est une liste de tous les noms d'espece possibles, ! Suivi du nom de l'espece ne dvant pas se trouver à cet emplacement (Inclus dans ft_find_pattern)"""
    output = {}
    for espece in especes_possibles:
        output[espece] = []
        for x in range(len(Pattern)):
            for y in range(len(Pattern[0])):
                if Pattern[x][y] != espece and Pattern[x][y] != '?' and Pattern[x][y][0] != '!' or Pattern[x][y][0] == '!' and Pattern[x][y][1:] == espece:
                    output[espece].append((-x, -y))
    return output


def ft_find_pattern(Pattern, Grid, Pattern_return_dic):
    """Fonction qui retourne le nombre de fois qu'elle a trouvé le pattern rentré dans la grille; Pattern est de la forme [["!", "fish", "!"], ["fish", "fish", "fish"], ["!", "fish", "!"]] pour une un pattern de taille 3x3 avec un croix de l'espèce "fish", Grid est de type x,y et non x, y, z; Le ? indique que n'importe quoi peut se trouver là. Le ! indique que tout sauf l'espece considérée peut se trouver là"""
    
    output = 0
    check = Pattern[0][0]
    different_check = True if check[0] == '!' else False 
    if different_check == True:
        check = check[1:]

    Empty_Grid = []
    for x in range(len(Grid)):
        Empty_Grid.append([])
        for y in range(len(Grid[0])):
            Empty_Grid[-1].append(0)

    for x in range(len(Grid[0]) - len(Pattern[0]) + 1):
        for y in range(len(Grid) - len(Pattern) + 1):
            if Empty_Grid[x][y] == 1:
                continue
            if different_check == False and Grid[x][y]["espece"] == check or different_check == True and Grid[x][y]["espece"] != check:
                continuer = True
                for x_temp in range(len(Pattern[0])):
                    if continuer == False:
                        break
                    for y_temp in range(len(Pattern)):
                        if Pattern[y_temp][x_temp] != '?' and ((Pattern[y_temp][x_temp] != Grid[x + x_temp][y + y_temp]["espece"] and Pattern[y_temp][x_temp][0] != '!') or (Pattern[y_temp][x_temp][0] == '!' and Pattern[y_temp][x_temp][1:] == Grid[x + x_temp][y + y_temp]["espece"])):
                            continuer = False
                            break
                if continuer == True:
                    output += 1
            for coords in Pattern_return_dic[Grid[x][y]["espece"]]:
                if x + coords[0] >= 0 and y + coords[1] >= 0:
                    Empty_Grid[x + coords[0]][y + coords[1]] = 1
    
    return output
            
