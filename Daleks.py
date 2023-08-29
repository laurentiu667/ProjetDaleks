import random

class Jeu():
    def __init__(self):
        self.partie = None
        self.nom_joueur = None
    def jouer_coup(self, rep):
        self.partie.jouer_coup(rep)
        # return jouer_coup

    def creer_partie(self):
        self.partie = Partie()

class Partie():
    def __init__(self):
        self.airdejeux = Airedejeu(8, 3)
        self.docteur = Docteur(2, 0)
        self.daleks = []
        self.niveau = 0
        self.dalek_par_niveau = 5
        self.creer_niveau()

    def jouer_coup(self, rep):
        self.docteur.changer_position(rep)
        # bouger Daleks

        # test etat du jeu

        # retourner reponse approprier
        return True

    def creer_niveau(self):
        self.niveau += 1
        nb_daleks = self.niveau * self.dalek_par_niveau
        for i in range(nb_daleks):
            x = random.randrange(self.airdejeux.largeur)
            y = random.randrange(self.airdejeux.hauteur)
            dalek = Dalek(x, y)
            self.daleks.append(dalek)


class Airedejeu():
    def __init__(self, largeur: int, hauteur: int):
        self.largeur = largeur
        self.hauteur = hauteur
class Docteur():
    # tester les limites avant
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def changer_position(self, pos_relative):
        rel_x, rel_y = pos_relative
        self.x += rel_x
        self.y += rel_y

class Ferraille():
    def __init__(self):
        self.x = None
        self.y = None
class Dalek():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def deplacer(self, docteur):
        doc_x = docteur.x
        doc_y = docteur.y

        if self.x < doc_x:
            self.x += 1
        elif self.x > doc_x:
            self.x -= 1

        if self.y < doc_y:
            self.y += 1
        elif self.y > doc_y:
            self.y -= 1

# La vue aide a afficher les choses visuelles
class Vue():
    def __init__(self):
        pass
        self.pos_possibles = reponse_possibles = {
                             "7": [-1,-1],
                             "8": [0, -1],
                             "9": [1, -1],
                             "4": [-1, 0],
                             "5": [0, 0],
                             "6": [1, 0],
                             "1": [-1, 1],
                             "2": [0, 1],
                             "3": [1, 1],
                             }

    def afficher_menu_initial(self):
        print("   ***   Bienvenue au Daleks   ***   ")
        rep = input(("Votre plaisir ce jour ? \n q - quitter \n j - jouer \n s - score"))
        return rep
    def creer_tablo(self, partie):
        tablo = []

        for i in range(partie.airdejeux.hauteur):
            ligne = []
            for j in range(partie.airdejeux.largeur):
                ligne.append("-")
            tablo.append(ligne)
        return tablo

    def afficher_aire_de_jeux(self, partie):
        tablo = self.creer_tablo(partie)

        for i in partie.daleks:
            tablo[i.y][i.x] = "W"

        tablo[partie.docteur.y][partie.docteur.x] = "D"

        for i in tablo:
            print(i)

        return self.jouer_coup()

    def jouer_coup(self):
        print("Jouer votre coups SVP")
        print("(Utilisez votre clavier numerique)")
        rep = input("Votre choix ici : ")
        vrai_rep = self.pos_possibles[rep]
        print(rep, vrai_rep)
        return vrai_rep

class Controleur():
    def __init__(self):
        self.partie_en_cours = False
        self.modele = Jeu()
        self.vue = Vue()
        rep = self.vue.afficher_menu_initial()
        if rep == "j":
            self.modele.creer_partie()
            self.partie_en_cours = True
            self.jouer_partie()

    def jouer_partie(self):
        while self.partie_en_cours:
            rep = self.vue.afficher_aire_de_jeux(self.modele.partie)
            self.modele.jouer_coup(rep)

        rep_coup = self.modele.jouer_coup(rep)
        # rep = self.vue.afficher_aire_de_jeux(self.modele)








if __name__ == "__main__":
    c = Controleur()




