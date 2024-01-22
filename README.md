# AppsList
A python program that allows you to make your list of your games.

## Description
Un programme qui permet de mettre tous ses jeux et applications dans une liste :  

`/ajout help {add, del, print} {C, D, E} {jeu.toString}`
`/ajout C Rocket_league 28Go Epic_games`

## Features
- [X] 🗄️ Base de données de test
- [X] 🌙 Dark theme
- [ ] 🖱️ Menu bar
- [ ] 📝 Fonctions
  - [ ] 🔗

## Interface prévue
```
------------------------------------------------
Fichier | Editer | Vue | BDD.json | 8 jeux
------------------------------------------------

SSD main (C:) [] :eg: | Rocket_League | 24 Go | 2015
[]
[]
[]
[ Ajouter un jeu ]
------------------------------------------------
[] SSD main (C:) | [] SSD sam (:D)
```
<br><br>  
>[!NOTE]
>Ce qui suit correspond uniquement au développement de l'application

### En-tête :
Fichier {ouvrir, sauvegarder, ouvrir l'emplacement, quitter}  
Edit {copy, paste, find (deplacerjeu)}  
Vue {liste, tri, thèmes, langue}  
Autres {Commande (terminal), GitHub, crédits}  

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
