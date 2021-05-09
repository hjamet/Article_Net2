Config = {
  #Paramètres de la grille
    "2D": True, # 2D ou 3D (3D NON IMPLEMENTEE)
    "Size": 100, # Taille de la carte
    "RepartitionList" : (("Vide", 100)), # (NE PAS TOUCHER) Indique les pourcentages de répartition des espèce lors de la Création de la Carte.
    "NaissanceAlternative" : False, #Indique si la règle de naissance alternative doit être appliquée (au moins pour certaines espèces)
  #A ne pas modifier
    "Grid" : [],
    "EspeceList" : {},
  #Affichage et optimisation
    "DonePercent" : False, #Affiche en Console le pourcentage fait au cours de l'étape d'évolution.
    "DynamicDisplay" : False, #Actualise la fenêtre durant la phase d'affichage pour déterminer la vitesse d'affichage
    "DisplayRate" : 1, #Actualise la fenêtre toute les X générations.
    "RandomIterative": True, #Actualisation des cases dans l'ordre ou dans un ordre aléatoire
    "EnableGUI": True, #Active l'affichage graphique
    "EnableGraphs": True, #Active les graphiques en temps réel
    "AffichageMoyenne": 3, #Active l'affichage moyenné
  #Statistiques
    "StatsSav" : False,
    "PersonNumber" : True,
    "SaveMap": False #Sauvegarder la carte lors de l'affichage, utile pour une exécution sans écran ou pour analyser plus précisément l'évolution
}
