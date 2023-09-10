class Jeu():
    def __init__(self):
        self.partie = Partie()
        self.nom_joueur = None
        self.username_entrer = False
        self.point_par_Dalek_detruit = 5
        self.point_par_partie = 0
        self.daleks_tues = 0

    def demander_nom_joueur(self):
        self.nom_joueur = input("Entrez votre username : ")
        self.username_entrer = True

    def jouer_coup(self, rep):
        self.partie.jouer_coup(rep)

    def creer_partie(self):
        self.partie = Partie()
        self.daleks_tues = 0 # reinti chaque partie

class Partie():
    def __init__(self):
        self.airdejeux = Airedejeu(20, 20)
        self.docteur = Docteur(8, 0)
        self.statut_docteur = "vivant"
        self.daleks = []
        self.ferrailles = []
        self.niveau = 0
        self.dalek_par_niveau = 5
        self.creer_niveau()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def jouer_coup(self, rep):
        self.docteur.changer_position(rep)

        for dalek in self.daleks:  # ajout de ma part
            dalek.deplacer(self.docteur)

    def mouvement_permis(self, rep, docteur):  # ajout de ma part
        rep_x, rep_y = rep
        rep_x += docteur.x
        rep_y += docteur.y
        if (((rep_x < 0) or (rep_x >= self.airdejeux.largeur)) or ((rep_y < 0) or (rep_y >= self.airdejeux.hauteur))):
            return False
        return True

    def choix_possible(self, rep):
        if rep.isnumeric():
            numrep = int(rep)
            if ((numrep >= 1) and (numrep <= 9)):
                return True

    def supprimer_dalecks(self, daleks_remove, controleur):  # j'aurais preferer mettre dans class dalek mais je trouve que ça complique la chose pour pas grand chose
        clean_daleks_remove = []
        for dalek in daleks_remove:
            if dalek not in clean_daleks_remove:
                clean_daleks_remove.append(dalek)
        for dalek in clean_daleks_remove:
            self.daleks.remove(dalek)
        if not self.daleks:
            controleur.partie_en_cours = False

    def collision(self, controleur):
        daleks_morts = 0  # Initialisation du nombre de Daleks morts

        for dalek in self.daleks:
            if dalek.x == self.docteur.x and dalek.y == self.docteur.y:
                controleur.partie_en_cours = False
                self.statut_docteur = "mort"
                daleks_morts += 1  # Incrémentation du nombre de Daleks morts

        daleks_remove = []

        for i in range(len(self.daleks)):
            for j in range(i + 1, len(self.daleks)):
                if self.daleks[i].x == self.daleks[j].x:
                    daleks_remove.append(self.daleks[i])
                    daleks_remove.append(self.daleks[j])
                    feraille = Ferraille(self.daleks[i].x, self.daleks[i].y).creer_ferraille(self)

        for dalek in self.daleks:
            for ferraille in self.ferrailles:
                if dalek.x == ferraille.x and dalek.y == ferraille.y:
                    daleks_remove.append(dalek)

        self.supprimer_dalecks(daleks_remove, controleur)

        return daleks_morts  # Retourner le nombre de Daleks morts

    def creer_niveau(self):
        self.niveau += 1
        nb_daleks = self.niveau * self.dalek_par_niveau
        for i in range(nb_daleks):
            x = 10 + i  # pour effectuer des test
            y = 10 + 1
            # x = random.randrange(self.airdejeux.largeur)
            # y = random.randrange(self.airdejeux.hauteur)
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
        if not jeu.username_entrer:
            jeu.demander_nom_joueur()
        if jeu.nom_joueur is not None:
            print(f"Votre plaisir ce jour {jeu.nom_joueur} ? \n q - quitter \n j - jouer \n s - score")
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

    def jouer_coup(self, partie):  # ajout du parametre partie pour que les donnés de la partie en cours soit transmi
        numvalide = False
        while not numvalide:
            print("Jouer votre coups SVP")  # si dans vue self.partie = Partie() alors donnée d'une new partie
            print("(Utilisez votre clavier numerique)")
            rep = input("Votre choix ici : ")
            if partie.choix_possible(rep):
                vrai_rep = self.pos_possibles[rep]
                if partie.mouvement_permis(vrai_rep, partie.docteur):
                    numvalide = True
        return vrai_rep

    def controle_etat_de_la_partie(self):
        pass

    def fin_partie(self, partie):
        daleks_morts = partie.collision(self)

        print(f"Nombre de Daleks morts : {daleks_morts}")
        print("Partie Termine \n")


class Controleur():
    def __init__(self):
        self.partie_en_cours = False
        self.modele = Jeu()
        self.vue = Vue()
        self.choix_menu()

    def choix_menu(self):
        choixvalide = False
        while not choixvalide:
            rep = self.vue.afficher_menu_initial(self.modele)
            if rep == "j" or rep == "J":
                self.modele.creer_partie()
                self.partie_en_cours = True
                self.jouer_partie()
            elif rep == "q" or rep == "Q":
                choixvalide = True
            if rep == "s" or rep == "S":
                pass

    def jouer_partie(self):
        while self.partie_en_cours:
            self.modele.partie.collision(self)
            rep = self.vue.afficher_aire_de_jeux(self.modele.partie)
            if self.partie_en_cours:
                self.modele.jouer_coup(self.vue.jouer_coup(self.modele.partie))

        self.vue.fin_partie(self.modele.partie)  # Passer la partie en cours à fin_partie


if __name__ == "__main__":
    c = Controleur()