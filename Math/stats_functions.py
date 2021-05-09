import json

# ==================================== Définition des fonctions exportées ============================================
__all__ = [ 'ft_compter_individus', 'ft_compter_individus2', 'ft_compter_individus_espece', 'ft_save_stats', 'ft_load_stats', 'ft_incrementer_naissance', 'ft_incrementer_morts_par_espece', 'ft_incrementer_morts', 'ft_ajouter_age']
# ====================================================================================================================

Morts_par_espece = {}
Morts = {}
Naissance = {}
Age = {}

def ft_compter_individus(grid, Generation):
    """ Compte le nombre d'individus par espèce dans une carte """
    individu_par_espece = {}
    taille = len(grid[0])
    case_nbr = taille ** 2
    if len(grid) == 1:
        for x in range(taille):
            for y in range(taille):
                espece = grid[0][x][y]["espece"]
                if espece in individu_par_espece:
                    individu_par_espece[espece] += 1
                else:
                    individu_par_espece[espece] = 0
        string = ""
        for especes in individu_par_espece:
            string += str(especes) + ' : ' + str(individu_par_espece[especes]) + " Pourcentage : " + str(round((individu_par_espece[especes] * 100) / case_nbr, 2)) + "%\n"
        print("Génération ", Generation, ':\n\n', string, sep="")

def ft_compter_individus2(grid, Generation, Especes):
    """ Compte le nombre d'individus par espèce dans une grille simplifiée (celle qui est sauvegardée puis analysée après simulation) """
    individu_par_espece = {}
    taille = len(grid[0])
    case_nbr = taille ** 2
    if len(grid) == 1:
        for x in range(taille):
            for y in range(taille):
                espece = Especes[grid[0][x][y]]
                if espece in individu_par_espece:
                    individu_par_espece[espece] += 1
                else:
                    individu_par_espece[espece] = 0
        string = ""
        for especes in individu_par_espece:
            string += str(especes) + ' : ' + str(individu_par_espece[especes]) + " Pourcentage : " + str(round((individu_par_espece[especes] * 100) / case_nbr, 2)) + "%\n"
        print("Génération", Generation, ':\n\n', string)
            
def ft_compter_individus_espece(grid, Espece_a_chercher):
    """ Compte le nombre d'individus d'une espèce donnée """
    individus = 0
    mode = type(grid[0][0][0]) # Permet de s'adapter au type de carte (complète ou simplifiée)
    taille = len(grid[0])
    if len(grid) == 1:
        for x in range(taille):
            for y in range(taille):
                espece = grid[0][x][y]
                if mode == int: # Mode simplifié
                    if espece == Espece_a_chercher:
                        individus += 1
                elif espece["espece"] == Espece_a_chercher:
                    individus += 1
    return individus

def ft_save_stats():
    """ Sauvegarde les statistiques """
    try:
        file = open('morts_par_espece.json', 'w+')
        file.write(json.dumps(Morts_par_espece))
        file.close()
        file = open('morts.json', 'w+')
        file.write(json.dumps(Morts))
        file.close()
        file = open('naissance.json', 'w+')
        file.write(json.dumps(Naissance))
        file.close()
        file = open('age.json', 'w+')
        file.write(json.dumps(Age))
        file.close()
    except:
        print("ERREUR: Une erreur est survenue lors de l'écriture des statistiques")
    return

def ft_load_stats():
    """ Charge les statistiques """
    try:
        file = open('morts_par_espece.json', 'r')
        Morts_par_espece = json.loads(file.read()) # pylint: disable=unused-variable
        file.close()
        file = open('morts.json', 'r')
        Morts = json.loads(file.read()) # pylint: disable=unused-variable
        file.close()
        file = open('naissance.json', 'r')
        Naissance = json.loads(file.read()) # pylint: disable=unused-variable
        file.close()
        file = open('age.json', 'r')
        Age = json.loads(file.read()) # pylint: disable=unused-variable
        file.close()
    except:
        print("ERREUR: Une erreur est survenue lors de l'écriture des statistiques")
    return

def ft_incrementer_naissance(espece):
    """ Incrémente le nombre de naissances d'une espèce """
    if espece == 'Vide':
        return
    if espece in Naissance:
        Naissance[espece] +=1
    else:
        Naissance[espece] = 1

def ft_incrementer_morts_par_espece(espece):
    """ Incrémente le nombre de morts d'une espèce """
    if espece in Morts_par_espece:
        Morts_par_espece[espece] +=1
    else:
        Morts_par_espece[espece] = 1

def ft_incrementer_morts(type_mort):
    """ Incrémente le nombre de morts d'un type de mort donné """
    if type_mort in Morts:
        Morts[type_mort] +=1
    else:
        Morts[type_mort] = 1

def ft_ajouter_age(espece, age):
    """ Ajoute l'age d'un individu à sa mort aux statistiques """
    if espece in Age:
        Age[espece] += [age]
    else:
        Age[espece] = [age]