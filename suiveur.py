from robot import Robot
from cible import Cible
import math
from collections import namedtuple

Erreurs = namedtuple("Erreurs", ["XY", "TH", "X", "Y", "V", "W", "LYA", "U1", "U2", "VC", "WC", "VS", "WS"])

class Suiveur(Robot):

    def __init__(self, x, y, theta, ax, color, cible):
        Robot.__init__(self, x, y, theta, ax, color, cible._vmax, cible._tacc, cible._te, 0.8)
        self.__cible = cible
        self.__e1, self.__e2, self.__e3 = 0., 0., 0.
        self.__k1, self.__k2, self.__k3 = 0., 0., 0.
        self.__u1, self.__u2 = 0., 0.
        self.__zeta = 0.5 # 0 <= zeta <= 1
        self.__b = 1. # b > 0
        self.__updateTrackingError()

    def suivre(self):
        self.__updateTrackingError()

        self.__u1 = -self.__k1*self.__e1
        self.__u2 = (self.__e3 != 0) and -self.__k2*self.__cible._v*(math.sin(self.__e3)/self.__e3)*self.__e2 - self.__k3*self.__e3 or 0

        newV = self.__cible._v*math.cos(self.__e3) - self.__u1
        newW = self.__cible._w - self.__u2
        
        self._commande(newV, newW)
    
    def handleErrors(self):
        pos = math.sqrt((self._x-self.__cible.getX())**2 + (self._y-self.__cible.getY())**2)
        dTheta = self._deltaErreur(self._theta, self.__cible.getTheta())
        lyapunov = (self.__k2/2)*(self.__e1**2 + self.__e2**2) + (self.__e3**2)/2

        return Erreurs(XY=pos, X=(self._x-self.__cible.getX()), Y=(self._y-self.__cible.getY()), TH=dTheta, V=abs(self._v-self.__cible.getV()), W=abs(self._w-self.__cible.getW()), LYA=lyapunov, U1=self.__u1, U2=self.__u2, VC=self.__cible.getV(), WC=self.__cible.getW(), VS=self._v, WS=self._w)
    
    def __updateTrackingError(self):
        x, y = self._x, self._y
        theta, v, w = math.radians(self._theta), self._v, self._w
        xd, yd = self.__cible.getX(), self.__cible.getY()
        thetad, vd, wd = math.radians(self.__cible.getTheta()), self.__cible.getV(), self.__cible.getW()

        self.__e1 = math.cos(theta)*(xd-x) + math.sin(theta)*(yd-y)
        self.__e2 = -math.sin(theta)*(xd-x) + math.cos(theta)*(yd-y)
        self.__e3 = math.radians(self._deltaErreur(math.degrees(theta), math.degrees(thetad)))

        self.__k1 = 2*self.__zeta*math.sqrt(wd**2 + self.__b*(vd**2))
        self.__k2 = self.__b
        self.__k3 = self.__k1