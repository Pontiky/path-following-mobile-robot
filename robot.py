import matplotlib.pyplot as plt
import math

class Robot:

    def __init__(self, x, y, theta, ax, color, vmax=1., tacc=2., te=0.005, alpha=1):
        """
        Créé un nouveau robot.

        Paramètres
        ----------
        x : int
            coordonnée x

        y : int
            coordonnée y

        theta : int
            angle (degrés)

        ax : plt.axes
            repère du robot
        
        color : string, Par défaut : 'k' (noir)
            couleur du robot
        
        vmax : float, Par défaut : 1
            vitesse en (m/s)
        
        tacc : float, Par défaut : 2
            temps d'acceleration/de décélération (s)
        
        te : float, Par défaut : 0.005
            période d'échantillonage (s)
        """
        # Attributs fixes
        self._r = 0.1 # Rayon des roues
        self._l = 0.3 # Distance entre le centre du robot et le centre des roues

        # Localisation spaciale
        self._x = x
        self._y = y
        self._theta = (theta+180)%360-180 # en degrés [-180; 180]

        # Paramètres généraux
        self._wl = 0. # Vitesse ansgulaire instantanée de la roue gauche (rad/s)
        self._wr = 0. # Vitesse angulaire instantanée de la roue droite (rad/s)
        self._v = self._r*(self._wl + self._wr)/2 # Vitesse linéaire du robot (m/s)
        self._w = self._r*(self._wr - self._wl)/(2*self._l) # Vitesse angulaire du robot (rad/s)
        self._vmax = vmax # Vitesse maximale (m/s)
        self._tacc = tacc # Temps d'accélération pour passer de 0 à Vmax (s) (idem pour la déceleration)

        # Autres attributs
        self._color = color
        self._te = te
        self.__ax = ax
        self.__alpha = alpha
        
        # Calculs preliminaires liés aux contraintes des outils matplotlib (coordonnées des rectangles dans le coin bas gauche et non au centre de gravité)
        dist = math.sqrt(0.05**2+0.5**2)
        ang = math.atan(0.05/0.5)
        aT = ang + math.radians(self._theta-90)

        dist2 = math.sqrt((0.25+0.1)**2 + (0.1)**2)
        ang2 = math.atan((0.1)/(0.25+0.1))
        aT2 = ang2 + math.radians(self._theta-90)

        dist3 = math.sqrt((0.25)**2 + (0.1)**2)
        ang3 = math.atan(-(0.1)/(0.25))
        aT3 = ang3 + math.radians(self._theta-90)

        # Initialisation des formes geometriques pour le robot
        self.__roueG = plt.Rectangle((self._x - dist2 * math.cos(aT2), self._y - dist2 * math.sin(aT2)), 0.1, 0.2, angle=(self._theta-90), fc=self._color, alpha=self.__alpha)
        self.__roueD = plt.Rectangle((self._x + dist3 * math.cos(aT3), self._y + dist3 * math.sin(aT3)), 0.1, 0.2, angle=(self._theta-90), fc=self._color, alpha=self.__alpha)
        self.__axeRoues = plt.Rectangle((self._x - dist/2 * math.cos(aT),self._y - dist/2 * math.sin(aT)), 0.5, 0.05, angle=(self._theta-90), fc=self._color, alpha=self.__alpha)
        self.__vecteur = plt.Arrow(self._x, self._y, -0.5*math.sin(math.radians(self._theta-90)), 0.5*math.cos(math.radians(self._theta-90)), 0.1, fc=self._color, alpha=self.__alpha)

        # Liaison entre le repère et le robot
        self.__ax.add_patch(self.__roueG)
        self.__ax.add_patch(self.__roueD)
        self.__ax.add_patch(self.__axeRoues)
        self.__vecLink = self.__ax.add_patch(self.__vecteur)

    def _commande(self, v, w):
        self._v = v
        self._w = w

        self._wl = (v - w*self._l)/self._r
        self._wr = (w*self._l + v)/self._r
        self.__updateRobot()

    def _changerVitesseRoues(self, g=0, d=0):
        if g == 1:
            self._wl = min(self._wl+g/self._tacc, math.floor(self._vmax/self._r))
        elif g == -1:
            self._wl = max(self._wl+g/self._tacc, -math.floor(self._vmax/self._r))
        if d == 1:
            self._wr = min(self._wr+d/self._tacc, math.floor(self._vmax/self._r))
        elif d == -1:
            self._wr = max(self._wr+d/self._tacc, -math.floor(self._vmax/self._r))
        
        self._v = self._r*(self._wl + self._wr)/2
        self._w = self._r*(self._wr - self._wl)/(2*self._l)
        self.__updateRobot()

    def __updateRobot(self):
        # Calcul du nouveau état du robot
        self._x = self._x + self._te*self._v*math.cos(math.radians(self._theta))
        self._y = self._y + self._te*self._v*math.sin(math.radians(self._theta))
        self._theta = (self._theta + math.degrees(self._te*self._w) + 180)%360 - 180

        # Calculs preliminaires liés aux contraintes des outils matplotlib
        dist = math.sqrt(0.05**2+0.5**2)
        ang = math.atan(0.05/0.5)
        aT = ang + math.radians(self._theta-90)
        dist2 = math.sqrt((0.25+0.1)**2 + (0.1)**2)
        ang2 = math.atan((0.1)/(0.25+0.1))
        aT2 = ang2 + math.radians(self._theta-90)
        dist3 = math.sqrt((0.25)**2 + (0.1)**2)
        ang3 = math.atan(-(0.1)/(0.25))
        aT3 = ang3 + math.radians(self._theta-90)
        vecLength = 0.5
        
        # Mise à jour des formes geometriques pour le robot
        self.__roueG.set_xy( (self._x - dist2 * math.cos(aT2), self._y - dist2 * math.sin(aT2)) )
        self.__roueD.set_xy( (self._x + dist3 * math.cos(aT3), self._y + dist3 * math.sin(aT3)) )
        self.__axeRoues.set_xy( (self._x - dist/2 * math.cos(aT),self._y - dist/2 * math.sin(aT)) )
        self.__roueG.angle = self._theta - 90
        self.__roueD.angle = self._theta - 90
        self.__axeRoues.angle = self._theta - 90
        self.__vecteur = plt.Arrow(self._x, self._y, -vecLength*math.sin(math.radians(self._theta-90)), vecLength*math.cos(math.radians(self._theta-90)), 0.1, fc=self._color, alpha=self.__alpha)
        self.__vecLink.remove()
        self.__vecLink = self.__ax.add_patch(self.__vecteur)

    def _deltaErreur(self, theta1, theta2):
        dTheta = (theta2 - theta1)
        if dTheta > 180:
            dTheta -= 360
        elif dTheta < -180:
            dTheta += 360
        return dTheta
    
    # Fonctions pour obtenir l'état du robot
    def getX(self):
        return self._x
    
    def getY(self):
        return self._y

    def getTheta(self):
        return self._theta

    def getV(self):
        return self._v

    def getW(self):
        return self._w