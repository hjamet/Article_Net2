print("Couscous Henri! (Ou Pa :D)")
nom = input("Nom de l'espèce a créer : ")
print("Choix de la couleur!")
color = []
color.append(int(int(input("Pourcentage de Rouge : ")) * 2.55))
color.append(int(int(input("Pourcentage de Vert : ")) * 2.55))
color.append(int(int(input("Pourcentage de Bleu : ")) * 2.55))
Age_moyen = "0"
Age = input("Si l'espèce meurt de vieillesse au bout de x génération, entrer x, sinon entrer -1 : ")
if Age == "-1":
    Age = "False"
else:
    Age_moyen = Age
    Age = "True"
Max_enfants_individu = "0"
Max_enfant_generation = "0"
Age_Procreation, Repos_Post_Naissance = '0', '0'
Naissance = input("Si deux individus et une case vide se trouvent en contact, tapper le nombre d'enfants au maximum par génération : ")
if Naissance == "0":
    Naissance = "False"
else:
    Max_enfant_generation = Naissance
    Naissance = "True"
    Max_enfants_individu = input("Nombre maximum d'enfants par individu au cours de sa longue et belle vie (ou pas) : ")
    Age_Procreation = input("Age à partir duquel un individu est en age de procréer : ")
    Repos_Post_Naissance = input("Nombre de génération pendant lesquelles un individu ne peut plus se reproduire après avoir enfanté : ")
Nourriture_par_generation = "0"
Espece_Nourriture = []
temp = ""
Generation_sans_manger = "0"
Predateur = "True"
Proie = "True"
Max_predateur_partage = '99'
Max_predateur = 10
Min_proies = '0'
while temp != "0":
    if temp != "":
        Espece_Nourriture.append(temp)
    temp = input("Si l'espece a besoin de se nourrire d'autres especes pour survivre, entrer le nom de l'espèce proie, entrer 0 pour arréter : ")
if len(Espece_Nourriture) > 0:
    temp = input("Voulez vous appliquer la règle de nourriture alternative? (1 pour oui): ")
    if temp != '1':
        Nourriture = "True"
        Nourriture_par_generation = input("Nombre de proies que doit faire un individu par génération pour être rassasié : ")
        Generation_sans_manger = input("Nombre de générations que peut survivre un individu sans se nourrir : ")

    else:
        Nourriture = "False"
        Predateur = "True"
        Max_predateur_partage = input("Nombre d'individus de la même espèce à partir duquel l'individu peut mourir de faim : ")
        Min_proies = input("Nombre de proies dans l'environnement proche en dessous duquel si l'individu est en sur-nombre (voir ci dessus), il meurt de faim : ")
        Max_predateur = input("Nombre de prédateurs dans l'environnement proche à partir duquel l'individu meurt dévoré : ")
else:
    Nourriture = "False"
if int(Max_predateur) > 8:
    Max_predateur = '0'
    Proie = "False"
Max_individus = "0"
Surpopulation = input("Entrer le nombre d'individus entrainant une surpopulation : ")
if Surpopulation == "0":
    Surpopulation = "False"
else:
    Max_individus = Surpopulation
    Surpopulation = "True"
Chance_de_mort = "0"
Mort_spontanee = input("Entrer les chances (Plutôt malchances) de mourir spontanément qu'a un individu : ")
if Mort_spontanee == "0":
    Mort_spontanee = "False"
else:
    Chance_de_mort = Mort_spontanee
    Mort_spontanee = "True"
Min_individu_naissance2, Min_matures_naissance2, Age_mature_naissance2, Max_perturbateurs_naissance2 = 0, 0, 0, 0
Naissance_alternative = input("Voulez vous appliquer la règle de Naissance alternative? (True, False) : ")
if Naissance_alternative == "True":
    Min_individu_naissance2 = input("Entrez le minimum d'individus de la même espèce dans l'environnement proche pour se reproduire : ")
    Min_matures_naissance2 = input("Entrez le minimum d'individus matures de la même espèce dans l'environnement proche pour se reproduire : ")
    Age_mature_naissance2 = input("Entrez l'age à partir duquel l'individu est considéré comme mature : ")
    Max_perturbateurs_naissance2 = input("Entrez le maximum d'inidividus appartenant à une autre espece à partir duquel il n'y a pas de reproduction : ")
else:
    Min_individu_naissance2 = 9
    Min_matures_naissance2 = 0
    Age_mature_naissance2 = 0
    Max_perturbateurs_naissance2 = 0

print()
print()
print()
print()
print()
print()
string = ""
string += '''Config["EspeceList"]["''' + nom + '''"] = Espece("''' + nom + '''", ''' + str(tuple(color)) + ''', ''' + Age + ''', ''' + Naissance + ''', ''' + Nourriture + ''', ''' + Surpopulation + ''', ''' + Mort_spontanee + ''', ''' + "False"+ ''', ''' + Proie + ''', ''' + Predateur + ''', ''' + Age_moyen + ''', ''' + Max_enfant_generation + ''', ''' + Max_enfants_individu + ''', ''' + Age_Procreation + ''', ''' + Repos_Post_Naissance + ''', ['''
i = 0
while i < len(Espece_Nourriture):
    i += 1
    string += '''"''' + Espece_Nourriture[i - 1] + '''"'''
    if i != len(Espece_Nourriture):
        string += ', '
string += '''], ''' + Nourriture_par_generation + ''', ''' + Generation_sans_manger + ''', ''' + Max_individus + ''', ''' + Chance_de_mort + ''',''' + str(Min_individu_naissance2) + ''', ''' + str(Min_matures_naissance2) + ''', ''' + str(Age_mature_naissance2) + ''', ''' + str(Max_perturbateurs_naissance2) + ''', ''' + Max_predateur + ''', ''' + Max_predateur_partage + ''', ''' + Min_proies + ''', {"Age_moyen" : 0, "Max_enfants_generation" : 0, "Max_enfants_individu" : 0, "Nourriture_par_generation" : 0, "Generation_sans_manger" : 0, "Mort" : False, "Derniere_Procreation" : 9999999999999, "Pare_a_Procreer" : 0})'''
print("Code généré!")
print(string)
