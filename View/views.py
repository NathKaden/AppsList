'''
interface
ex : /add C Rocket_league Epic_games 28Go 2015

Un launcher comme 'Epic_games' peut être écrit de plusieurs façons différentes :
on le réecrit en 'epicgames' mais quand on demande c'est 'Epic Games'

année facultatif
peut-être une fonction qui le fait pour nous qu'on peut activer dans l'interface finale
Une seule BDD par utilisateur
'''


def terminal():
    arg1 = ['help', 'print', 'add', 'delete', 'edit']  # Choses possibles
    arg2 = ['C', 'D', 'E', 'F', 'G']  # Disques possibles
    # arg = launcher (default : Undefined)
    # arg3 = jeu (default : game)
    # arg4 = taille (default : 0) en Go

    cmd = input("/")
    if cmd == "":
        cmd = "vide"
        return "Erreur : entrée vide"
    else:
        print("Commande : " + "/" + str(cmd))
        cmds = cmd.split(' ')
        print(cmds)
        for i in range(len(cmds)):
            print(cmds[i])
            if cmds[0] in arg1:
                print('argument 1 OK')
                if cmds[1] in arg2:
                    print('argument 2 OK')
                else:
                    return "Erreur : arg2 non valide, doit être : " + str(arg2)
            else:
                return "Erreur : arg1 non valide, doit être : " + str(arg1)


# terminal()
#%%
# print(BDD)
# # print(BDD['SSD']['Steam'])
# print(printGamesList(BDD))