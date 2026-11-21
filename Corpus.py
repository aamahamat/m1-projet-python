# Corpus.py
import pandas as pd
from datetime import datetime
from Author import Author
from Document import Document, HackerNewsDocument, ArxivDocument, DocumentFactory

class Corpus:
    instance = None
    # 3.1 Constructeur avec les attributs demandés
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    @classmethod
    def get_instance(cls, nom="corpus"):
        if cls.instance is None:    # tiroir vide : on crée l'objet et on le range
            cls.instance = Corpus(nom)
        return cls.instance         # s

    # 3.1 Méthode d'ajout d'un document qui met à jour id2doc et authors
    def add_doc(self, doc):
        self.id2doc[self.ndoc] = doc
        self.ndoc += 1

        if doc.auteur not in self.authors:
            self.authors[doc.auteur] = Author(doc.auteur)
            self.naut += 1
        self.authors[doc.auteur].add(doc)

    # 3.2 Affichage des documents avec leur source via getType()
    def afficher_avec_source(self, n=None):
        docs = list(self.id2doc.values())
        if n is not None:
            docs = docs[:n]
        for doc in docs:
            print(doc.getType(), ":", doc.titre)

    # 3.2 Affichage des documents triés par date
    def trier_par_date(self, n):
        docs_tries = sorted(self.id2doc.values(), key=lambda doc: doc.date)
        for doc in docs_tries[:n]:
            print(doc)

    # 3.2 Affichage des documents triés par titre
    def trier_par_titre(self, n):
        docs_tries = sorted(self.id2doc.values(), key=lambda doc: doc.titre)
        for doc in docs_tries[:n]:
            print(doc)

    # 3.2 Méthode __repr__ pour un affichage digeste du corpus
    def __repr__(self):
        return ("Corpus '" + self.nom + "' : " + 
                str(self.ndoc) + " documents, " + 
                str(self.naut) + " auteurs.")

    # 3.3 Sauvegarde du corpus sur le disque via un DataFrame pandas
    def save(self, nom_fichier):
        lignes = []
        for id_doc, doc in self.id2doc.items():
            date_str = doc.date.strftime("%Y-%m-%d") if isinstance(doc.date, datetime) else str(doc.date)
            lignes.append({
                "id": id_doc,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": date_str,
                "url": doc.url,
                "texte": doc.texte
            })
        df = pd.DataFrame(lignes)
        df.to_csv(nom_fichier, sep="\t", index=False)

    # 3.3 Chargement du corpus depuis le disque via un DataFrame pandas
    def load(self, nom_fichier):
        df = pd.read_csv(nom_fichier, sep="\t")
        # On réinitialise les dictionnaires et compteurs avant de charger
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

        for _, row in df.iterrows():
            titre = str(row["titre"]) if pd.notna(row["titre"]) else ""
            auteur = str(row["auteur"]) if pd.notna(row["auteur"]) else "Inconnu"
            date_str = str(row["date"])[:10]
            date = datetime.strptime(date_str, "%Y-%m-%d")
            url = str(row["url"]) if pd.notna(row["url"]) else ""
            texte = str(row["texte"]) if pd.notna(row["texte"]) else ""

            doc = Document(titre, auteur, date, url, texte)
            self.add_doc(doc)
        
        