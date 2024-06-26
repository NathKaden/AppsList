import json
import os

def fonctiontest(a):
    return a

#%%
# loadBDD
def loadBDD(path):
    fichier = open(path, "r", encoding='utf-8')
    BDD = json.load(fichier)
    fichier.close()
    return BDD

#%%
'''
modifie la bdd si c'est bien un json
ex : ./BDDTest.json
'''


def editBDD(*args):
    if args == ():
        print('Args vide')
        path = input("Indiquer le chemin d'accès (exemple : './BDDTest.json') :")
    else:
        path = args
    if path == "":
        path = "vide"
    print("Entrée :", path)
    if path[-5:] == '.json':
        print('Le fichier est bien un json')
        if os.path.exists(path):
            print('Le fichier existe')
            print('Chargement de la base de données')
            loadBDD(path)
            print('Fichier chargé avec succès')
            print(BDD)
    else:
        return "Erreur : Merci de mettre un fichier json."


#test :
#editBDD()

#%%
################ GETTERS ################
'''
Retourne les disques de la bdd
'''


def getDisques(BDD):
    return (list(BDD.keys()))


def get_color(index):
    fichiersettings = open(path_settings, "r", encoding='utf-8')
    colors = json.load(fichier)
    fichiersettings.close()

    colors = ["#ED7F10", "#BDFF00", "skyblue"]
    return colors[index % len(colors)]


#%%
'''
Retourne le nombre de jeux
'''


def getNbJeux(BDD):
    count = 0
    for disque in BDD.values():  # Parcours des niveaux supérieurs ("SSD main", "SSD Sam")
        for platform in disque.values():  # Parcours des plates-formes ("Epic Games", "Steam", etc.)
            for game in platform:  # Parcours des jeux dans chaque plate-forme
                if 'nom' in game:  # Vérification de la présence de la clé "nom"
                    count += 1
    return count

#%%
### A FAIRE ###

#%%
'''
Retourne les launchers
'''


def getLaunchers():
    r = {}
    # for cle in getDisques():
    #     r[cle]=list(BDD[cle].keys())
    return r


# print(getLaunchers())

#%%
'''
Retourne les jeux de la bdd
'''


def getGames():
    r = []
    for c in getDisques():
        r += BDD[c].keys()
    return r


# print(getGames())

#%%
################ FONCTIONS PRINCIPALES ################
def printGamesList(BDD):
    res = ''
    #for cle in bdd:
    #    res+=bdd[cle]
    #
    #    for cle2 in Steam:
    #        res+=bdd[cle2]
    return BDD


#%%
'''
ajoute un jeu à la bdd
'''


def addGame(item, BDD):
    return ''


#%%
'''
supr un jeu à la bdd
'''


def delete(item, BDD):
    return ''


#%%
'''
modifie un jeu de la bdd
'''


def edit(item, BDD):
    return ''


#%%

print("Fonctions lues")
