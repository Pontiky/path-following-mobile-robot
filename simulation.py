from suiveur import Suiveur
from cible import Cible
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import namedtuple
from threading import Thread
import time # Log temporel

temps = []
erreurs = [ [[], []], [[], []] ]
lyapunov = []
n_err, n_sim = 0, 0
close = False
pause = True

# Evenements lies aux figures
def onPress(event):
    global pause
    if event.key == ' ':
        pause ^= True
    elif event.key == 'left' or event.key == 'q':
        cible.leftKey = True
    elif event.key == 'right' or event.key == 'd':
        cible.rightKey = True
    elif event.key == 'o':
        Cible(cible._x, cible._y, cible._theta, ax, 'k', 1, 2, Te, "ligne")
    elif event.key == 'p':
        Suiveur(suiveur._x, suiveur._y, suiveur._theta, ax, 'r', cible)

def onRelease(event):
    if event.key == 'left' or event.key == 'q':
        cible.leftKey = False
    elif event.key == 'right' or event.key == 'd':
        cible.rightKey = False

def stop(event):
    global close
    close = True
    plt.close('all')

# Initialisation de la fenêtre et des axes de simulation
fig = plt.figure(figsize=(10, 10))
fig.canvas.mpl_connect('key_press_event', onPress)
fig.canvas.mpl_connect('key_release_event', onRelease)
fig.canvas.mpl_connect('close_event', stop)
fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
ax = plt.axes(xlim=(0, 6), ylim=(0, 6))
ax.grid()

# Mise a jour de la simulation
def simulation():
    global pause, close, n_sim, Te
    t0 = time.perf_counter()

    if save:
        errFile = open("erreurs.txt", 'w')
        errFile.write(str(cible.getX())+'\t'+str(cible.getY())+'\t'+str(cible.getTheta())+'\t'+str(suiveur.getX())+'\t'+str(suiveur.getY())+'\t'+str(suiveur.getTheta())+'\t0\t0\t0\t0\t0\t0\t0\t0\n')

    while not close:
        time.sleep(Te)
        if not pause:
            errList = suiveur.handleErrors()
            if save: errFile.write(str(n_sim*Te)+'\t'+str(errList.XY)+'\t'+str(errList.TH)+'\t'+str(errList.X)+'\t'+str(errList.Y)+'\t'+str(errList.V)+'\t'+str(errList.W)+'\t'+str(errList.LYA)+'\t'+str(errList.U1)+'\t'+str(errList.U2)+'\t'+str(errList.VC)+'\t'+str(errList.WC)+'\t'+str(errList.VS)+'\t'+str(errList.WS)+'\n')
           
            cible.avancer()
            suiveur.suivre()

            n_sim += 1

            if n_sim%int(0.5/Te) == 0:
                appendErrors(errList)
                print(time.perf_counter()-t0, "/ 0.5") # temps pour simuler 0.5s 
                t0 = time.perf_counter()

            if trace:
                ax.plot(cible._x, cible._y, '.', color='k', lw=0.1)
                ax.plot(suiveur._x, suiveur._y, '.', color='r', lw=0.1)

    if save: errFile.close()

def animation(i):
    return []

# Initialisation de la fenêtre et des axes des erreurs
figE, axE = plt.subplots(2,2,figsize=(12, 6))
figE.canvas.mpl_connect('key_press_event', onPress)
figE.canvas.mpl_connect('key_release_event', onRelease)
figE.canvas.mpl_connect('close_event', stop)
figE.canvas.mpl_disconnect(figE.canvas.manager.key_press_handler_id)

# Mise a jour des erreurs
def appendErrors(errList):
    global n_err
    temps.append(n_err*0.5)

    erreurs[0][0].append(errList.XY)
    erreurs[0][1].append(errList.TH)
    erreurs[1][0].append(errList.X)
    erreurs[1][1].append(errList.Y)

    n_err += 1

def init_errors():
    axE[0][0].set_ylabel('Erreur position')
    axE[0][1].set_ylabel('Erreur angulaire')
    axE[1][0].set_ylabel('Erreur X')
    axE[1][1].set_ylabel('Erreur Y')

    errList = suiveur.handleErrors()
    appendErrors(errList)

    for k in range(0, 2):
        for m in range(0, 2):
            axE[k][m].plot(temps, erreurs[k][m], '.-', color='#1f77ba', lw=2)
            axE[k][m].set_xlim((0, 0.5))
            axE[k][m].grid()

def errors(i):
    global pause, Te, n_err, n_sim
    if not pause:
        for k in range(0, 2):
            for m in range(0, 2):
                axE[k][m].plot(temps, erreurs[k][m], color='#1f77ba', lw=2)
                axE[k][m].set_xlim((0, n_err*0.5))

# Initialisation des paramètres et des robots
Te = 0.005
trace = True
save = False
cible = Cible(3, 3, 0, ax, 'k', 1, 2, Te, "huit") # ligne / cercle / huit / random / custom / control
suiveur = Suiveur(1, 1, 180, ax, 'r', cible)

# Légende
ax.text(0.03, 0.95, '- Robot suiveur', verticalalignment='bottom', horizontalalignment='left', transform=ax.transAxes, color=suiveur._color, fontsize=10, bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 13})
ax.text(0.03, 0.93, '- Robot cible', verticalalignment='bottom', horizontalalignment='left', transform=ax.transAxes, color=cible._color, fontsize=10)
ax.text(0.03, 0.97, 'Légende :', verticalalignment='bottom', horizontalalignment='left', transform=ax.transAxes, color='k', fontsize=10)

# Lancement de la simulation
anim = FuncAnimation(fig, animation, frames=30000, interval=20, cache_frame_data=False, save_count=0, repeat=False)
err = FuncAnimation(figE, errors, init_func=init_errors, frames=1200, interval=500, cache_frame_data=False, save_count=0, repeat=False)
Thread(target=simulation).start()

plt.show()