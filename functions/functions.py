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
    # Un exemple : add "SSD Main" app "Rocket league" "Epic Games" 28 2015
    # 28 Go et année 2015 facultatif
    # item = [disque, launcher, app, taille?, annee?]

    # with open(self.settings["path_bdd"], "r", encoding='utf-8') as file:
    #     BDD = json.load(file)

    if item[3] in item and item[4] in item:
        app = {
            "nom": item[2],
            "taille": item[3],
            "année": item[4]
        }
    # BDD[disque][launcher].append(app)

    # with open("bdd.json", "w", encoding='utf-8') as file:
    #     json.dump(BDD, file, ensure_ascii=False, indent=4)
    return 'add'


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

def terminal(cmd, BDD):
    arg1 = ['help', 'print', 'add', 'delete']  # Choses possibles
    disques = getDisques(BDD)  # Disques possibles

    # Si la commande est vide
    if cmd == "":
        return "Entrée vide | Voir help pour plus d'informations"

    cmds = shlex.split(cmd)
    print(f"Commandes : {', '.join(cmds)}")
    print(len(cmds), " Argument(s)")

    if cmds[0] not in arg1:
        return "Erreur : commande invalide | Voir help pour plus d'informations"
    if cmds[0] == "help":
        return f"Commandes possibles : {', '.join(arg1)}"
    if cmds[0] == 'print':
        return f"Disques : {', '.join(getDisques(BDD))}"

    # Dictionnaire de commandes
    dico_app_cmds = {
        'add': addApp,
        'delete': deleteApp,
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
        # for arg in cmds[1:]:

        if cmds[1] and cmds[1] == "app":
            if cmds[2] and cmds[2] not in disques:
                return f"Erreur : Disque '{cmds[2]}' non valide"
            if cmds[3] and cmds[3] in launchers:
                return f"Erreur : Launcher '{cmds[3]}' n'est pas une app!"
            if cmds[4] and cmds[4] not in launchers:
                return f"Erreur : Launcher '{cmds[3]}' non valide | Voir add launcher"

            if cmds[2] in disques and cmds[3] not in launchers and cmds[4] in launchers:
                return "Commande Ok"

            # res = dico_app_cmds[cmds[0]]
            # Un exemple : add app "SSD Main" "Rocket league" "Epic Games" 28 2015


            return "c pa bon"
        return "c pa bon"



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
