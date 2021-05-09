#DRAW MAP (+save)
#ESPECE (+ft_vie)
#DEFINITION ESPECES
#Generation carte + simulation

# ========================== Importation des librairies et des fonctions supplémentaires =============================

from Data.config import *
from Evolve.Evolve import * # pylint: disable=unused-wildcard-import
from Evolve.generate_map import * # pylint: disable=unused-wildcard-import
from Math.stats_functions import * # pylint: disable=unused-wildcard-import
from Tools.SaveMap import * # pylint: disable=unused-wildcard-import
from Tools.Find_Pattern import ft_conclude,ft_find_pattern
from GUI.GUI import ft_conversion_rgb,ft_draw_map
from Evolve.Espece import Espece
if Config["EnableGraphs"] == True:
    # On charge la librairie pyplot si nécessaire
    import matplotlib.pyplot as plt
if Config["EnableGUI"] == True:
    # On charge la librairie tkinter si nécessaire
    from tkinter import * # pylint: disable=unused-wildcard-import

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

# ============================================ Génération de la carte ================================================

try:
    Config["Grid"] = ft_generate_map_repartition(Config["Size"], Config["EspeceList"], Config["RepartitionList"], ft_random_map_creation_args)
    print("Grille générée d'après la liste de répartition indiquée!")
except:
    print("Repartition incorrecte, génération d'un carte aléatoire!")
    Config["Grid"] = ft_generate_map(Config["Size"], Config["EspeceList"], Config["RepartitionList"], ft_random_map_creation_args)

# ====================================================================================================================

# ============================================ Positionnement Précis =================================================


args = ft_random_map_creation_args_repartition("Tomates",  Config["EspeceList"])
Config["Grid"][0][0][0] = {
    "espece": args[0],
    "milieu": args[1],
    "etat": args[2]
}
Config["Grid"][0][0][1] = {
    "espece": args[0],
    "milieu": args[1],
    "etat": args[2]
}
Config["Grid"][0][1][0] = {
    "espece": args[0],
    "milieu": args[1],
    "etat": args[2]
}

# ====================================================================================================================

# ======================================= Configuration du programme =================================================

if Config["SaveMap"] == True:
    #Si on souhaite sauvegarder la carte, il faut réinitialiser le fichier de sauvegarde au démarrage
    sauvegarde = open('save.txt', 'w+')
    sauvegarde.close()

if Config["EnableGUI"] == True:
    # Si l'interface graphique est activée, on crée la fenêtre
    fenetre = Tk()
    #Récupération des variables d'environnement
    screenx = fenetre.winfo_screenwidth()
    screeny = fenetre.winfo_screenheight()

    #Génération de la fenêtre
    fenetre.title("Projet Net2")
    fenetre.geometry(str(screenx) + 'x' + str(screeny))
    Map = Canvas(fenetre, height = screeny,width = screeny, background = "#CC2EFA")
    Map.pack(side = LEFT)

    # On affiche la carte initiale
    ft_draw_map(fenetre, Config["Grid"], screeny, Config["DynamicDisplay"], Config["AffichageMoyenne"], Config["EspeceList"], Map)

if Config["EnableGraphs"] == True:
    # Si activé, on génère les statistiques initiales
    Stats = {}
    for k in Especes.keys():
        Stats[k] = [ft_compter_individus_espece(Config["Grid"], k)]

# ====================================================================================================================

# ================================== Boucle infinie d'évolution du système ===========================================

#initialisation du Programme
i = 1
j = 1
while 1:
    if Config["SaveMap"] == True:
        ft_save_map(Config["Grid"], 'save.txt', Especes)
    if Config["StatsSav"] == True:
        ft_save_stats()
    if Config["PersonNumber"] == True:
        ft_compter_individus(Config["Grid"], j)
    if Config["EnableGUI"] == True:
        if i >= Config["DisplayRate"]:
            i = 1
            ft_draw_map(fenetre, Config["Grid"], screeny, Config["DynamicDisplay"], Config["AffichageMoyenne"], Config["EspeceList"], Map)
    if Config["EnableGraphs"] == True:
        plt.clf()
        for k in Especes.keys():
            Stats[k].append(ft_compter_individus_espece(Config["Grid"], k))
            plt.plot(range(j+1), Stats[k], label=k)
        plt.pause(0.0000000000000000001) # On veut que le programme s'arrête le moins longtemps possible
                                         # Pour cela, il faut mettre un temps de pause non nul mais le plus faible possible
    #input()
    if Config["RandomIterative"] == True:
        ft_random_actualize(Config)
    else:
        ft_actualize(Config)
    #Pattern = [["!shark", "shark", "shark" "!shark"], ["shark", "shark", "shark" "shark"], ["shark", "shark", "shark" "shark"], ["!shark", "shark", "shark" "!shark"]]
    #Grid = Config["Grid"][0]
    #Pattern_return_dic = ft_conclude(Pattern, Especes.keys())
    #print("Nombre d'occurence trouvées : ", ft_find_pattern(Pattern, Grid, Pattern_return_dic))
    #print(j)
    j += 1
    i += 1

# ====================================================================================================================