from Evolve.Evolve import * # pylint: disable=unused-wildcard-import
from Math.stats_functions import * # pylint: disable=unused-wildcard-import
from random import shuffle

class Espece:

    def __init__(self, nom, color, Age, Naissance, Nourriture, Surpopulation, Mort_spontanee, Naissance_alternative, Proie, Predateur, Age_moyen, Max_enfant_generation, Max_enfants_individu, Age_Procreation, Repos_Post_Naissance, Espece_Nourriture, Nourriture_par_generation, Generation_sans_manger, Max_individus, Chance_de_mort, Min_individu_naissance2, Min_matures_naissance2, Age_mature_naissance2, Max_perturbateurs_naissance2, Max_predateur, Max_predateur_partage, Min_proies, Etat_a_la_naissance):
        """ Création d'une espèce """

        #Paramètres Généraux
        self.Nom = nom
        self.Couleur = color
        self.Etat_a_la_naissance = Etat_a_la_naissance
        #Règles utilisées
        self.Age = Age
        self.Naissance = Naissance
        self.Nourriture = Nourriture
        self.Surpopulation = Surpopulation
        self.Mort_spontanee = Mort_spontanee
        self.Naissance_alternative = Naissance_alternative
        self.Proie = Proie
        self.Predateur = Predateur

        #Paramètres des Règles
        #Age
        self.Age_moyen = Age_moyen
        #Naissance
        self.Max_enfants_generation = Max_enfant_generation
        self.Max_enfants_individu = Max_enfants_individu
        self.Age_Procreation = Age_Procreation
        self.Repos_Post_Naissance = Repos_Post_Naissance
        #Nourriture
        self.Espece_Nourriture = Espece_Nourriture
        self.Nourriture_par_generation = Nourriture_par_generation
        self.Generation_sans_manger = Generation_sans_manger
        #Surpopulation
        self.Max_individus = Max_individus
        #Mort Spontanée
        self.Chance_de_mort = Chance_de_mort
        #Naissance alternative
        self.Min_individu_naissance2 = Min_individu_naissance2
        self.Min_matures_naissance2 = Min_matures_naissance2
        self.Age_mature_naissance2 = Age_mature_naissance2
        self.Max_perturbateurs_naissance2 = Max_perturbateurs_naissance2
        #Proie
        self.Max_predateur = Max_predateur
        #Predateur
        self.Max_predateur_partage = Max_predateur_partage
        self.Min_proies = Min_proies

    #Fonction Vie
    def ft_vie(self, etat, environnement, grid_old, grid_new, x, y, z, Config):
        """ Fonction permettant de déterminer l'état d'une case à l'instant t+1 en fonction de l'instant t """
        if self.Mort_spontanee == True:
            if random.randint(1, 100) <= self.Chance_de_mort:
                ft_ajouter_age(self.Nom, etat["Age_moyen"])
                ft_incrementer_morts('MortSpontanee')
                ft_incrementer_morts_par_espece(self.Nom)
                return {"espece" : "Vide", "milieu" : environnement, "etat" : {}}

        if self.Age == True:
            etat["Age_moyen"] += 1
            if etat["Age_moyen"] >= self.Age_moyen:
                ft_ajouter_age(self.Nom, etat["Age_moyen"])
                ft_incrementer_morts('Age')
                ft_incrementer_morts_par_espece(self.Nom)
                return {"espece" : "Vide", "milieu" : environnement, "etat" : {}}

        if self.Naissance == True or self.Nourriture == True or self.Naissance_alternative == True or self.Surpopulation == True or self.Proie == True or self.Predateur == True:
            env_proche = ft_scan(grid_old, x, y, z)
            shuffle(env_proche)

        if self.Nourriture == True:
            feed = False
            killed = []
            for individu in env_proche:
                coords = individu[1]
                individu = individu[0]
                for food in self.Espece_Nourriture:
                    if food == individu["espece"] and individu["etat"]["Mort"] == False:
                        ft_ajouter_age(self.Nom, etat["Age_moyen"])
                        ft_incrementer_morts('Nourriture')
                        ft_incrementer_morts_par_espece(individu["espece"])
                        individu["etat"]["Mort"] == True
                        etat["Nourriture_par_generation"] += 1
                        killed.append(coords)
                        if etat["Nourriture_par_generation"] >= self.Nourriture_par_generation:
                            etat["Nourriture_par_generation"] = 0
                            etat["Generation_sans_manger"] = 0
                            feed = True
                            break
                if feed == 1:
                    break
            if feed == 1:
                for kill in killed:
                    ft_naissance(grid_new, x + kill[0], y + kill[1], 0, "Vide", {})
            else:
                etat["Generation_sans_manger"] += 1
                if etat["Generation_sans_manger"] > self.Generation_sans_manger:
                    return {"espece" : "Vide", "milieu" : environnement, "etat" : {}}

        if self.Naissance == True:
            if etat["Age_moyen"] >= self.Age_Procreation and etat["Derniere_Procreation"] >= self.Repos_Post_Naissance and etat["Max_enfants_individu"] <= self.Max_enfants_individu:
                etat["Pare_a_Procreer"] = self.Max_enfants_generation
            
                accouplement = 0
                espace = 0
                for individu in env_proche:
                    individu = individu[0]
                    if individu["espece"] == self.Nom and individu["etat"]["Mort"] == False and individu["etat"]["Pare_a_Procreer"] != 0:
                        while accouplement < self.Max_enfants_generation and individu["etat"]["Pare_a_Procreer"] > 0:
                            individu["etat"]["Pare_a_Procreer"] -= 1
                            accouplement += 1
                    if individu["espece"] == "Vide":
                        espace = 1
                if accouplement != 0 and espace == 1:
                    for individu in env_proche:
                        coords = individu[1]
                        individu = individu[0]
                        if individu["espece"] == "Vide" and etat["Max_enfants_generation"] <= self.Max_enfants_generation and etat["Max_enfants_individu"] <= self.Max_enfants_individu and accouplement > 0: 
                            accouplement -= 1
                            ft_incrementer_naissance(self.Nom)                
                            ft_naissance(grid_new, x + coords[0], y + coords[1], 0, self.Nom, self.Etat_a_la_naissance)
                            etat["Max_enfants_generation"] += 1
                            etat["Max_enfants_individu"] += 1
                            etat["Derniere_Procreation"] = -1
                etat["Max_enfants_generation"] = self.Max_enfants_generation
            etat["Derniere_Procreation"] += 1

        if self.Surpopulation == True:
            i = 0
            for individus in env_proche:
                individus = individus[0]
                if individus["espece"] == self.Nom:
                    i += 1
                    if i >= self.Max_individus:
                        ft_ajouter_age(self.Nom, etat["Age_moyen"])
                        ft_incrementer_morts('Surpopulation')
                        ft_incrementer_morts_par_espece(self.Nom)
                        return {"espece" : "Vide", "milieu" : environnement, "etat" : {}}

        if self.Naissance_alternative == True:
            env_list = {}
            for individu in env_proche:
                individu = individu[0]
                if individu["espece"] != "Out" and individu["espece"] != "Vide":
                    if individu["espece"] not in env_list:
                        if Config[individu["espece"]].Age_moyen >= Config[individu["espece"]].Age_mature_naissance2:
                            env_list[individu["espece"]] = [1, 1]
                        else:
                            env_list[individu["espece"]] = [1, 0]
                    else:
                        env_list[individu["espece"]][0] += 1
                        if Config[individu["espece"]].Age_moyen >= Config[individu["espece"]].Age_mature_naissance2:
                            env_list[individu["espece"]][1] += 1

            perturbateur = ""
            
            for espece in env_list:
                if env_list[espece][0] >= Config[espece].Max_perturbateurs_naissance2:
                    if perturbateur != "":
                        ft_incrementer_naissance(self.Nom)
                        return {"espece" : self.Nom, "milieu" : environnement, "etat" : etat}
                    perturbateur = espece

            if perturbateur != "" and env_list[perturbateur][0] >= Config[perturbateur].Min_individu_naissance2 and env_list[perturbateur][1] >= Config[perturbateur].Min_matures_naissance2:
                ft_incrementer_naissance(perturbateur)
                return {"espece" : perturbateur, "milieu" : environnement, "etat" : Config[perturbateur].Etat_a_la_naissance}
            
            for individu in env_list:
                if env_list[individu][0] >= Config[individu].Min_individu_naissance2 and env_list[individu][1] >= Config[individu].Min_matures_naissance2:
                    ft_incrementer_naissance(individu)
                    return {"espece" : individu, "milieu" : environnement, "etat" : Config[individu].Etat_a_la_naissance}
            
            return {"espece" : self.Nom, "milieu" : environnement, "etat" : etat}

        if self.Proie == True:
            predateurs = 0
            for individu in env_proche:
                individu = individu[0]
                if individu["espece"] != "Out" and self.Nom in Config[individu["espece"]].Espece_Nourriture:
                    predateurs += 1
            if predateurs >= self.Max_predateur:
                ft_ajouter_age(self.Nom, etat["Age_moyen"])
                ft_incrementer_morts('Proie')
                ft_incrementer_morts_par_espece(self.Nom)
                return {"espece" : "Vide", "milieu" : environnement, "etat" : {}}
        
        if self.Predateur == True:
            congenere = 0
            proies = 0
            for individu in env_proche:
                individu = individu[0]
                if individu["espece"] == self.Nom:
                    congenere += 1
                elif individu["espece"] in self.Espece_Nourriture:
                    proies += 1
            if congenere >= self.Max_predateur_partage and proies <= self.Min_proies:
                ft_ajouter_age(self.Nom, etat["Age_moyen"])
                ft_incrementer_morts('Predateur')
                ft_incrementer_morts_par_espece(self.Nom)
                return {"espece" : "Vide", "milieu" : environnement, "etat" : {}}

        return {"espece" : self.Nom, "milieu" : environnement, "etat" : etat}