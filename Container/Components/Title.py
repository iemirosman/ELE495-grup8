from tkinter import *


class Title:
    def __init__(self, container, height, width, relx=0.1, rely=0.04):
        self._container = container
        self.height = height
        self.width = width
        self.relx = relx
        self.rely = rely

    def addTitle(self, titleText):
        title = Frame(master=self._container)
        title.place(relx=self.relx, rely=self.rely, relwidth=self.width, relheight=self.height)
        titleLabel = Label(title, text=titleText, font=('Helvatical bold',40))
        titleLabel.pack()

