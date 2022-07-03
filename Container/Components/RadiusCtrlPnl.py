from tkinter import *


class RadiusPanel:

    def __init__(self, container, height, width, relx=0.05, rely=0.1):
        self._container = container
        self.height = height
        self.width = width
        self.relx = relx
        self.rely = rely
        self.inputBox = Frame(master=self._container)
        self.rowLabels = {1: 'Min Radius ', 2: 'Max Radius '}

    def createSliders(self):
        self.inputBox.place(relx=self.relx, rely=self.rely, relwidth=self.width, relheight=self.height)
        self.inputBox.columnconfigure(0, weight=1)
        self.inputBox.columnconfigure(1, weight=6)
        Label(self.inputBox, text="Radius Parameters", font=('Helvatical bold', 20)).grid(row=0, columnspan=2, sticky=EW)
        sliders = []
        for row in range(1, 3):
            sliders.append(self._createSlider(row, self.rowLabels.get(row)))

        return sliders

    def _createSlider(self, row, inputText):
        slider = Scale(self.inputBox, from_=0, to=250, orient="horizontal", length=250)
        slider.grid(row=row, column=1, sticky=EW, pady=10)
        Label(self.inputBox, text=inputText).grid(row=row)
        return slider
