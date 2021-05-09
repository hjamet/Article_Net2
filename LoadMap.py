#DRAW MAP
#ESPECE
#DEFINITION ESPECES

# ========================== Importation des librairies et des fonctions supplémentaires =============================

from tkinter import * # pylint: disable=unused-wildcard-import
from Data.config import * # pylint: disable=unused-wildcard-import
from Evolve.Evolve import * # pylint: disable=unused-wildcard-import
from Evolve.generate_map import * # pylint: disable=unused-wildcard-import
from Math.stats_functions import * # pylint: disable=unused-wildcard-import
from Evolve.Espece import Espece
from GUI.GUI import ft_draw_map
import json

# ====================================================================================================================

# ======================================= Configuration du programme =================================================

sauvegarde = open('save.txt', 'r')
grids = sauvegarde.readlines()

# Récupération des variables d'environnement
fenetre = Tk()
screenx = fenetre.winfo_screenwidth()
screeny = fenetre.winfo_screenheight()

# Génération de la fenêtre
fenetre.title("Projet Net2")
fenetre.geometry(str(screenx) + 'x' + str(screeny))
Map = Canvas(fenetre, height = screeny,width = screeny, background = "#CC2EFA")
Map.pack(side = LEFT)

# ====================================================================================================================

# ============================================= Création des espèces =================================================

FichierEspeces = open('Data/especes.py') # On stocke la définition des espèces dans un fichier extérieur pour pouvoir tester différentes configurations
ChaineEspeces = FichierEspeces.readlines()
for i in ChaineEspeces:
    if i[0] != '#': # Si la ligne n'est pas commentée, l'exécuter
        exec(i)
FichierEspeces.close()
ListeEspeces = list(Config["EspeceList"].keys()) # On crée une liste des noms d'espèce, afin de générer le dictionnaire pour alléger la carte sauvegardée
Especes = dict([(k, ListeEspeces[k]) for k in range(len(ListeEspeces))]) # On crée le dictionnaire cité à la ligne précédente

# ====================================================================================================================

ft_draw_map(fenetre, json.loads(grids[0]), screeny, Config["DynamicDisplay"], Config["AffichageMoyenne"], Config["EspeceList"], Map, mode=0, Especes=Especes)

# =========================================== Affichage de la fenêtre ================================================

# Compteur de génération
i = 0

def printMap():
    if Config["PersonNumber"] == True:
        ft_compter_individus2(json.loads(grids[i]), i, Especes)
    ft_draw_map(fenetre, json.loads(grids[i]), screeny, Config["DynamicDisplay"], Config["AffichageMoyenne"], Config["EspeceList"], Map, mode=0, Especes=Especes)
    fenetre.update()

def incrementGrid(event):
    global i
    if i == len(grids) - 1:
        return
    i += 1
    printMap()

def decrementGrid(event):
    global i
    if i == 0:
        return
    i -= 1
    printMap()

fenetre.bind('<Left>', decrementGrid)
fenetre.bind('<Right>', incrementGrid)
fenetre.focus_set()
fenetre.mainloop()

# ====================================================================================================================