from random import randint
import numpy as np
import pprint as p
import datetime
from pytz import timezone

game_over = False
global nombreReelDeBombes

dicoFonctions = {  # Dictionnaire pour recenser les fonctions                 ON SAVAIT PAS QUON POUVAIT DOCU LES FONCTIONS...
    "grille": "Création d'un dictionnaire 'plateau' comportant pour chaque case: Une clé (tuple) dont la première valeur est l'abscisse (augmente vers la droite), et la deuxième est l'ordonnée (augmente vers la droite); Une valeur (liste de trois valeurs) dont le premier chiffre représente la bombe (0=Pas de Bombe, -1=Bombe), le deuxième le nombre de bombes autour uniquement si la case ne comporte pas de bombe, et le troisième est l'état de la case (0=Cachée, 1=Révélée).",
    "nbbombes": "Compte, pour la case dont les coordonnées doivent être fournies en paramètres, le nombre de bombes dans les 8 cases autour.",
    "calcul": "Remplis le dictionnaire 'plateau' et le tableau numpy 'tempTableauNombresEtBombes' avec pour chaque case le nombre de bombes dans les 8 cases autour si la case elle-même ne contient pas de bombe.",
}
dicoVariables = {  # Dictionnaire pour recenser les variables                 ON SAVAIT PAS QUON POUVAIT DOCU LES FONCTIONS...
    "abscisseMax": "Longueur maximale de la grille.",
    "ordonneeMax": "Hauteur maximale de la grille.",
    "quantiteDeBombes": "Nombre approximatif de bombes dans la grille.",
    "tempTableauBombesAffichees": "Array (Tableau numpy) servant à afficher une grille avec les emplacements des bombes.",
    "tempTableauNombresEtBombes": "Array (Tableau numpy) servant à afficher une grille avec les emplacements des bombes et pour chaque autre case le nombre de bombes dans les 8 cases autour.",
    "plateau": 'Dictionnaire avec toutes les cases et leurs valeurs (pour les détails des valeurs, voir dicoFonctions["grille"]).',
    "random_case": "Dans la fonction grille, cette variable est une case choisie aléatoirement pour être une bombe.",
    "nombreReelDeBombes": "Variable globale servant à afficher le nombre de bombes réel, et non celui demandé.",
    "abscisse": "Dans la fonction nbbombes, l'abscisse de la case comptée.",
    "ordonnee": "Dans la fonction nbbombes, l'ordonnée de la case comptée.",
}


class Couleur:
    VERT = "\033[92m"  # VERT
    JAUNE = "\033[93m"  # JAUNE
    ROUGE = "\033[91m"  # ROUGE
    BLEU = "\033[94m"  # BLEU
    MAGENTA = "\033[95m"  # MAGENTA
    CYAN = "\033[96m"  # CYAN
    RESET = "\033[0m"  # RESET LA Couleur


def demineur_credits():
    print("Crédits:")
    print("Programme créé par [REDACTED], [REDACTED] et [REDACTED].")
    print("Librairies utilisées: random, numpy, pprint, datetime, pytz")
    print("Remerciement spécial aux sites StackOverflow et DelftStack (ct dur sinon)")


def check_debug(variable):
    try:
        dicoFonctions[variable]
    except KeyError:
        try:
            dicoVariables[variable]
        except KeyError:
            return False


def grille(abscissemax, ordonneemax):
    """
    précondition : deux entiers correspondant à la taille de la grille
    postcondition : dictionnaire contenant les cases et les bombes
    """
    plateau = {}  # crée un dictionnaire "plateau"
    for abscisse in range(
        1, abscissemax + 1
    ):  # crée une clé dans le dictionnaire pour chaque case
        for ordonnee in range(1, ordonneemax + 1):
            plateau[(abscisse, ordonnee)] = [0, 0, 0]
    for i in range(
        quantiteDeBombes
    ):  # place toutes les bombes aléatoirement sur le plateau
        random_case = (randint(1, abscissemax), randint(1, ordonneemax))
        plateau[random_case[0], random_case[1]][0] = -1
        tempTableauBombesAffichees[random_case[1] - 1, random_case[0] - 1] = -1
        tempTableauNombresEtBombes[random_case[1] - 1, random_case[0] - 1] = -1
    global nombreReelDeBombes  # calcul du nombre total réel de bombes dans la grille
    nombreReelDeBombes = 0
    for value in plateau.values():
        if value[0] == -1:
            nombreReelDeBombes += 1
    return plateau


# print(grille(abscisseMax,ordonneeMax))


# print(plateau)
def nbbombes(abscisse, ordonnee):
    """
    précondition : deux entiers (coordonnee d'une case)
    postcondition : entier correspondant au nombre de bombes autour de la case
    """
    total = 0
    # print(plateau)
    for xMalus in range(-1, 2):
        for yMalus in range(-1, 2):
            try:
                if plateau[abscisse + xMalus, ordonnee + yMalus][0] == -1:
                    total += 1
            except KeyError:
                continue
    return total


# print(nbbombes(int(input("x")),int(input("y"))))


def calcul(
    plateau,
):  # calcule le nombre de bombes pour chaque case, et remplit le dictionnaire et le tableau numpy
    """
    précondition : dictionnaire
    postcondition dictionnaire ou chaque case a son nombre de bombe autour
    """
    for key, value in plateau.items():
        if value[0] != -1:
            tempTableauNombresEtBombes[key[1] - 1, key[0] - 1] = nbbombes(
                key[0], key[1]
            )
            plateau[key[0], key[1]][1] = nbbombes(key[0], key[1])
    return plateau


# print(calcul(plateau))
# print(tempTableauNombresEtBombes)

# print('Sur',quantiteDeBombes,'bombes,',nombreReelDeBombes,'ont été générées avec succès !')


def affichageLigne(numero_de_ligne):
    """
    précondition : entier (numéro de la ligne à afficher)
    postcondition : affichage de la ligne
    """
    global game_over
    for key, value in tempPlateau.items():
        if key[1] == numero_de_ligne and key[0] < 10:
            if value[2] == 0:
                print(Couleur.VERT + "   ·" + Couleur.RESET, end="")
            elif value[2] == 1:
                if value[0] == -1:
                    print("  ", Couleur.ROUGE + "X" + Couleur.RESET, end="")
                    game_over = 1
                else:
                    if value[1] != 0:
                        print(
                            "  ", Couleur.JAUNE + str(value[1]) + Couleur.RESET, end=""
                        )
                    else:
                        print("  ", Couleur.JAUNE + " " + Couleur.RESET, end="")
            elif value[2] == 2:
                print(Couleur.ROUGE + "   #" + Couleur.RESET, end="")
        elif key[1] == numero_de_ligne and key[0] >= 10:
            if value[2] == 0:
                print(Couleur.VERT + "   ·" + Couleur.RESET, end="")
            elif value[2] == 1:
                if value[0] == -1:
                    print("  ", Couleur.ROUGE + "X" + Couleur.RESET, end="")
                    game_over = 1
                else:
                    if value[1] != 0:
                        print(
                            "  ", Couleur.JAUNE + str(value[1]) + Couleur.RESET, end=""
                        )
                    else:
                        print("  ", Couleur.JAUNE + " " + Couleur.RESET, end="")
            elif value[2] == 2:
                print(Couleur.ROUGE + "   #" + Couleur.RESET, end="")


def grilleAffichee():
    """
    précondition : aucune
    postcondition : affichage standard de la grille
    """
    for i in range(8):
        print(" ", end="")
    for i in range(1, abscisseMax + 1):
        if i < 10:
            print(i, "  ", end="")
        elif 10 <= i < 100:
            print(i, " ", end="")
        elif 100 <= i < 1000:
            print(i, "", end="")
    print("")
    for i in range(4):
        print(" ", end="")
    for i in range((abscisseMax * 4) + 4):
        print("-", end="")
    for i in range(1, ordonneeMax + 1):
        print("")
        if i < 10 and i == ordonneeMax:
            print(" ", i, "|", end="")
            affichageLigne(i)
            print()
        elif i < 100 and i == ordonneeMax:
            print("", i, "|", end="")
            affichageLigne(i)
            print()
        elif i < 1000 and i == ordonneeMax:
            print(i, "|", end="")
            affichageLigne(i)
            print()
        elif i < 10 and i != ordonneeMax:
            print(" ", i, "|", end="")
            affichageLigne(i)
        elif i < 100 and i != ordonneeMax:
            print("", i, "|", end="")
            affichageLigne(i)
        elif i < 1000 and i != ordonneeMax:
            print(i, "|", end="")
            affichageLigne(i)


def checkCase(longueur, hauteur):
    """
    précondition : deux entiers (coordonnées d'une case)
    postcondition : booléen
    """
    try:
        plateau[longueur, hauteur]
        if plateau[longueur, hauteur][2] == 1:
            print("")
            print(
                Couleur.ROUGE
                + "Attention, cette case à déjà été révélée !"
                + Couleur.RESET
            )
            print("")
            return False
    except KeyError:
        print("")
        print(
            Couleur.ROUGE
            + "Attention, cette case n'est pas sur la grille !"
            + Couleur.RESET
        )
        print("")
        return False


def selection_case():
    """
    précondition : aucune
    postcondition : deux entiers (coordonnée d'une case)
    """
    try:
        hauteur = int(
            input(
                Couleur.JAUNE
                + "A quelle ligne se trouve la case que vous voulez jouer ? "
                + Couleur.RESET
            )
        )
        longueur = int(
            input(
                Couleur.JAUNE
                + "A quelle colonne se trouve la case que vous voulez jouer ? "
                + Couleur.RESET
            )
        )
        return longueur, hauteur
    except ValueError:
        print(tempTableauNombresEtBombes)


def action():
    """
    précondition : aucune
    postcondition : entier
    """
    print(Couleur.ROUGE + "Options:" + Couleur.RESET)
    print(Couleur.CYAN + "[1] Révéler la case" + Couleur.RESET)
    print(Couleur.CYAN + "[2] Placer un drapeau" + Couleur.RESET)
    print(Couleur.CYAN + "[3] Retirer un drapeau" + Couleur.RESET)
    action = int(input(Couleur.JAUNE + "Que souhaitez-vous faire ? " + Couleur.RESET))
    if action == 1:
        print(Couleur.VERT + "La case va être révélée." + Couleur.RESET)
    elif action == 2:
        print(Couleur.VERT + "Drapeau placé." + Couleur.RESET)
    elif action == 3:
        print(Couleur.VERT + "Drapeau retiré." + Couleur.RESET)
    return action


def decouvrir_case(temp_ordonnee, temp_abscisse):
    """
    précondition : deux entiers (coordonnée)
    postcondition : découverte des cases
    """
    for yMalus in range(-1, 2):
        for xMalus in range(-1, 2):
            try:
                # if xMalus == 0 and yMalus == 0:
                # continue
                # if temp_abscisse + xMalus < 0 or temp_abscisse + xMalus > ordonneeMax - 1:
                # continue
                # if temp_ordonnee + yMalus < 0 or temp_ordonnee + yMalus > abscisseMax - 1:
                # continue
                if tempPlateau[temp_ordonnee + yMalus, temp_abscisse + xMalus][0] != -1:
                    tempPlateau[temp_ordonnee + yMalus, temp_abscisse + xMalus][2] = 1
                else:
                    continue
            except KeyError:
                continue


def IU():
    """
    précondtion : aucune
    postcondition : effectue l'action demandée
    """
    global game_over
    game_over = 0
    global total_cases_visibles
    total_cases_visibles = 0
    nombreReelDeBombes = 0
    for case in plateau.keys():
        if plateau[case][0] == -1:
            nombreReelDeBombes += 1
    while True:
        total_cases_visibles = 0
        for case in tempPlateau.keys():
            if tempPlateau[case][2] == 1:
                total_cases_visibles += 1
            if total_cases_visibles == abscisseMax * ordonneeMax - nombreReelDeBombes:
                break
        grilleAffichee()
        if game_over:
            break
        try:
            temp_ordonnee, temp_abscisse = selection_case()
        except TypeError:
            continue
        # print(tempOrdonnee,tempAbscisse)
        # print(tempPlateau)
        if checkCase(temp_ordonnee, temp_abscisse) == False:
            continue
        else:
            action_utilisateur = action()
            if (
                action_utilisateur == 1
                and tempPlateau[temp_ordonnee, temp_abscisse][0] == -1
            ):
                tempPlateau[temp_ordonnee, temp_abscisse][2] = 1
                game_over = 1
                grilleAffichee()
                break
            elif (
                action_utilisateur == 1
                and tempPlateau[temp_ordonnee, temp_abscisse][0] == 0
                and tempPlateau[temp_ordonnee, temp_abscisse][1] > 0
            ):
                tempPlateau[temp_ordonnee, temp_abscisse][2] = 1
                total_cases_visibles = 0
                for case in tempPlateau.keys():
                    if tempPlateau[case][2] == 1:
                        total_cases_visibles += 1
                if (
                    total_cases_visibles
                    == abscisseMax * ordonneeMax - nombreReelDeBombes
                ):
                    break
            elif (
                action_utilisateur == 1
                and plateau[temp_ordonnee, temp_abscisse][0] == 0
                and plateau[temp_ordonnee, temp_abscisse][1] == 0
            ):
                tempPlateau[temp_ordonnee, temp_abscisse][2] = 1
                total_cases_visibles = 0
                for case in tempPlateau.keys():
                    if tempPlateau[case][2] == 1:
                        total_cases_visibles += 1
                if (
                    total_cases_visibles
                    == abscisseMax * ordonneeMax - nombreReelDeBombes
                ):
                    break
                for yMalus in range(-1, 2):
                    for xMalus in range(-1, 2):
                        try:
                            if (
                                tempPlateau[
                                    temp_ordonnee + yMalus, temp_abscisse + xMalus
                                ][1]
                                == 0
                            ):
                                decouvrir_case(
                                    temp_ordonnee + yMalus, temp_abscisse + xMalus
                                )
                            elif (
                                tempPlateau[
                                    temp_ordonnee + yMalus, temp_abscisse + xMalus
                                ][1]
                                != 0
                            ):
                                pass
                        except KeyError:
                            continue
                for i in range(abscisseMax):
                    for case in plateau.keys():
                        if (
                            tempPlateau[case][1] == 0
                            and tempPlateau[case][0] == 0
                            and tempPlateau[case][2] == 1
                        ):
                            decouvrir_case(case[0], case[1])
            elif action_utilisateur == 2:
                tempPlateau[temp_ordonnee, temp_abscisse][2] = 2
            elif action_utilisateur == 3:
                tempPlateau[temp_ordonnee, temp_abscisse][2] = 0


difficulte = "0"
option = "0"
debug = "0"
stats = open("statistiques_demineur.txt", "a")
nbTotalDeParties = 1
username = str(input("Entrez votre nom d'utilisateur/pseudonyme s'il vous plaît : "))
while (
    option != "1"
    and difficulte != "1"
    and difficulte != "2"
    and difficulte != "3"
    and difficulte != "4"
):
    if option != "1" and option != "2" and option != "3":
        print(
            "Bonjour {}, veuillez choisir une option parmi la liste suivante:".format(
                username
            )
        )
    print(Couleur.ROUGE + "Options disponibles :" + Couleur.RESET)
    print(Couleur.CYAN + "[1] Jouer" + Couleur.RESET)
    print(Couleur.CYAN + "[2] Règles du jeu" + Couleur.RESET)
    print(Couleur.CYAN + "[3] Crédits" + Couleur.RESET)
    print(Couleur.CYAN + "[4] Débug" + Couleur.RESET)
    print(Couleur.CYAN + "[5] Historique des parties et statistiques" + Couleur.RESET)
    print(Couleur.CYAN + "[6] Quitter" + Couleur.RESET)
    option = input(Couleur.JAUNE + "Que souhaitez-vous faire ? " + Couleur.RESET)
    if option == "1":
        print(Couleur.VERT + "Option '[1] Jouer' sélectionée." + Couleur.RESET)
        while (
            difficulte != "1"
            and difficulte != "2"
            and difficulte != "3"
            and difficulte != "4"
        ):
            print(
                Couleur.ROUGE
                + "Veuillez choisir un mode de difficulté :"
                + Couleur.RESET
            )
            print(
                Couleur.VERT
                + "[1] Facile --- Grille de 10 par 10 avec 20% de bombes (~20 bombes)"
                + Couleur.RESET
            )
            print(
                Couleur.JAUNE
                + "[2] Moyen --- Grille de 20 par 20 avec 20% de bombes (~80 bombes)"
                + Couleur.RESET
            )
            print(
                Couleur.ROUGE
                + "[3] Difficile --- Grille de 30 par 30 avec 20% de bombes (~180 bombes)"
                + Couleur.RESET
            )
            print(Couleur.MAGENTA + "[4] Personnalisé" + Couleur.RESET)
            difficulte = input(
                Couleur.JAUNE
                + "Quel mode de difficulté souhaitez-vous ? "
                + Couleur.RESET
            )
            if difficulte == "1":
                print(
                    Couleur.VERT + "Option '[1] Facile' sélectionnée." + Couleur.RESET
                )
                print("")
                abscisseMax = 10
                ordonneeMax = 10
                quantiteDeBombes = 20
            elif difficulte == "2":
                print(Couleur.VERT + "Option '[2] Moyen' sélectionnée." + Couleur.RESET)
                print("")
                abscisseMax = 20
                ordonneeMax = 20
                quantiteDeBombes = 80
            elif difficulte == "3":
                print(
                    Couleur.VERT
                    + "Option '[3] Difficile' sélectionnée."
                    + Couleur.RESET
                )
                print("")
                abscisseMax = 30
                ordonneeMax = 30
                quantiteDeBombes = 180
            elif difficulte == "4":
                print(
                    Couleur.VERT
                    + "Option '[4] Personnalisé' sélectionnée."
                    + Couleur.RESET
                )
                print("")
                abscisseMax = int(
                    input(
                        Couleur.JAUNE
                        + "Combien de cases de longueur ? "
                        + Couleur.RESET
                    )
                )
                ordonneeMax = int(
                    input(
                        Couleur.JAUNE + "Combien de cases de hauteur ? " + Couleur.RESET
                    )
                )
                quantiteDeBombes = int(
                    input(
                        Couleur.JAUNE
                        + "Combien de bombes (environ, le tableau en comportera un peu moins) ? "
                        + Couleur.RESET
                    )
                )
            else:
                print("")
                print(
                    Couleur.ROUGE
                    + "Attention, ce mode de difficulté n'existe pas !"
                    + Couleur.RESET
                )
                print("")
        while True:
            tempTableauBombesAffichees = np.array([[0] * abscisseMax] * ordonneeMax)
            tempTableauNombresEtBombes = np.array([[0] * abscisseMax] * ordonneeMax)
            plateau = grille(abscisseMax, ordonneeMax)
            tempPlateau = calcul(plateau)
            game_over = 0
            IU()
            print("")
            if game_over == 1:
                with open("statistiques_demineur.txt", "a+") as fichier:
                    nbDeLignes = -1
                    fichier.seek(0, 0)
                    contenu = fichier.read().split("\n")
                    for char in contenu:
                        if char:
                            nbDeLignes += 1
                    if nbDeLignes == -1:
                        nbDeLignes = 1
                    fichier.seek(0, 0)
                    totalWins = 0
                    victoires = fichier.read().split("La partie est gagnée.")
                    for win in victoires:
                        if win:
                            totalWins += 1
                    fichier.seek(0, 0)
                    totalLoss = 0
                    defaites = fichier.read().split("La partie est perdue.")
                    for loss in defaites:
                        if loss:
                            totalLoss += 1
                    statsAEcrire: str = "[DEFAITE #{numeroLoss}] Partie numéro {nbDeLignes}, jouée par {username} le {datetime}. La partie est perdue. Nombre de victoires : {totalWins}. Nombre de défaites : {totalLoss}.".format(
                        nbDeLignes=nbDeLignes,
                        username=username,
                        datetime=datetime.datetime.now(
                            tz=timezone("Europe/Paris")
                        ).strftime("%d/%m/%Y à %Hh%M et %S secondes"),
                        totalWins=totalWins,
                        totalLoss=totalLoss + 1,
                        numeroLoss=totalLoss,
                    )
                    fichier.write(str(statsAEcrire))
                    fichier.write("\n")
                    fichier.close()
                nbTotalDeParties += 1
                print(
                    Couleur.ROUGE
                    + "Vous avez perdu ! Voulez vous recommencer une partie ?"
                    + Couleur.RESET
                )
            elif game_over == 0 and total_cases_visibles == (
                abscisseMax * ordonneeMax - nombreReelDeBombes
            ):
                grilleAffichee()
                with open("statistiques_demineur.txt", "a+") as fichier:
                    nbDeLignes = -1
                    fichier.seek(0, 0)
                    contenu = fichier.read().split("\n")
                    for char in contenu:
                        if char:
                            nbDeLignes += 1
                        else:
                            nbDeLignes = 0
                    fichier.seek(0, 0)
                    totalWins = 0
                    victoires = fichier.read().split("La partie est gagnée.")
                    for win in victoires:
                        if win:
                            totalWins += 1
                    fichier.seek(0, 0)
                    totalLoss = 0
                    defaites = fichier.read().split("La partie est perdue.")
                    for loss in defaites:
                        if loss:
                            totalLoss += 1
                    statsAEcrire = "[VICTOIRE #{numeroWin}] Partie numéro {nbDeLignes}, jouée par {username} le {datetime}. La partie est gagnée. Nombre de victoires : {totalWins}. Nombre de défaites : {totalLoss}.".format(
                        nbDeLignes=nbDeLignes,
                        username=username,
                        datetime=datetime.datetime.now(
                            tz=timezone("Europe/Paris")
                        ).strftime("%d/%m/%Y à %Hh%M et %S secondes"),
                        totalWins=totalWins + 1,
                        totalLoss=totalLoss,
                        numeroWin=totalWins,
                    )
                    fichier.write(str(statsAEcrire))
                    fichier.write("\n")
                    fichier.close()
                nbTotalDeParties += 1
                print(
                    Couleur.MAGENTA
                    + "Vous avez gagné ! Voulez vous recommencer une partie ?"
                    + Couleur.RESET
                )
            print(Couleur.VERT + "[1] Oui" + Couleur.RESET)
            print(Couleur.ROUGE + "[2] Non" + Couleur.RESET)
            optionRestart = int(
                input(Couleur.JAUNE + "Que souhaitez-vous faire ? " + Couleur.RESET)
            )
            if optionRestart == 1:
                print(Couleur.VERT + "Option '[1] Oui' sélectionnée." + Couleur.RESET)
                continue
            else:
                print("")
                print(Couleur.VERT + "Option '[2] Non' sélectionnée." + Couleur.RESET)
                print("")
                print(Couleur.JAUNE + "Fin de la partie." + Couleur.RESET)
                print("")
                print(Couleur.JAUNE + "A bientôt !" + Couleur.RESET)
                break

    elif option == "2":
        print(Couleur.VERT + "Option '[2] Règles du jeu' sélectionée." + Couleur.RESET)
        print("")
        print("Les règles du démineur sont très simples.")
        print(
            "Vous allez avoir devant vous une grille, d'une taille qui varie selon la difficulté choisie."
        )
        print("Cette grille contient des mines cachées, placées aléatoirement.")
        print(
            "Votre but est de révéler toutes les cases contenant une mine, mais attention:"
        )
        print(
            "Si par mégarde vous révélez une mine, toute la grille explosera et la partie sera perdue !"
        )
        print(
            "Pour vous aider, chaque case révélée affichera un nombre qui représente le nombre"
        )
        print("de mines dans les 8 cases autour de la cases révélée.")
        print(
            "Vous pouvez aussi placer un drapeau sur les cases que vous suspectez de cacher une mine."
        )
        print(Couleur.MAGENTA + "Amusez-vous bien !" + Couleur.RESET)
        print("")

    elif option == "3":
        print(Couleur.VERT + "Option '[3] Crédits' sélectionnée." + Couleur.RESET)
        demineur_credits()

    elif option == "4":  # Dico debug
        debugTermine = False
        print(Couleur.VERT + "Option '[4] Débug' sélectionée." + Couleur.RESET)
        while debug != 1 and debug != 2 and debugTermine == False:
            print(Couleur.ROUGE + "Options de débug diponibles :" + Couleur.RESET)
            print(Couleur.CYAN + "[1] Débug fonction" + Couleur.RESET)
            print(Couleur.CYAN + "[2] Débug Variable" + Couleur.RESET)
            debug = input(Couleur.JAUNE + "Que souhaitez-vous faire ? " + Couleur.RESET)
            if debug == "1":
                fonctionADebug = input(
                    Couleur.JAUNE
                    + "Quelle fonction voulez-vous examiner ? "
                    + Couleur.RESET
                )
                if check_debug(fonctionADebug):
                    p.pprint(dicoFonctions[fonctionADebug])
                    debugTermine = True
                else:
                    print("")
                    print(
                        Couleur.ROUGE
                        + "Attention, cette fonction n'existe pas !"
                        + Couleur.RESET
                    )
                    print("")
            elif debug == "2":
                variableADebug = input(
                    Couleur.ROUGE
                    + "Quelle variable voulez-vous examiner ? "
                    + Couleur.RESET
                )
                if check_debug(variableADebug):
                    p.pprint(dicoVariables[variableADebug])
                    debugTermine = True
                else:
                    print("")
                    print(
                        Couleur.ROUGE
                        + "Attention, cette variable n'existe pas !"
                        + Couleur.RESET
                    )
                    print("")
            else:
                print("")
                print(
                    Couleur.ROUGE
                    + "Attention, cette option n'existe pas !"
                    + Couleur.RESET
                )
                print("")

    elif option == "5":
        print("")
        print(
            Couleur.VERT
            + "Option '[5] Historique des parties et statistiques' sélectionée."
            + Couleur.RESET
        )
        print("")
        with open("statistiques_demineur.txt", "a+") as fichier:
            fichier.seek(0, 0)
            print(fichier.read())
    elif option == "6":
        print("")
        print(Couleur.VERT + "Option '[6] Quitter' sélectionée." + Couleur.RESET)
        print("")
        print(Couleur.JAUNE + "Fin de la partie." + Couleur.RESET)
        print("")
        print(Couleur.JAUNE + "A bientôt !" + Couleur.RESET)
        break

    else:
        print("")
        print(Couleur.ROUGE + "Attention, cette option n'existe pas !" + Couleur.RESET)
        print("")
