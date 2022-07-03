from tkinter import *


class PIDPanel:

    def __init__(self, container, height, width, relx=0.3, rely=0.1):
        self._container = container
        self.height = height
        self.width = width
        self.relx = relx
        self.rely = rely
        self.inputBox = Frame(master=self._container)
        self.rowLabels = {1: 'P ', 2: 'I ', 3: 'D '}

    def createEntries(self, title):
        self.inputBox.place(relx=self.relx, rely=self.rely, relwidth=self.width, relheight=self.height)
        Label(self.inputBox, text=title, font=('Helvatical bold', 20)).grid(row=0, columnspan=2, sticky=EW)
        entries = []
        for row in range(1, 4):
            entries.append(self._createEntry(row, self.rowLabels.get(row)))
        return entries

    def _createEntry(self, row, inputText):
        entry = Entry(self.inputBox)
        entry.grid(row=row, column=1, sticky=E, pady=10)
        Label(self.inputBox, text=inputText, font=('Helvatical bold', 15)).grid(row=row, column=0)
        return entry

