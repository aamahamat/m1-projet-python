#_______________________________________________
# Partie 1
#________________________________________________

# 1.1 Création de la classe avec ses attributs
class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = "Document"

    # 1.2 Affichage 
    def afficher(self):
        print("Titre :", self.titre)
        print("L'auteur :", self.auteur)
        print("Date :", self.date)
        print("URL :", self.url)
        print("Texte :", self.texte)

    def getType(self):
        return self.type

    def __str__(self):
        return self.titre

    # 1.3 

class HackerNewsDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nbr_commentaires):
        super().__init__(titre, auteur, date, url, texte)
        self.nbr_commentaires = nbr_commentaires
        self.type = "Hacker News"

    def get_nbr_commentaires(self):
        return self.nbr_commentaires

    def set_nbr_commentaires(self, nbr_commentaires):
        if nbr_commentaires < 0:
            print("Le nombre des commentaires ne peut etre négatif.")
        else:
            self.nbr_commentaires = nbr_commentaires


    def __str__(self):
        return "[HackerNewsDocument] " + self.titre + self.auteur + str(self.date)  + self.url + self.texte + str(self.nbr_commentaires)

class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, coauteurs=None):
        super().__init__(titre, auteur, date, url, texte)
        self.coauteurs = coauteurs  

        self.type = "ArxivDocument"

    def get_coauteurs(self):
        return self.coauteurs

    def set_coauteurs(self, coauteurs):
        if not coauteurs:
            print("Cet article est publié par un seul auteur.")
            self.coauteurs = []
        else :
            self.coauteurs = coauteurs

    def __str__(self):
        coauteurs_str = ", ".join(self.coauteurs) if isinstance(self.coauteurs, list) else str(self.coauteurs)
        return (
            f"[ArxivDocument] {self.titre} | Auteur: {self.auteur} | "
            f"Co-auteurs: {coauteurs_str} | Date: {self.date} | URL: {self.url}"
        )

        
class DocumentFactory:
    @staticmethod
    def creer(source, titre, auteur, date, url, texte, nb_commentaires=0, co_auteurs=None):
        if source == "Hacker News":
            return HackerNewsDocument(titre, auteur, date, url, texte, nb_commentaires)
        elif source == "Arxiv":
            return ArxivDocument(titre, auteur, date, url, texte, co_auteurs)
        elif source == "Document":
            return Document(titre, auteur, date, url, texte)
        else:
            raise ValueError("Source inconnue : " + str(source))