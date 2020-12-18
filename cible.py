from robot import Robot
from matplotlib.animation import FuncAnimation
from random import randint
import math


class Cible(Robot):
    def __init__(self, x, y, theta, ax, color, vmax=1., tacc=2., te=0.005, pattern="ligne"):
        Robot.__init__(self, x, y, theta, ax, color, vmax, tacc, te, 1)
        self.__t = 0
        self.__pattern = (pattern in ["ligne", "cercle", "huit", "random", "custom", "control"]) and pattern or "ligne"
        self.leftKey = False
        self.rightKey = False
        self.__theta0 = theta
        self.eightState = 0

    def avancer(self):
        self.__t += 1
        if self.__pattern == "ligne":
            self._changerVitesseRoues(1, 1)

        elif self.__pattern == "cercle":
            if self._v < self._vmax/2:
                self._changerVitesseRoues(1, 1)
            else:
                self._changerVitesseRoues(0, 1)

        elif self.__pattern == "huit":
            if self.eightState == 0:
                if self._v < self._vmax/2:
                    self._changerVitesseRoues(1, 1)
                else:
                    self._changerVitesseRoues(0, 1)
                    self.eightState += (0 < self._deltaErreur(self._theta, self.__theta0) < 4) and 1
            elif self.eightState == 1:
                if self._v > self._vmax/2:
                    self._changerVitesseRoues(0, -1)
                else:
                    self.eightState += 1
            elif self.eightState == 2:
                self._changerVitesseRoues(1, 0)
                self.eightState += (-4 < self._deltaErreur(self._theta, self.__theta0) < 0) and 1
            elif self.eightState == 3:
                if self._v > self._vmax/2:
                    self._changerVitesseRoues(-1, 0)
                else:
                    self.eightState += 1
            elif self.eightState == 4:
                self._changerVitesseRoues(0, 1)
                self.eightState = (0 < self._deltaErreur(self._theta, self.__theta0) < 4) and 1 or self.eightState

        elif self.__pattern == "random":
            self._changerVitesseRoues(randint(-1, 1), randint(-1, 1))

        elif self.__pattern == "custom":
            self.__t = self.__t + 1
            if self.__t < 1000:
                self._changerVitesseRoues(1,1)
            elif self.__t > 1000 and self.__t < 1050:
                self._changerVitesseRoues(-1,-1)
            elif self.__t > 1050 and self.__t < 1150:
                self._changerVitesseRoues(1,0)
            elif self.__t > 1150 and self.__t < 2150:
                self._changerVitesseRoues(1,1)
            elif self.__t > 2150 and self.__t < 2200:
                self._changerVitesseRoues(-1,-1)
            elif self.__t > 2200 and self.__t < 2300:
                self._changerVitesseRoues(0,1)
            elif self.__t > 2300 and self.__t < 3300:
                self._changerVitesseRoues(1,1)
            elif self.__t > 3300 and self.__t < 3350:
                self._changerVitesseRoues(-1,-1) 
            elif self.__t == 3450:
                self.__t = 0
            elif self.__t > 3350:
                self._changerVitesseRoues(0,1)
        
        elif self.__pattern == "control":
            (not self.leftKey) and (not self.rightKey) and self._changerVitesseRoues(1, 1)
            (self.leftKey) and (not self.rightKey) and self._changerVitesseRoues(-1, 0)
            (not self.leftKey) and (self.rightKey) and self._changerVitesseRoues(0, -1)
            (self.leftKey) and (self.rightKey) and self._changerVitesseRoues(-1, -1)