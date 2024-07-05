import json
import os
import shlex

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
        path = input("Indiquer le chemin d'accès (exemple : './BDD.json') :")
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
    return 'add'


#%%
'''
supr une app à la bdd
'''


def deleteApp(item, BDD):
    return ''


#%%
'''
modifie une app de la bdd
'''


def editApp(item, BDD):
    return ''


#%%

def terminal(cmd, BDD):
    arg1 = ['help', 'print', 'add', 'delete']  # Choses possibles
    disques = getDisques(BDD)  # Disques possibles

    # Si la commande est vide
    if cmd == "":
        return "Erreur : entrée vide | Voir help pour plus d'informations"

    cmds = shlex.split(cmd)
    print(f"Commandes : {', '.join(cmds)}")
    print(len(cmds), " Argument(s)")

    if cmds[0] not in arg1:
        return "Erreur : commande invalide | Voir help pour plus d'informations"

    if cmds[0] == "help":
        return f"Commandes possibles : {', '.join(arg1)}"

    # Dictionnaire de commandes
    command_dict = {
        'add': addApp,
        'delete': deleteApp,
        'edit': editApp
    }

    # Vérifier les arguments supplémentaires pour les commandes add, delete et edit
    if cmds[0] in command_dict:
        # for arg in cmds[1:]:
        print(cmds[1])
        if cmds[1] not in disques:
            return f"Erreur : argument 2 '{cmds[1]}' non valide"

        result = command_dict[cmds[0]]
        # result()
        print("arg2 valide")
        return "Exit 0"

    # Traitement de la commande print (ou toute autre commande future sans arguments supplémentaires)
    if cmds[0] == 'print':
        # Ajoutez ici la logique pour la commande print si nécessaire
        return f"Disques : {', '.join(getDisques(BDD))}"

    return "Erreur : commande invalide"

# Parcourir chaque argument dans cmds
# for arg in cmds:
#     # Vérifier si l'argument est dans arg1
#     if arg in arg1:
#         print('Argument 1 OK')
#     # Vérifier si l'argument est dans arg2
#     elif arg in arg2:
#         print('Argument', arg, 'dans arg2 OK')
#     else:
#         return f"Erreur : argument '{arg}' non valide"

#%%

# fixName(app, type)
# retourne app ou launcher en bien écrit
# retourne false si il arrive pas

#%%

print("Fonctions lues")
