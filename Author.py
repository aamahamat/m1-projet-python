# Partie 2

class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}
        
    # 2.2 Méthode add pour alimenter production et incrémenter ndoc
    def add(self, doc):
        self.production[self.ndoc] = doc
        self.ndoc += 1

    # 2.2 Affichage digeste de l'auteur
    def __str__(self):
        return self.name + " (" + str(self.ndoc) + " document(s))"