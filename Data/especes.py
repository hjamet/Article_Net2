# pylint: disable=all
# self, nom, color, Age, Naissance, Nourriture, Surpopulation, Mort_spontanee, Naissance_alternative, Proie, Predateur, Age_moyen, Max_enfant_generation, Max_enfants_individu, Age_Procreation, Repos_post_Naissance, Espece_Nourriture, Nourriture_par_generation, Generation_sans_manger, Max_individus, Chance_de_mort, Min_individu_naissance2, Min_matures_naissance2, Age_mature_naissance2, Max_perturbateurs_naissance2, Max_predateur, Max_predateur_partage, Min_proies, Etat_a_la_naissance

#################### PLACER ICI LE CONTENU DU FICHIER DE CONFIGURATION D'ESPECES SOUHAITE ############################

Config["EspeceList"]["Vide"] = Espece("Vide", (255,255,255), False, False, False, False, False, Config["NaissanceAlternative"], False, False, 0, 0, 0, 0, 0, [""], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, {})
Config["EspeceList"]["Tomates"] = Espece("Tomates", (255, 150, 0), True, True, False, True, True, False, False, True, 10, 7, 999999999999999999999999999999999999999999999999999999999, 1, 0, [], 0, 0, 3, 10,9, 0, 0, 0, 0, 99, 0, {"Age_moyen" : 0, "Max_enfants_generation" : 0, "Max_enfants_individu" : 0, "Nourriture_par_generation" : 0, "Generation_sans_manger" : 0, "Mort" : False, "Derniere_Procreation" : 9999999999999, "Pare_a_Procreer" : 0})
Config["RepartitionList"] = (("Tomates", 5), ("Vide", 95))

######################################################################################################################