# Réalisé par Irvan.N et laurentiu.D
import random


class Jeu():
    def __init__(self):
        self.partie_en_cours = False
        self.scores = []

    def creer_partie(self):
        self.partie = Partie()

class Score():
    def __init__(self, partie):
        self.nom = partie.nom_joueur
        self.point = partie.score
        self.dalek_vivant = len(partie.daleks)
        if partie.statut_docteur == "vivant":
            self.score = "Win"
        else:
            self.score = "Loose"


class Partie():
    def __init__(self):
        self.airdejeux = self.demander_lair_de_jeux()
        self.docteur = Docteur(2, 0)
        self.statut_docteur = "vivant"
        self.daleks = []
        self.ferrailles = []
        self.niveau = 0
        self.point_par_Dalek_detruit = 5
        self.dalek_par_niveau = 5
        self.score = 0
        self.nom_joueur = self.demander_nom_joueur()
        self.creer_niveau()

    def demander_nom_joueur(self):
        return input("Entrez votre username : ")

    def demander_lair_de_jeux(self):
        print("Veillez rentrer un largeur minimale de 8 et une hauteur de 10")
        while True:

            pos_x = input("Entrez la largeur du jeux : ")
            pos_y = input("Entrez la hauteur du jeux : ")
            while not (pos_x.isnumeric() and pos_y.isnumeric()):
                pos_x = input("Entrez la largeur du jeux : ")
                pos_y = input("Entrez la hauteur du jeux : ")

            pos_x = int(pos_x)
            pos_y = int(pos_y)
            if pos_x >= 8 and pos_y >= 10:
                return Airedejeu(pos_x, pos_y)
            print("Veuillez recommencer, l'un des deux est invalide")

    def creer_niveau(self):
        self.niveau += 1
        nb_daleks = self.niveau * self.dalek_par_niveau
        i = 0
        while i < nb_daleks:
            x = random.randrange(self.airdejeux.largeur)
            y = random.randrange(self.airdejeux.hauteur)
            dalek = Dalek(x, y)
            if ((dalek not in self.daleks) and ((dalek.x != self.docteur.x) or (dalek.y != self.docteur.y))):
                self.daleks.append(dalek)
                i += 1

    def choix_possible(self, rep, partie):
        if rep.isnumeric():
            numrep = int(rep)
            if ((numrep >= 1) and (numrep <= 9)):
                return True
        elif (rep == "t" or "T"):
            rep = "t"
            return True

    def mouvement_permis(self, rep, partie):
        rep_x, rep_y = rep
        rep_x += partie.docteur.x
        rep_y += partie.docteur.y

        for ferraille in partie.ferrailles:
            if ((rep_x == ferraille.x) and (rep_y == ferraille.y)):
                return False
        if (((rep_x < 0) or (rep_x >= partie.airdejeux.largeur)) or (
                (rep_y < 0) or (rep_y >= partie.airdejeux.hauteur))):
            return False
        return True

    def jouer_coup(self, rep):
        self.docteur.changer_position(rep)

        for dalek in self.daleks:
            dalek.deplacer(self.docteur)

    def collision(self, modele):
        daleks_remove = []

        for dalek in modele.partie.daleks:
            if dalek.x == modele.partie.docteur.x and dalek.y == modele.partie.docteur.y:
                modele.partie_en_cours = False
                modele.partie.statut_docteur = "mort"

        if modele.partie.statut_docteur == "vivant":
            for i in range(len(modele.partie.daleks)):
                for j in range(i + 1, len(modele.partie.daleks)):
                    if modele.partie.daleks[i].x == modele.partie.daleks[j].x and modele.partie.daleks[i].y == \
                            modele.partie.daleks[j].y:
                        if not daleks_remove:
                            daleks_remove.append(modele.partie.daleks[i])
                            daleks_remove.append(modele.partie.daleks[j])
                            feraille = Ferraille(modele.partie.daleks[i].x, modele.partie.daleks[i].y).creer_ferraille(
                                self)
                        else:
                            ok = True
                            ok1 = True
                            for dalek in daleks_remove:
                                if modele.partie.daleks[i] is dalek:
                                    ok = False
                                if modele.partie.daleks[j] is dalek:
                                    ok1 = False
                            if ok:
                                daleks_remove.append(modele.partie.daleks[i])
                            if ok1:
                                daleks_remove.append(modele.partie.daleks[j])

            Dalek.supprimer_dalecks(daleks_remove, modele)
            daleks_remove = []

            for dalek in modele.partie.daleks:
                for ferraille in modele.partie.ferrailles:
                    if dalek.x == ferraille.x and dalek.y == ferraille.y:
                        daleks_remove.append(dalek)
            Dalek.supprimer_dalecks(daleks_remove, modele)


class Airedejeu():
    def __init__(self, largeur: int, hauteur: int):
        self.largeur = largeur
        self.hauteur = hauteur


class Docteur():

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def changer_position(self, pos_relative):
        if pos_relative is not None:
            rel_x, rel_y = pos_relative
            self.x += rel_x
            self.y += rel_y

    def teleport(self, partie):

        while True:
            new_x = random.randrange(partie.airdejeux.largeur)
            new_y = random.randrange(partie.airdejeux.hauteur)
            ferraile = Ferraille(new_x, new_y)
            while (not Dalek.est_a_proximite(Docteur(new_x, new_y), partie.daleks) and (ferraile not in partie.ferrailles)):
                new_x -= partie.docteur.x
                new_y -= partie.docteur.y
                return [new_x, new_y]
            
    def zapper(self, partie):
        daleks_a_supprimer = []

        for dalek in partie.daleks:
            distance_x = abs(dalek.x - self.x)
            distance_y = abs(dalek.y - self.y)
            if distance_x <= 1 and distance_y <= 1:
                daleks_a_supprimer.append(dalek)

        for dalek in daleks_a_supprimer:
            partie.daleks.remove(dalek)

        if daleks_a_supprimer:
            partie.score += partie.point_par_Dalek_detruit
            print("Dalek(s) zappe(s) !")
            
        else:
            print("Aucun Dalek proche a zapper.")
        print(len(partie.daleks))

class Ferraille():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def creer_ferraille(self, partie):
        ferraille = Ferraille(self.x, self.y)
        if not partie.ferrailles:
            partie.ferrailles.append(ferraille)
        elif ferraille not in partie.ferrailles:
            partie.ferrailles.append(ferraille)


class Dalek():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

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

    @classmethod
    def est_a_proximite(self, objet, daleks):
        for dalek in daleks:
            distance_x = abs(objet.x - dalek.x)
            distance_y = abs(objet.y - dalek.y)

            if distance_x <= 2 and distance_y <= 2:
                return True
        return False


    @classmethod
    def supprimer_dalecks(self, daleks_remove, modele):

        for dalek in daleks_remove:
            modele.partie.daleks.remove(dalek)
            modele.partie.score += modele.partie.point_par_Dalek_detruit
        if not modele.partie.daleks:
            modele.partie_en_cours = False


# La vue aide a afficher les choses visuelles
class Vue():
    def __init__(self):
        self.pos_possibles = reponse_possibles = {
            "7": [-1, -1],
            "8": [0, -1],
            "9": [1, -1],
            "4": [-1, 0],
            "5": [0, 0],
            "6": [1, 0],
            "1": [-1, 1],
            "2": [0, 1],
            "3": [1, 1],
        }

    def afficher_menu_initial(self, jeu):
        print("   ***   Bienvenue au Daleks   ***   ")
        print(f"Votre plaisir ce jour ? \n q - quitter \n j - jouer \n s - score")
        rep = input("Votre choix ici : ")
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

        for i in partie.ferrailles:
            tablo[i.y][i.x] = "F"

        tablo[partie.docteur.y][partie.docteur.x] = "D"

        for i in tablo:
            print(i)

        print(f"Credits cosmiques  : {partie.score} \n")

    def jouer_coup(self, partie):
        numvalide = False
        while not numvalide:
            print("Jouer votre coups SVP")
            print("(Utilisez votre clavier numerique)")
            rep = input("Votre choix ici : ")
            if partie.choix_possible(rep, partie):
                if rep.isnumeric():
                    vrai_rep = self.pos_possibles[rep]
                    if partie.mouvement_permis(vrai_rep, partie):
                        numvalide = True
                elif rep == "t":
                    vrai_rep = partie.docteur.teleport(partie)
                    numvalide = True
                elif rep == "z":
                    vrai_rep = partie.docteur.zapper(partie)
                    numvalide = True

        return partie.jouer_coup(vrai_rep)

    def afficher_score(self, score, daleks):
        print(f"Partie : {score.score}")
        print(f"joueur : {score.nom} \n credits cosmiques  : {score.point} \n")
        if daleks:
            print(f"nombre de dalek encore en vie : {score.dalek_vivant} \n")


class Controleur():
    def __init__(self):
        self.modele = Jeu()
        self.vue = Vue()
        rep = self.choix_menu()
        while rep != "q":
            if rep == "j":
                self.modele.partie_en_cours = True
                self.modele.creer_partie()
                self.jouer_partie()
                self.modele.scores.append(Score(self.modele.partie))
                self.vue.afficher_score(self.modele.scores[-1], self.modele.partie.daleks)
            elif rep == "s":
                for score in self.modele.scores:
                    print("\n")
                    self.vue.afficher_score(score, self.modele.partie.daleks)
            rep = self.choix_menu()

    def choix_menu(self):
        choixvalide = False
        while not choixvalide:
            rep = self.vue.afficher_menu_initial(self.modele)
            if rep == "j" or rep == "J":
                return "j"
            elif rep == "q" or rep == "Q":
                return "q"
            if rep == "s" or rep == "S":
                return "s"

    def jouer_partie(self):
        self.vue.afficher_aire_de_jeux(self.modele.partie)
        while self.modele.partie_en_cours:
            if self.modele.partie_en_cours:
                self.vue.jouer_coup(self.modele.partie)
                self.modele.partie.collision(self.modele)
            self.vue.afficher_aire_de_jeux(self.modele.partie)


if __name__ == "__main__":
    c = Controleur()