from tkinter import *
from tkinter import ttk
import sv_ttk
import ctypes as ct

app = Tk() #window
app.title("GameList")
app.geometry('750x480')
#window.iconbitmap("./assets/icon.png")
app.config(background="#334")
# Label that act as a "Title" something like an H1
#lbl = Label(app, text="haap", font=("Roboto", 20), bg="#334")
#lbl.grid(column=0, row=0)

# Barres de menu
menu_bar = Menu(app, background='blue', fg='white')
menu_bar.configure(bg="blue",fg="white")
app.config(menu=menu_bar)
# Fichier
fichier_menu = Menu(menu_bar, tearoff=0, background="#334", foreground="white")
menu_bar.add_cascade(label="Fichier",menu=fichier_menu)
fichier_menu.add_command(label="Nouveau",command="")
fichier_menu.add_command(label="Quitter", command=app.quit)
fichier_menu["bg"]="#334"
fichier_menu["activebackground"]="#5ab021"
# Editer
editer_menu = Menu(menu_bar, tearoff=0, background="#334", foreground="white")
menu_bar.add_cascade(label="Editer",menu=editer_menu)
editer_menu.add_command(label="haap",command="")
fichier_menu["bg"]="#334"
fichier_menu["activebackground"]="#5ab021"
# Vue
editer_menu = Menu(menu_bar, tearoff=0, background="#334", foreground="white")
menu_bar.add_cascade(label="Editer",menu=editer_menu)
editer_menu.add_command(label="haap",command="")
fichier_menu["bg"]="#334"
fichier_menu["activebackground"]="#5ab021"
# Commandes
editer_menu = Menu(menu_bar, tearoff=0, background="#334", foreground="white")
menu_bar.add_cascade(label="Editer",menu=editer_menu)
editer_menu.add_command(label="haap",command="")
fichier_menu["bg"]="#334"
fichier_menu["activebackground"]="#5ab021"
# Fin menubar

# Toolbar
toolbar = Frame(app, bg="#223")

insertbutton = Button(toolbar, text="abfezhfezu", command="")
insertbutton.pack(side=LEFT, padx=10, pady=10)

toolbar.pack(side=TOP, fill=X)




#----workflow txt

#root = Tk()
#text = StringVar()
#fr = Frame (root,bg="black")
#fr.grid()
#menu = OptionMenu (fr, text, "hi", "there")
#menu.grid (pady=50, padx=50)
# Pretty colouring goes here
# Or ugly yellow, I don't mind
#menu ["menu"] ["bg"] = "red"
#menu ["bg"] = "blue"
#menu ["activebackground"] = "green"
#---


def dark_title_bar(app):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    app.update()
    dwmwa_use_immersive_dark_mode = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(app.winfo_id())
    rendering_policy = dwmwa_use_immersive_dark_mode
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),ct.sizeof(value))
dark_title_bar(app)

sv_ttk.set_theme("dark")
app.mainloop()