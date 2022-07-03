from tkinter import *


class Cam:
    def __init__(self, container, height, width, relx=0.3, rely=0.15):
        self._container = container
        self.height = height
        self.width = width
        self.relx = relx
        self.rely = rely
        self.camBox = Label(master=self._container)

    def addCam(self):
        self.camBox.place(relx=self.relx, rely=self.rely, relwidth=self.width, relheight=self.height)
        # Label(self.camBox, text='titleText', font=('Helvatical bold', 20))
        return self.camBox

