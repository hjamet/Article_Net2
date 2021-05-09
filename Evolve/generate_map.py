import random
from math import ceil #pylint: disable=no-name-in-module

def ft_generate_percent_list(repartitionList):
  """ Trie la liste de répartition par ordre croissant de pourcentage """
  i = 0
  while i < len(repartitionList) - 1:
    if repartitionList[i][1] > repartitionList[i + 1][1]:
      (repartitionList[i], repartitionList[i + 1]) = (repartitionList[i + 1], repartitionList[i])
      i = 0
    else:
      i += 1
  return repartitionList

def ft_generate_map(taille, especeList, repartitionList, ft_random_map_creation_args):
  """ Génère une carte aléatoirement et dans des proportions aléatoires """
  grid = []

  for ord_z in range(1):
    grid.append([])
    for ord_x in range(taille):
      grid[ord_z].append([])
      for ord_y in range(taille): # pylint: disable=unused-variable
        args = ft_random_map_creation_args(especeList)
        grid[ord_z][ord_x].append({
          "espece": args[0],
          "milieu": args[1],
          "etat": args[2]
        })
  return grid

def ft_generate_map_repartition(taille, especeList, repartitionList, ft_random_map_creation_args):
  """ Génère une carte aléatoirement, dans des proportions données """
  grid = []
  individus = []
  for espece in repartitionList:
    for percent in range(int((espece[1] * 0.01 * taille ** 2))): # pylint: disable=unused-variable
      individus.append(espece[0])
  random.shuffle(individus)
  for ord_z in range(1):
    grid.append([])
    for ord_x in range(taille):
      grid[ord_z].append([])
      for ord_y in range(taille): # pylint: disable=unused-variable
        args = ft_random_map_creation_args_repartition(individus[0], especeList)
        grid[ord_z][ord_x].append({
          "espece": args[0],
          "milieu": args[1],
          "etat": args[2]
        })
        del individus[0]
  return grid        

def ft_random_map_creation_args_repartition(espece, especeList):
  """ Renvoie les caractéristiques de l'espèce demandée, ainsi qu'un age maximal aléatoire """
  etat = especeList[espece].Etat_a_la_naissance.copy()
  if espece != "Vide":
    etat["Age_moyen"] = random.randint(0, especeList[espece].Age_moyen)
  return [espece, {"Oxygène" : 20}, etat]

def ft_random_map_creation_args(especeList):
  """ Renvoie des caractéristiques aléatoires pour la nouvelle case """
  espece = [especes for especes in especeList][random.randint(0, len(especeList)) - 1]
  etat = especeList[espece].Etat_a_la_naissance.copy()
  if espece != "Vide":
    etat["Age_moyen"] = random.randint(0, especeList[espece].Age_moyen)
  return [espece, {"Oxygène" : 20}, etat]
