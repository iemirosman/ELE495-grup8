from tkinter import *


class ProfilePanel:

    def __init__(self, container, height, width, relx=0.3, rely=0.1):
        self._container = container
        self.height = height
        self.width = width
        self.relx = relx
        self.rely = rely
        self.inputBox = Frame(master=self._container)
        self.clicked = StringVar()

    def createEntry(self, callbackFunc, title):
        self.inputBox.place(relx=self.relx, rely=self.rely, relwidth=self.width, relheight=self.height)
        entry = self._createEntry()
        submitButton = self._createButton(callbackFunc)
        Label(self.inputBox, text=title, font=('Helvatical bold', 20)).grid(row=0, columnspan=2, sticky=EW)
        return entry, submitButton

    def _createEntry(self):
        entry = Entry(self.inputBox)
        entry.grid(row=1, column=0)
        return entry

    def _createButton(self, func):
        button = Button(self.inputBox, text='Submit', command=func)
        button.grid(row=1, column=1)
        return button
