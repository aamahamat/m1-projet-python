# programme principal complet
import os
import json
import html
import urllib.request
import urllib.parse
import xmltodict
from datetime import datetime
from Document import Document, HackerNewsDocument, ArxivDocument, DocumentFactory
from Corpus import Corpus

theme = "climate"
fichier_csv = "corpus.csv"
corpus = Corpus.get_instance(theme)

# Si le fichier existe déjà, on le charge directement sans réinterroger les APIs


if os.path.exists(fichier_csv):
    print("Chargement du corpus depuis le disque...")
    corpus.load(fichier_csv)
else:
    print("Acquisition des données depuis les APIs...")
    
    # 1. Hacker News
    url_hn = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": theme, "tags": "story", "hitsPerPage": 50})
    with urllib.request.urlopen(url_hn) as reponse:
        d_hn = json.load(reponse)

    for hit in d_hn["hits"]:
        titre = (hit.get("title") or "").replace("\n", " ").replace("\t", " ").strip()
        auteur = hit.get("author") or "Inconnu"
        date_str = hit.get("created_at", "")[:10]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        url = hit.get("url") or ""
        
        texte = hit.get("story_text")
        if not texte:
            texte = titre
        texte = html.unescape(texte).replace("<p>", " ").replace("\n", " ").replace("\t", " ").strip()

        if len(texte) >= 20:
            corpus.add_doc(Document(titre, auteur, date, url, texte))

    # 2. Arxiv
    url_arxiv = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": "all:" + theme, "start": 0, "max_results": 50})
    with urllib.request.urlopen(url_arxiv) as reponse:
        d_arxiv = xmltodict.parse(reponse.read())

    entrees = d_arxiv["feed"].get("entry", [])
    if isinstance(entrees, dict):
        entrees = [entrees]

    for entree in entrees:
        titre = entree.get("title", "").replace("\n", " ").replace("\t", " ").strip()
        aut = entree.get("author", {})
        if isinstance(aut, list):
            auteur = aut[0].get("name", "Inconnu")
        else:
            auteur = aut.get("name", "Inconnu")
            
        date_str = entree.get("published", "")[:10]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        url = entree.get("id", "")
        texte = entree.get("summary", "").replace("\n", " ").replace("\t", " ").strip()

        if len(texte) >= 20:
            corpus.add_doc(Document(titre, auteur, date, url, texte))

    # Sauvegarde sur le disque
    corpus.save(fichier_csv)
    print("Corpus sauvegardé dans", fichier_csv)

# --- Tests des fonctionnalités ---

# Affichage du corpus (appelle __repr__)
print("\n--- Informations sur le corpus ---")
print(corpus)

# Affichage d'un document (appelle afficher() puis __str__)
print("\n--- Premier document ---")
corpus.id2doc[0].afficher()
print("Version digeste :", corpus.id2doc[0])

# Tri par date et par titre (3.2)
print("\n--- 5 premiers documents triés par date ---")
corpus.trier_par_date(5)

print("\n--- 5 premiers documents triés par titre ---")
corpus.trier_par_titre(5)

# Statistiques d'un auteur (2.4)
print("\n--- Recherche d'un auteur ---")
print("Exemples d'auteurs présents :", list(corpus.authors.keys())[:5])
nom_auteur = input("Entrez le nom d'un auteur : ")
if nom_auteur in corpus.authors:
    aut = corpus.authors[nom_auteur]
    print(aut)
    taille_moy_car = sum(len(d.texte) for d in aut.production.values()) / aut.ndoc
    taille_moy_mots = sum(len(d.texte.split(" ")) for d in aut.production.values()) / aut.ndoc
    print("Taille moyenne des documents :", round(taille_moy_car, 1), "caractères /", round(taille_moy_mots, 1), "mots")
else:
    print(f"{nom_auteur} est introuvable dans la liste des auteurs.")


# --- Tests des notions du TD 5 ---

print("\n1. Héritage et super()")
doc_test = corpus.id2doc[0]
print("Titre et date hérités :", doc_test.titre, "|", doc_test.date)
print("Est une instance de Document ?", isinstance(doc_test, Document))

print("\n2. Accesseur et mutateur")
hn_ex = HackerNewsDocument("Test HN", "alice", datetime(2026, 1, 1), "http://ex.com", "Un texte assez long.", 10)
print("Commentaires initiaux :", hn_ex.get_nbr_commentaires())
hn_ex.set_nbr_commentaires(-5)        # refusé par le mutateur
hn_ex.set_nbr_commentaires(42)
print("Commentaires après modification :", hn_ex.get_nbr_commentaires())

print("\n3. Polymorphisme et champ type")
print("--- Tri par date (chaque objet utilise SON __str__) ---")
corpus.trier_par_date(5)
print("--- Affichage avec la source (via getType()) ---")
corpus.afficher_avec_source(5)

print("\n4. Singleton")
c2 = Corpus.get_instance("un_autre_nom")
print("corpus et c2 sont le même objet :", corpus is c2)
print("Nombre de documents dans c2 :", c2.ndoc)

print("\n5. Usine (Factory)")
doc_usine = DocumentFactory.creer(
    "Arxiv", "Article test", "Dupont", datetime(2026, 2, 1),
    "http://arxiv.org/abs/0000", "Un résumé d'article scientifique.",
    co_auteurs=["Martin", "Durand"]
)
print(doc_usine)
print("Type renvoyé par getType() :", doc_usine.getType())