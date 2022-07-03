from tkinter import *
from PIL import Image, ImageTk
from Components.Title import Title
from Components.HSVCtrlPanel import HSVPanel
from Components.RadiusCtrlPnl import RadiusPanel
from Components.Cam import Cam
from Components.PIDCtrlPanel import PIDPanel
from Components.SizeCtrlPnl import SizePanel
from Components.ProfilePanel import ProfilePanel
from POJOs.Options import PROFILES
import cv2 as cv2


class ControlPanel:
    def __init__(self, profile):
        self.mainWindow = Tk()
        self._initProfile = profile
        self._thresholds = []
        self._radius = []
        self._size = Entry()
        self._InnerPID = []
        self._OuterPID = []
        self._camRaw = Label()
        self._camMasked = Label()
        self._profile = Entry()
        self._button = Button()
        self._createCanvas()
        self._addTitle()
        self._addHSVCtrlPnl()
        self._addRadiusCtrlPnl()
        self._addSizeCtrlPnl()
        self._addInnerPID()
        self._addOuterPID()
        self._addCamRaw()
        self._addCamMasked()
        self._addButton()

    def openControlPanel(self):
        self.mainWindow.title('Control Panel')
        return self.mainWindow

    def getH(self):
        hLowerThreshold = self._thresholds[0].get()
        hUpperThreshold = self._thresholds[3].get()
        return hLowerThreshold, hUpperThreshold

    def getS(self):
        sLowerThreshold = self._thresholds[1].get()
        sUpperThreshold = self._thresholds[4].get()
        return sLowerThreshold, sUpperThreshold

    def getV(self):
        vLowerThreshold = self._thresholds[2].get()
        vUpperThreshold = self._thresholds[5].get()
        return vLowerThreshold, vUpperThreshold

    def getRadius(self):
        minRadius = self._radius[0].get()
        maxRadius = self._radius[1].get()
        return minRadius, maxRadius

    def getSize(self):
        try:
            size = int(self._size.get())
        except ValueError:
            size = PROFILES[self._initProfile]['Size']
        return size

    def getInnerPID(self):
        try:
            P = float(self._InnerPID[0].get())
            I = float(self._InnerPID[1].get())
            D = float(self._InnerPID[2].get())

        except ValueError:
            P = PROFILES[self._initProfile]['InnerPID']['P']
            I = PROFILES[self._initProfile]['InnerPID']['I']
            D = PROFILES[self._initProfile]['InnerPID']['D']
            print('Please enter inner PID parameters')
        return P, I, D

    def getOuterPID(self):
        try:
            P = float(self._OuterPID[0].get())
            I = float(self._OuterPID[1].get())
            D = float(self._OuterPID[2].get())
        except ValueError:
            P = PROFILES[self._initProfile]['OuterPID']['P']
            I = PROFILES[self._initProfile]['OuterPID']['I']
            D = PROFILES[self._initProfile]['OuterPID']['D']
            print('Please enter inner PID parameters')
        return P, I, D

    def camRawStream(self):
        return self._camRaw

    def camMaskedStream(self):
        return self._camMasked

    def _getProfile(self):
        newProfile = self._profile.get()
        print(newProfile)
        if newProfile in PROFILES.keys():
            self._initProfile = newProfile
            self._setProfileHSV()
            self._setProfileRadius()
            self._setProfileInnerPID()
            self._setProfileOuterPID()
            self._setProfileSize()

    # def _setInnerPID(self, P, I, D):
    #     self._clearInnerPID()
    #     self._InnerPID[0].insert(0, P)
    #     self._InnerPID[1].insert(0, I)
    #     self._InnerPID[2].insert(0, D)
    #
    # def _setOuterPID(self, P, I, D):
    #     self._clearOuterPID()
    #     self._OuterPID[0].insert(0, P)
    #     self._OuterPID[1].insert(0, I)
    #     self._OuterPID[2].insert(0, D)

    def _createCanvas(self, height=1000, width=1500):
        Canvas(self.mainWindow, height=height, width=width).pack()

    def _addTitle(self, text='Control Panel', height=0.1, width=0.8):
        Title(self.mainWindow, height, width).addTitle(text)

    def _addHSVCtrlPnl(self):
        self._thresholds = HSVPanel(self.mainWindow, 0.6, 0.3, rely=0.15).createSliders()
        self._setProfileHSV()

    def _addRadiusCtrlPnl(self):
        self._radius = RadiusPanel(self.mainWindow, 0.4, 0.3, rely=0.7).createSliders()
        self._setProfileRadius()

    def _addSizeCtrlPnl(self):
        self._size = SizePanel(self.mainWindow, 0.4, 0.2, relx=0.8, rely=0.7).createEntry('Object Size')
        self._setProfileSize()

    def _addInnerPID(self):
        self._InnerPID = PIDPanel(self.mainWindow, 0.4, 0.2, relx=0.38, rely=0.7).createEntries('Inner PID Parameters')
        self._setProfileInnerPID()

    def _addOuterPID(self):
        self._OuterPID = PIDPanel(self.mainWindow, 0.4, 0.2, relx=0.58, rely=0.7).createEntries('Outer PID Parameters')
        self._setProfileOuterPID()

    def _addCamRaw(self):
        self._camRaw = Cam(self.mainWindow, 0.31, 0.21, relx=0.4).addCam()

    def _addCamMasked(self):
        self._camMasked = Cam(self.mainWindow, 0.31, 0.21, relx=0.7).addCam()

    def _addButton(self):
        self._profile, self._button = ProfilePanel(self.mainWindow, 0.4, 0.3, relx=0.8, rely=0.79).createEntry(self._getProfile, 'Profile')

    def _setProfileHSV(self):
        idxThreshold = 0
        for threshold in PROFILES[self._initProfile]['HSV']:
            self._thresholds[idxThreshold].set(PROFILES[self._initProfile]['HSV'][threshold])
            idxThreshold += 1

    def _setProfileInnerPID(self):
        self._clearInnerPID()
        idxPID = 0
        for param in PROFILES[self._initProfile]['InnerPID']:
            self._InnerPID[idxPID].insert(END, PROFILES[self._initProfile]['InnerPID'][param])
            idxPID += 1

    def _setProfileOuterPID(self):
        self._clearOuterPID()
        idxPID = 0
        for param in PROFILES[self._initProfile]['OuterPID']:
            self._OuterPID[idxPID].insert(END, PROFILES[self._initProfile]['OuterPID'][param])
            idxPID += 1

    def _setProfileRadius(self):
        self._radius[0].set(PROFILES[self._initProfile]['Radius']['minRadius'])
        self._radius[1].set(PROFILES[self._initProfile]['Radius']['maxRadius'])

    def _setProfileSize(self):
        self._clearSize()
        self._size.insert(END, PROFILES[self._initProfile]['Size'])

    def _clearInnerPID(self):
        for PID in range(len(self._InnerPID)):
            self._InnerPID[PID].delete(0, END)

    def _clearOuterPID(self):
        for PID in range(len(self._OuterPID)):
            self._OuterPID[PID].delete(0, END)

    def _clearSize(self):
        self._size.delete(0, END)
