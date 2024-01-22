import json
import os

#%%
# loadBDD
def loadBDD(path):
    fichier = open(path,"r",encoding='utf-8')
    BDD = json.load(fichier)
    fichier.close()
    return BDD

path = "./BDDTest.json"
BDD = loadBDD(path)
print(BDD,type(BDD))

#%%
'''
modifie la BDD si c'est bien un json
ex : ./BDDTest.json
'''
def editBDD(*args):
    if args == ():
        print('Args vide')
        path = input("Indiquer le chemin d'accès (exemple : './BDDTest.json') :")
    else:
        path=args
    if path=="":
        path="vide"
    print("Entrée :",path)
    if path[-5:]=='.json':
        print('Le fichier est bien un json')
        if os.path.exists(path):
            print('Le fichier existe')
            print('Chargement de la base de données')
            loadBDD(path)
            print('Fichier chargé avec succès')
            print(BDD)
    else:return "Erreur : Merci de mettre un fichier json."

#test :
#editBDD()

#%%
################ GETTERS ################
'''
Retourne les disques de la BDD
'''
def getDisques():
    return list(BDD.keys())
print((getDisques()))

#%%
'''
Retourne les launchers
'''
def getLaunchers():
    r={}
    for cle in getDisques():
        r[cle]=list(BDD[cle].keys())
    return r

print(getLaunchers())
#{'SSD main': ['Epic Games', 'Steam'], 'SSD Sam': ['Battle.net', 'EA']}

#%%
'''
Retourne les jeux de la BDD
'''
def getGames():
    r=[]
    for c in getDisques():
        r += BDD[c].keys()
    return r
print(getGames())

#%%
################ FONCTIONS PRINCIPALES ################
def printGamesList(BDD):
    res=''
    #for cle in BDD:
    #    res+=BDD[cle]
    #
    #    for cle2 in Steam:
    #        res+=BDD[cle2]
    return BDD

#%%
'''
ajoute un jeu à la BDD
'''
def addGame(item,BDD):
    return ''

#%%
'''
supr un jeu à la BDD
'''
def delete(item,BDD):
    return ''

#%%
'''
modifie un jeu de la BDD
'''
def edit(item,BDD):
    return ''

#%%