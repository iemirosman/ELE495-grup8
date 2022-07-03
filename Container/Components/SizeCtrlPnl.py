from tkinter import *


class SizePanel:

    def __init__(self, container, height, width, relx=0.3, rely=0.1):
        self._container = container
        self.height = height
        self.width = width
        self.relx = relx
        self.rely = rely
        self.inputBox = Frame(master=self._container)
        self.rowLabels = {1: 'P ', 2: 'I ', 3: 'D '}

    def createEntry(self, title):
        self.inputBox.place(relx=self.relx, rely=self.rely, relwidth=self.width, relheight=self.height)
        entry = self._createEntry()
        Label(self.inputBox, text=title, font=('Helvatical bold', 20)).grid(row=0, columnspan=2, sticky=EW)
        return entry

    def _createEntry(self):
        entry = Entry(self.inputBox)
        entry.grid(row=1, column=0, sticky=E, pady=10)
        Label(self.inputBox, text='cm', font=('Helvatical bold', 15)).grid(row=1, column=1)
        return entry
