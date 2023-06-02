# Ce prototype met en oeuvre la création d'une image pixel par pixel
# à travers une interface graphique en utilisant "tkinter/Canvas"
# Cependant l'experience montre que la solution n'est pas adaptée car elle prend
# un certains temps (en occurence 4 à 5 sec) car la librairie n'est pas faite 
# pour une telle utilisation.

import tkinter as tki

WIDTH,HEIGHT = 800,600

# Méthode pour formater la couleur au format hexadécimal : r,g,b => "#RRGGBB"
def setColor (r:int, g:int, b:int) -> str :
    retour = "#" + "{:02x}".format(r)+ "{:02x}".format(g) + "{:02x}".format(b)
    return retour

mainWindow = tki.Tk()
mainWindow.title("RayTracer !")

cvs = tki.Canvas(mainWindow, background="black", height=HEIGHT, width=WIDTH, name="fenêtre de rendu")
img = tki.PhotoImage(width=WIDTH, height=HEIGHT)

# Remplissage de la grille
for y in range(HEIGHT):
    for x in range(WIDTH):
        R = x % 256
        G = (x+y) % 256
        B = y % 256
        color = setColor(R,G,B)
        img.put(color, (x,y))

cvs.create_image((WIDTH/2,HEIGHT/2),image=img)
# Affichage
cvs.pack()
mainWindow.mainloop()

