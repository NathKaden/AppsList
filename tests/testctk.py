# -*- coding: utf-8 -*-

import tkinter as tk
import customtkinter
import os
import sys

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title("GameList")
app.geometry('750x480')
app.config(background="#33333F")

def afficher_boutons():
    global bouton_ouvrir, bouton_enregistrer, bouton_quitter, afficher
    # Basculer entre l'affichage et le masquage des boutons
    if afficher:
        bouton_ouvrir.pack_forget()
        bouton_enregistrer.pack_forget()
        bouton_quitter.pack_forget()
        afficher = False
    else:
        bouton_ouvrir.pack(side=tk.TOP, padx=0, pady=0)
        bouton_enregistrer.pack(side=tk.TOP, padx=0, pady=0)
        bouton_quitter.pack(side=tk.TOP, padx=0, pady=0)
        afficher = True

def button_function():
    print("button pressed")

def exit_app():
    app.destroy()  # Ferme l'application tkinter
    sys.exit()     # Ferme le script Python, ce qui devrait fermer le terminal

# Création d'un cadre pour contenir les boutons et les aligner à droite
button_frame = customtkinter.CTkFrame(app)
button_frame.pack(side="top", fill="x", padx=0, pady=0)  # Place le cadre en haut à droite
button_frame.configure(fg_color="#2B2B3B", border_width=0, corner_radius=0)  # Définit la couleur de fond du cadre

# Utilisez CTkButton au lieu de Button tkinter
Fichier_btn = customtkinter.CTkButton(master=button_frame, text="Fichier", fg_color="#2F2F3F", border_width=0, corner_radius=0, command=afficher_boutons)
Fichier_btn.pack(side="left", padx=0, pady=0)  # Place le bouton à gauche dans le cadre

Quit_btn = customtkinter.CTkButton(master=button_frame, text="Quitter", command=exit_app)
Quit_btn.pack(side="right", padx=0, pady=0)  # Place le bouton à droite dans le cadre
Quit_btn.configure(fg_color="#2F2F3F", border_width=0, corner_radius=0)  # Définit la couleur de fond du bouton et enlève les bords arrondis

# Création d'un nouveau cadre pour les boutons "Ouvrir", "Enregistrer" et "Quitter"
sub_button_frame = customtkinter.CTkFrame(app)
sub_button_frame.pack(side="top", fill="x", padx=0, pady=0)  # Place le cadre en dessous du bouton "Fichier"
sub_button_frame.configure(fg_color="#2B2B3B", border_width=0, corner_radius=0)  # Définit la couleur de fond du cadre

# Création des boutons "Ouvrir", "Enregistrer" et "Quitter" masqués par défaut
bouton_ouvrir = customtkinter.CTkButton(master=sub_button_frame, text="Ouvrir", command=button_function)
bouton_enregistrer = customtkinter.CTkButton(master=sub_button_frame, text="Enregistrer", command=button_function)
bouton_quitter = customtkinter.CTkButton(master=sub_button_frame, text="Quitter", command=exit_app)
bouton_ouvrir.pack_forget()
bouton_enregistrer.pack_forget()
bouton_quitter.pack_forget()

# Ajout d'un espaceur à droite pour pousser les boutons vers la gauche
spacer = customtkinter.CTkLabel(master=sub_button_frame, text="", fg_color="#2B2B3B")
spacer.pack(side="right", fill="both", expand=True)

# Variable pour suivre l'état d'affichage des boutons
afficher = False

app.mainloop()
