from Evolve.Evolve import ft_copy_grid
import json

def ft_save_map(grid, file, Especes):
    """ Sauvegarde de la carte dans le fichier de sauvegarde """
    sauvegarde = open(file, 'a')
    new_grid = ft_copy_grid(grid)
    for x in range(len(new_grid)):
        taille = len(new_grid[0])
        for y in range(taille):
            for z in range(taille):
                new_grid[x][y][z] = Especes[new_grid[x][y][z]["espece"]]
    sauvegarde.write(json.dumps(new_grid) + '\n')
    sauvegarde.close()