
# ==================================== Définition des fonctions exportées ============================================
__all__ = [ 'ft_conversion_rgb', 'ft_draw_map']
# ====================================================================================================================

def ft_conversion_rgb(rgb):
    """ Conversion d'un tuple rgb qui contient les valeurs entre 0 et 255 de rouge, vert, et bleu en code HTML
    rgb étant de la forme (0,0,0) """
    return "#%02x%02x%02x" % rgb 

def ft_draw_map(fenetre, grid, screeny, DynamicDisplay, n, EspeceList, Map, mode = -1, Especes = {}):
    """ Affiche la carte sur la fenêtre.
    Chaque couleur est la moyenne les couleurs du carré de (2n+1)**2 cubes environnants (au maximum, moins au bord de la carte) """
    Map.delete("all")
    # Lit le contenu de la carte et l'affiche dans la fenêtre
    if len(grid) == 1:
        taille = len(grid[0])
        cell_taille = screeny // taille
        for x in range(taille):
            for y in range(taille):
                k = 0
                couleur = [0,0,0]
                for i in range(-n,n+1):
                    for j in range(-n, n+1):
                        if x+i >= 0 and y+j >= 0 and x+i < len(grid[0]) and y+j < len(grid[0][0]):
                            k +=1
                            r,g,b = 0,0,0
                            if mode == -1:
                                r,g,b = EspeceList[grid[0][x+i][y+j]["espece"]].Couleur
                            else:
                                r,g,b = EspeceList[Especes[grid[0][x+i][y+j]]].Couleur
                            couleur[0] += r
                            couleur[1] += g
                            couleur[2] += b
                couleur[0] = int(couleur[0] / k) #
                couleur[1] = int(couleur[1] / k) # Chaque composante de couleur est moyennée
                couleur[2] = int(couleur[2] / k) #
                couleur = tuple(couleur)
                outline = (0,0,0)
                if mode == -1:
                    outline = EspeceList[grid[0][x][y]["espece"]].Couleur
                else:
                    outline = EspeceList[Especes[grid[0][x][y]]].Couleur
                Map.create_rectangle(x * cell_taille, y * cell_taille, x * cell_taille + cell_taille, y * cell_taille + cell_taille, fill = ft_conversion_rgb(couleur), outline = ft_conversion_rgb(outline))
                if DynamicDisplay == True: # Si l'affichage dynamique est activé, on met à jour la fenêtre à chaque itération dans la carte
                    fenetre.update()
    fenetre.update()
    print("Affichage OK")