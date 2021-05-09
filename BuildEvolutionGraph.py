#ESPECE
#DEFINITION ESPECES

# ========================== Importation des librairies et des fonctions supplémentaires =============================

from Data.config import *
from Math.stats_functions import * # pylint: disable=unused-wildcard-import
from Evolve.Espece import Espece
import matplotlib.pyplot as plt
import json

sauvegarde = open('save.txt', 'r')
grids = sauvegarde.readlines()

# ====================================================================================================================

# ============================================= Création des espèces =================================================

FichierEspeces = open('Data/especes.py') # On stocke la définition des espèces dans un fichier extérieur pour pouvoir tester différentes configurations
ChaineEspeces = FichierEspeces.readlines()
for i in ChaineEspeces:
    if i[0] != '#': # Si la ligne n'est pas commentée, l'exécuter
        exec(i)
FichierEspeces.close()
ListeEspeces = list(Config["EspeceList"].keys()) # On crée une liste des noms d'espèce, afin de générer le dictionnaire pour alléger la carte sauvegardée
Especes = dict([(ListeEspeces[k], k) for k in range(len(ListeEspeces))]) # On crée le dictionnaire cité à la ligne précédente

# ====================================================================================================================

# =========================================== Calcul des statistiques ================================================

stats = {}

for espece in Config["EspeceList"].keys():
    stats[espece] = []
    for i in range(len(grids)):
        stats[espece].append(ft_compter_individus_espece(json.loads(grids[i]), Especes[espece]))

# ====================================================================================================================

# ========================================= Affichage des statistiques ===============================================

for i in stats:
    plt.plot(list(range(len(stats[i]))), stats[i], label=i)
plt.legend()
plt.show()

for i in stats:
    for j in range(len(stats[i])):
        if j != 0:
            plt.scatter(stats[i][j], (stats[i][j] - stats[i][j-1])/stats[i][j], color="blue")
    plt.title(i)
    plt.show()

# ====================================================================================================================