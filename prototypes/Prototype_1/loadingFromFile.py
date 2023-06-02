# Ce prototype met en oeuvre l'affichage d'une image au format 'bmp'
# 

from PIL import Image, ImageTk
from tkinter import Tk, Canvas

mainWindow = Tk()
mainWindow.title(string='Ray-Tracer')

img_tk = ImageTk.PhotoImage(Image.open('image.bmp'))

cvs = Canvas(master=mainWindow,name="rendu", height=img_tk.height(),width=img_tk.width())
cvs.create_image(img_tk.width()/2,img_tk.height()/2,image=img_tk)

cvs.pack()
mainWindow.mainloop()
