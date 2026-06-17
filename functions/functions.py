import json
import os
import shlex
from models import Database

# Resolve path_settings relative to this file's location
path_settings = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets",
        "settings.json"
    )
)

def get_color(index):
    with open(path_settings, "r", encoding='utf-8') as file:
        colorsload = json.load(file)
    colors = colorsload["colors"]
    return colors[index % len(colors)]

def get_launchers_config():
    with open(path_settings, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data.get("launchers", {})

# Delegated getters for backward compatibility
def getDisques(db):
    return db.get_disques()

def getLaunchers(db):
    return db.get_launchers()

def getApps(db):
    apps = []
    for disk in db.disks.values():
        for launcher in disk.launchers.values():
            for app in launcher.apps:
                apps.append({"nom": app.name, "taille": app.size, "année": app.year})
    return apps

def getOccurApps(db, nom, tab=False):
    return db.get_occurrences_count(nom, return_list=tab)

def getNbDisques(db):
    return len(db.disks)

def getNbLaunchers(db):
    return len(db.get_launchers())

def getNbApps(db):
    return db.get_apps_count()

def terminal(cmd, db, path_bdd):
    print(db.get_occurrences_count("Ratchet"))
    arg1 = ['help', 'print', 'add', 'delete', 'remove']  # Choses possibles
    disques = db.get_disques()  # Disques possibles
    print(db)

    # Si la commande est vide
    if not cmd:
        return "Entrée vide | Voir help pour plus d'informations"

    try:
        cmds = shlex.split(cmd)
    except ValueError as e:
        return "Erreur : commande invalide | Voir help pour plus d'informations"

    print(f"Commandes : {', '.join(cmds)}")
    print(len(cmds), " Argument(s)")

    if cmds[0] not in arg1:
        return "Erreur : commande invalide | Voir help pour plus d'informations"
    if cmds[0] == "help":
        if len(cmds) > 1:
            if cmds[1] == "add":
                return (
                    'Utilisation : add app "Disque" "Nom app" "Launcher" (taille en Go) (date)\nUn exemple : add app '
                    '"SSD Main" "Nom app" "Microsoft Store" 42 2005')
            if cmds[1] == "delete" or cmds[1] == "remove":
                return (
                    'Utilisation : delete app "Nom app" ou remove app "Nom app"\n'
                    'Un exemple : delete app "Celeste"'
                )
        return f"Commandes possibles : {', '.join(arg1)}"
    if cmds[0] == 'print':
        return f"Disques : {', '.join(db.get_disques())}"

    # Load launchers list dynamically from settings.json
    launchers = list(get_launchers_config().keys())

    # Vérifier les arguments pour les commandes add, delete
    if cmds[0] == 'add':
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
                item = cmds[2:]
                nom = item[1]
                launcher = item[2]
                try:
                    taille = float(item[3]) if len(item) > 3 and item[3] else 0.0
                except ValueError:
                    taille = 0.0
                try:
                    annee = int(item[4]) if len(item) > 4 and item[4] else 0
                except ValueError:
                    annee = 0
                return db.add_app(cmds[2], launcher, nom, taille, annee)

    if cmds[0] in ('delete', 'remove'):
        if len(cmds) < 3:
            return "Erreur : arguments insuffisants pour la commande | Voir help pour plus d'informations"
        if cmds[1] == "app":
            occur = db.get_occurrences_count(cmds[2], return_list=True)
            if len(occur) > 1:
                return f"Errreur : préciser le launcher car {occur} occurrences trouvées pour {cmds[2]}"
            if len(occur) == 1:
                return db.delete_app(cmds[2])

    return "Erreur : commande invalide | Voir help pour plus d'informations"

print("Fonctions lues")
