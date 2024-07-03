import json
import os

path_settings = "../assets/settings.json"


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
'''
Retourne la couleur par rapport aux paramètres
'''


def get_color(index):
    fichiersettings = open(path_settings, "r", encoding='utf-8')
    colorsload = json.load(fichiersettings)
    fichiersettings.close()
    colors = colorsload["colors"]
    return colors[index % len(colors)]


#%%
# GETTERS
'''
Retourne les disques de la bdd
'''


def getDisques(BDD):
    return list(BDD.keys())


#%%
### A FAIRE ###

#%%
'''
Retourne les launchers
'''


def getLaunchers(BDD):
    launchers = []
    for disques in BDD.values():
        launchers.extend(disques.keys())
    return launchers


# print(getLaunchers())

#%%
'''
Retourne apps
'''


def getApps(BDD):
    apps = []
    for disques in BDD.values():
        for launcher in disques.values():
            apps.extend(launcher)
    return apps


#%%
'''
Retourne le nbre de disques de la bdd
'''


def getNbDisques(BDD):
    return len(BDD)


#%%
'''
Retourne le nombre apps
'''


def getNbLaunchers(BDD):
    return len(getLaunchers(BDD))


#%%
'''
Retourne le nombre launchers
'''


def getNbApps(BDD):
    return len(getApps(BDD))


#%%
'''
ajoute une app à la bdd
'''


def addApp(item, BDD):
    return ''


#%%
'''
supr une app à la bdd
'''


def delete(item, BDD):
    return ''


#%%
'''
modifie une app de la bdd
'''


def edit(item, BDD):
    return ''


#%%

def terminal(cmd):
    arg1 = ['help', 'print', 'add', 'delete', 'edit']  # Choses possibles
    arg2 = ['C', 'D', 'E', 'F', 'G']  # Disques possibles

    # Si la commande est vide
    if cmd == "":
        cmd = "vide"
        return "Erreur : entrée vide"

    else:
        cmds = cmd.split(' ')
        print("Nombre d'arguments :", len(cmds))

        # Parcourir chaque argument dans cmds
        for arg in cmds:
            # Vérifier si l'argument est dans arg1
            if arg in arg1:
                print('Argument 1 OK')
            # Vérifier si l'argument est dans arg2
            elif arg in arg2:
                print('Argument', arg, 'dans arg2 OK')
            else:
                return f"Erreur : argument '{arg}' non valide"

    return str(cmds)


#%%

print("Fonctions lues")
