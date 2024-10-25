import json
import os
import shlex

path_settings = "./assets/settings.json"


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


def addApp(item, path_bdd):

    # item = [disque, nom, launcher, taille ?, annee ?]

    disque = item[0]
    nom = item[1]
    launcher = item[2]
    if len(item) > 3 and item[3]:
        taille = int(item[3])
    else:
        taille = 0
    if len(item) > 4 and item[4]:
        annee = int(item[4])
    else:
        annee = 0

    with open(path_bdd, "r", encoding='utf-8') as file:
        bdd = json.load(file)

    if disque not in bdd:
        return "Erreur : Disque"
    if launcher not in bdd[disque]:
        return "Erreur : Launcher"

    app = {
        "nom": nom,
        "taille": taille,
        "année": annee
    }

    bdd[disque][launcher].append(app)

    with open(path_bdd, "w", encoding='utf-8') as file:
        json.dump(bdd, file, ensure_ascii=False, indent=4)
    print(bdd)

    return "Application ajoutée avec succès"


#%%
'''
supr une app à la bdd
'''


def deleteApp(item, BDD):
    return item


#%%
'''
modifie une app de la bdd
'''


def editApp(item, BDD):
    return ''


#%%

def terminal(cmd, BDD, path_bdd):
    arg1 = ['help', 'print', 'add', 'delete', 'remove']  # Choses possibles
    disques = getDisques(BDD)  # Disques possibles
    print(BDD)

    # Si la commande est vide
    if not cmd:
        return "Entrée vide | Voir help pour plus d'informations"

    try:
        cmds = shlex.split(cmd)
    except ValueError as e:
        return "Erreur : commande invalide | Voir help pour plus d'informations"
        # f"Erreur de parsing de commande : {str(e)}"

    print(f"Commandes : {', '.join(cmds)}")
    print(len(cmds), " Argument(s)")

    if cmds[0] not in arg1:
        return "Erreur : commande invalide | Voir help pour plus d'informations"
    if cmds[0] == "help":
        if len(cmds) > 1 and cmds[1] == "add":
            return ('Utilisation : add app "Disque" "Nom app" "Launcher" (taille en Go) (date)\nUn exemple : add app '
                    '"SSD Main" "Nom app" "Microsoft Store" 42 2005')
        return f"Commandes possibles : {', '.join(arg1)}"
    if cmds[0] == 'print':
        return f"Disques : {', '.join(getDisques(BDD))}"

    # Dictionnaire de commandes
    dico_app_cmds = {
        'add': addApp,
        'delete': deleteApp,
        'remove': deleteApp,
        'edit': editApp
    }
    launchers = [
        "Steam",
        "Epic Games",
        "Battle.net",
        "EA",
        "Ubisoft",
        "Rockstar",
        "Microsoft Store"  # C'est aussi xbox non ?
    ]

    # Vérifier les arguments supplémentaires pour les commandes add, delete et edit
    if cmds[0] in dico_app_cmds:
        if len(cmds) < 3:
            return "Erreur : arguments insuffisants pour la commande | Voir help pour plus d'informations"
        if len(cmds) > 7:
            return "Erreur : trop d'arguments pour la commande | Voir help pour plus d'informations"
        if cmds[1] == "app":
            if cmds[2] not in disques:
                return f"Erreur : Disque '{cmds[2]}' non valide"
            if len(cmds) == 3:
                return f"Erreur : préciser l'app et launcher !"
            if cmds[3] and cmds[3] in launchers:
                return f"Erreur : '{cmds[3]}' est un launcher!"
            if len(cmds) == 4:
                return f"Erreur : préciser le launcher !"

            if cmds[4] and cmds[4] not in launchers:
                return f"Erreur : Launcher '{cmds[4]}' non valide | Voir add launcher"

            if cmds[2] in disques and cmds[3] not in launchers and cmds[4] in launchers and len(cmds) >= 5:
                item = cmds[2:]  # Récupère tous les arguments sauf les deux premiers
                return addApp(item, path_bdd)

            # Si pas de taille/date spécifiée ça mettra 0
            # Si date, mais pas de taille, on met taille à 0 puis la date

            # res = dico_app_cmds[cmds[0]]
            # Un exemple : add app "SSD Main" "Rocket league" "Epic Games" 28 2015

    return "Erreur : commande invalide | Voir help pour plus d'informations"


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
