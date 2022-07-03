from tkinter import *


class HSVPanel:

    def __init__(self, container, height, width, relx=0.05, rely=0.1):
        self._container = container
        self.height = height
        self.width = width
        self.relx = relx
        self.rely = rely
        self.inputBox = Frame(master=self._container)
        self.rowLabels = {1: 'H Lower ', 2: 'S Lower ', 3: 'V Lower ', 4: 'H Upper ', 5: 'S Upper ', 6: 'V Upper '}

    def createSliders(self):
        self.inputBox.place(relx=self.relx, rely=self.rely, relwidth=self.width, relheight=self.height)
        self.inputBox.columnconfigure(0, weight=1)
        self.inputBox.columnconfigure(1, weight=6)
        Label(self.inputBox, text="HSV Parameters", font=('Helvatical bold', 20)).grid(row=0, columnspan=2, sticky=EW)
        sliders = []
        for row in range(1, 7):
            sliders.append(self._createSlider(row, self.rowLabels.get(row)))
        return sliders

    def _createSlider(self, row, inputText):
        slider = Scale(self.inputBox, from_=0, to=255, orient="horizontal", length=250)
        slider.grid(row=row, column=1, sticky=EW, pady=10)
        Label(self.inputBox, text=inputText, font=('Helvatical bold', 15)).grid(row=row, column=0)
        return slider



