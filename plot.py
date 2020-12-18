import matplotlib.pyplot as plt
import numpy as np

headers = ["Temps (s)", "Erreur de position (m)", "Erreur angulaire (degrés)", "Erreur en X (m)", "Erreur en Y (m)", "Erreur de vitesse linéaire (m/s)", "Erreur de vitesse angulaire (rad/s)", "Function de Lyapunov", "Commande u1", "Commande u2", "Vitesse linéaire des robots (m/s)", "Vitesse augulaire des robots (rad/s)"]

def stop(event):
    plt.close('all')

data = np.genfromtxt("erreurs.txt")

for i in range(1, len(headers)):
    fig = plt.figure()
    fig.canvas.mpl_connect('close_event', stop)

    if i == len(headers)-2:
        plt.plot(data[1:,0], data[1:,i], label="Vitesse linéaire (cible)")
        plt.plot(data[1:,0], data[1:,i+2], label="Vitesse linéaire (suiveur)")
        plt.legend()
    elif i == len(headers)-1:
        plt.plot(data[1:,0], data[1:,i], label="Vitesse angulaire (cible)")
        plt.plot(data[1:,0], data[1:,i+2], label="Vitesse angulaire (suiveur)")
        plt.legend()
    else:
        plt.plot(data[1:,0], data[1:,i])
    
    plt.xlabel(headers[0])
    plt.ylabel(headers[i])
    plt.grid()
    plt.xlim(left=0)
    plt.savefig("figures/fig"+"_"+"_".join(format(x, ".0f") for x in data[0,0:6]).replace("-", "m")+"_"+str(i)+".png") # format: figID_initParam.png

plt.show()