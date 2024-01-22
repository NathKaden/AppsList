# 📜 AppsList
A python program that allows you to make your list of your games.

## 🖋️ Description
Un programme qui permet de mettre tous ses jeux et applications dans une liste :  

`/ajout help {add, del, print} {C, D, E} {jeu.toString}`
`/ajout C Rocket_league 28Go Epic_games`

## ✨ Features
- [X] 📦 Base de données de test
- [X] 🌙 Dark theme
- [ ] ⚙️ Menu bar
- [ ] 📜 Fonctions
  - [ ] 📎 Fichiers
  - [ ] 📎 Editer
     

## Interface prévue
```
--------------------------------------------------------------
Fichier | Editer | Vue | Autres             BDD.json | 8 apps
--------------------------------------------------------------

SSD main (C:) [] :eg: | Rocket_League | 24 Go | 2015
              []
              []
              []
              [ Ajouter un jeu ]

--------------------------------------------------------------
[] SSD main (C:) | [] SSD sam (:D)
```
>Remarques :  
>[] : Bordure épaisse colorée par disques (rouge, vert, bleu etc)  
>Ligne d'une app : logo launcher | jeu | taille | année de sortie

### En-tête :
Fichier {ouvrir, sauvegarder, ouvrir l'emplacement, quitter}  
Edit {copy, paste, find (deplacerjeu)}  
Vue {liste, tri, thèmes, langue}  
Autres {Commande (terminal), GitHub, crédits}

<br>

>[!NOTE]
>Ce qui suit correspond uniquement au développement de l'application

## Description de la base de données :
Une base de données a :  
Des disques qui ont  
des launchers qui ont  
des jeux ou application qui ont  
un nom, une taille, et une année de sortie.  

## Fonctions :
- loadBDD(path)
- editBDD(*args)
- getDisques()
- getLaunchers()
- getGames()
- printGamesList() (toString)
- addGame()
- addLauncher()
- terminal()
fonction pour modifier le launcher d'un jeu
fonction deplacer(jeu) de disque
fonction ajouter un jeu ouvre une petite fenêtre pour ajouter un jeu
fonction verifLauncher qui prend en paramètre un launcher qui le remet en bien écrit

### Fonctionnement lors de l'ouverture :
Sauvegarde dans un fichier `last.json` pour savoir où est la dernière bdd chargée.
  Si c'est vide c'est que aucune bdd n'a encore été chargée.
  Dans ce cas création d'une BDD vide.
La bdd par défaut se nomme BDD.json

Charger la bdd si aucune chargée depuis sauvegarde écrite dans `last.json`
>-> `loadBDD`
<br>

La fonction `actualiser()` : actualisera le nombre d'applications, elle sera appellée à chaque changement.  
- Écrit la bdd chargée en haut à droite dans la même ligne que fichier  
- Écrit le nbre de jeux dans la bdd

## N'est pas compris dans l'objectif principal :
Fonction qui permet de prendre une application en cours et de l'ajouter à la liste

