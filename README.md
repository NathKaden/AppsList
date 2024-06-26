# 📜 AppsList
### An app that allows you to make your list of your apps.

## 🖋️ Description
**Une application qui permet de mettre tous ses jeux et applications dans une liste**  

## ✨ Features
- [X] 📦 Base de données de test
- [X] 🌙 Dark theme
- [ ] ⚙️ Menu bar (haut) (80%)
- [ ] ⚙️ Menu bar (bas)
- [ ] 📜 Fonctions
  - [ ] 📎 Fichiers
  - [ ] 📎 Editer

## 📁 Fonctionnement des dossiers

Le `main.py` est le fichier principal, l'application. C'est la dernière meilleure version de l'application.  
Le dossier `ver/` contient les versions de l'application, à chaque fonctionnalité, une version est ajoutée.
Le dossier `tests/` est le "bac à sable" de l'application, c'est là qu'on fait nos tests et où on développe nos trucs.

## 🖥️ Interface prévue
![Voir image](https://github.com/NathKaden/AppsList/blob/main/assets/maquette.png)
>Note :
>Ligne d'une app : logo launcher | jeu | taille | année de sortie

### En-tête :
Fichier {ouvrir, sauvegarder, ouvrir l'emplacement, quitter}  
Edit {copier, coller, trouver (deplacerjeu)}  
Vue {liste, tri, thèmes, langue}  
Autres {Commande (terminal), GitHub, crédits}

## Terminal :
Synthaxe : `/ajout help {add | del | print} {C | D | E} {app.toString}`  

Exemple : `/ajout C Rocket_league 28Go Epic_games`

<br>

>[!NOTE]
>Ce qui suit correspond uniquement au développement de l'application

## 🗄️ Description de la base de données :
Une base de données a :  
Des disques qui ont  
des launchers qui ont  
des jeux ou application qui ont  
un nom, une taille, et une année de sortie.  

## 🔗 Fonctions :
- loadBDD(path)
- editBDD(*args)
- getters :
  - getDisques()
  - getLaunchers()
  - getGames()
- terminal()
- printGamesList() (toString)
- addGame()
- addLauncher()
fonction pour modifier le launcher d'un jeu  
fonction deplacer(jeu) de disque  
fonction ajouter un jeu ouvre une petite fenêtre pour ajouter un jeu  
fonction verifLauncher qui prend en paramètre un launcher qui le remet en bien écrit  

### Fonctionnement lors de l'ouverture :
Sauvegarde dans un fichier `settings.json` pour savoir où est la dernière bdd chargée.
  Si c'est vide c'est que aucune bdd n'a encore été chargée.
  Dans ce cas création d'une BDD vide.
La bdd par défaut se nomme BDD.json

>Charger la bdd si aucune chargée depuis sauvegarde écrite dans `settings.json`
> -> Utilisation de la fonction `loadBDD`
<br>

La fonction `actualiser()` : actualisera le nombre d'applications, elle sera appellée à chaque changement.  
- Écrit la bdd chargée en haut à droite dans la même ligne que fichier  
- Écrit le nbre de jeux dans la bdd

## N'est pas compris dans l'objectif principal :
- Fonction qui permet de prendre une application en cours et de l'ajouter à la liste
- Un thème clair

