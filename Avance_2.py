from gatitolabs.rosbot import Rosbot #importo la libreria del simulador de rosbot
import numpy as np
from matplotlib import pyplot as plt 
from sensor_msgs.msg import LaserScan #importo libreria para poder usar  read_laser
from gatitolabs.rosbot import Rosbot #Se importa la librería para el robot.
import time
import numpy  as np
#Función 1: Ingresa el bot al simulador, luego lo hace avanzar en linea recta recopilando la distancia que recorrió.
#funcion que mueva al rosbot


robot = Rosbot() #Nuestro objeto robot nos permite controlar al robot.
def mover(v,t):
    time.sleep(1)
    robot.set_vel(v,0) # da velocidad para que se mueva en linea recta por eso es 0 la segunda componente
    time.sleep(t) # dice el tiempo que debe moverse
    robot.set_vel(0,0)#detiene al rosbot
    time.sleep(1)
    d=v*t
    return d #entrega la distancia


def ReadLaser():
    Laser=robot.read_laser()
    angles = []
    i= 0
    for x in Laser.ranges:
        delta_angle= i*Laser.angle_increment
        angle_i= Laser.angle_min+delta_angle
        angles= angles+ [angle_i]
        i= i+1
    X= []
    Y= []
    k=0
    for teta in angles:
        x= np.cos(teta)*Laser.ranges[k]
        y= np.sin(teta)*Laser.ranges[k]
        X= X + [x]
        Y= Y + [y]
        k= k+1
    return [X,Y]
def Funcion2(n,dTotal):
    t= 30
    v= dTotal/t
    dt= t/n
    laserList= [ReadLaser()]
    dList= np.linspace(0,dTotal,n)
    while n>1:
        mover(v,dt)
        laserList= laserList+ [ReadLaser()]
        n=n-1
    return [dList,laserList]


def Funcion3y4(CompletList):
    Distancias = CompletList[0]
    Lecturas = CompletList[1]
    n= len(Distancias)
    print("el Largo es",n)
    FinalList = []
    i= 0
    fig, ax = plt.subplots()
    for d in Distancias:
        xy= Lecturas[i]
        X= xy[1]
        Y= []
        for y in xy[0]:
            Yi= y-d
            Y= Y+[Yi]
        iFlist=[X,Y]
        ax.plot(iFlist[0],iFlist[1],marker=".",linestyle="")
        i= i+1
    fig.savefig("aa")
dTotal= 3
N= 4
CompletList=Funcion2(N,dTotal)
Funcion3y4(CompletList)
