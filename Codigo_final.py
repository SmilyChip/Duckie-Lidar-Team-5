from gatitolabs.rosbot import Rosbot
from sensor_msgs.msg import LaserScan
import time
import numpy as np
import matplotlib.pyplot as plt

robot = Rosbot() #Nuestro objeto robot nos permite controlar al robot.

#Recive una velocidad y un tiempo
#Hace que el robot se mueva en línea recta a la velocidad recibida por el tiempo recibido.
def mover(v,t):
    time.sleep(1)
    robot.set_vel(v,0) # da velocidad para que se mueva en linea recta por eso es 0 la segunda componente
    time.sleep(t) # dice el tiempo que debe moverse
    robot.set_vel(0,0)#detiene al rosbot
    time.sleep(1)
    d=v*t
    return d #entrega la distancia

#Recibe None  
#Entrega los puntos medidos por el sensor LIDAR en coordenadas cartesianas con respecto a la posición del robot (odometría perfecta)  
def ReadLaser():
    Laser=robot.read_laser()
    angles = []
    botAngle=robot.get_rotation()
    i= 0
    for x in Laser.ranges:
        delta_angle= i*Laser.angle_increment
        angle_i= Laser.angle_min+delta_angle+botAngle
        angles= angles+ [angle_i]
        i= i+1
    botPosition=robot.get_position()
    X= [botPosition[0]]
    Y= [botPosition[1]]
    k=0
    for teta in angles:
        x= -(np.cos(teta)*Laser.ranges[k]-botPosition[0])
        y= -(np.sin(teta)*Laser.ranges[k]-botPosition[1])
        X= X + [x]
        Y= Y + [y]
        k=k+1
    return [X,Y]

#Recibe una velocidad angular
#Mueve al robot en el angulo recibido en un tiempo de 3 segundos para minimizar errores 
def girar(theta):
    time.sleep(1)
    robot.set_vel(0,theta/3)
    time.sleep(3)
    robot.set_vel(0,0)
    time.sleep(1)

ang_g = robot.get_rotation() #guarda el angulo del robot con respecto a su eje coordenado polar

#Recibe la cantidad de veces que se detendrá (n) y la distancia a la cual se moverá el robot por cada detención
#Mueve el robot y corrige su angulo para moverse siempre en línea recta en el angulo pi y entrega las mediciones del sensor LIDAR
def Funcion2_0(n,dTotal):
    t= 10
    v= dTotal/t
    dt= t/n
    laserList= [ReadLaser()]
    kks=[None]*(n-1)
    for i in kks:
        mover(v,dt) #mueve el robot en línea recta
        if robot.get_rotation()<3.1 and robot.get_rotation()>0: #corrige el ángulo después de avanzar si este es menor a pi  
            print(robot.get_rotation())
            rot= 3.14-robot.get_rotation()
            girar(rot+0.5)
        if robot.get_rotation()>-3.1 and robot.get_rotation()<0: #corrige el ángulo después de avanzar si este es mayor a -pi
            print(robot.get_rotation())
            rot= 3.14+robot.get_rotation()
            girar(-rot-0.5)
        mover(0,1)     
        laserList= laserList+ [ReadLaser()]
    return laserList

#Recibe la cantidad de veces que se detendrá (n) y la distancia a la cual se moverá el robot por cada detención
#Mueve el robot y corrige su angulo para moverse siempre en línea recta en el angulo -pi/2 y entrega las mediciones del sensor LIDAR
def Funcion2_1(n,dTotal):
    t= 10
    v= dTotal/t
    dt= t/n
    laserList= [ReadLaser()]
    kks=[None]*(n-1)
    for i in kks:
        mover(v,dt)
        if robot.get_rotation()<-1.61 and robot.get_rotation()<0: #corrige el ángulo después de avanzar si este es menor a -pi/2 
            rot= -1.57-robot.get_rotation()
            girar(rot+0.5)
        if robot.get_rotation()>-1.53 and robot.get_rotation()<0: #corrige el ángulo después de avanzar si este es mayor a -pi/2 
            rot= 1.57+robot.get_rotation()
            girar(rot-0.5)
        mover(0,1)     
        laserList= laserList+ [ReadLaser()]
    return laserList

#Recibe la cantidad de veces que se detendrá (n) y la distancia a la cual se moverá el robot por cada detención
#Mueve el robot y corrige su angulo para moverse siempre en línea recta en el angulo -pi/2 y entrega las mediciones del sensor LIDAR  
def Funcion2_2(n,dTotal):
    t= 10
    v= dTotal/t
    dt= t/n
    laserList= [ReadLaser()]
    kks=[None]*(n-1)
    for i in kks:
        mover(v,dt)
        if robot.get_rotation()<-0.04 and robot.get_rotation()<0: #corrige el ángulo después de avanzar si este es mayor a 0 
            rot= -robot.get_rotation()
            girar(rot+0.5)
        if ang_g> 0.04 and robot.get_rotation()>0: #corrige el ángulo después de avanzar si este es mayor a 0
            rot= -robot.get_rotation()
            girar(rot-0.5)
        mover(0,1)     
        laserList= laserList+ [ReadLaser()]
    return laserList

#Recibe las mediciones del LIDAR 
#Grafica las mediciones del LIDAR
def Funcion3y4(laserList):
    fig, ax = plt.subplots()
    i=1
    o=0
    for xy in laserList:
        for xy in laserList[o]:
            X= xy[0]
            Y= xy[1]
            ax.plot(X,Y,marker=".",linestyle="")
            plt.xlim([-4,4])
            plt.ylim([-6,6])
            fig.savefig("fig"+str(o)+str(i))
            i+=1
        o+=1

#El robot parte de la esquina superior derecha del mapa y solo hace un recorrido total del mapa 
mov_med1=Funcion2_0(5,5)#se mueve a la izquierda
girar(2.3)
mov_med2=Funcion2_1(5,5)
girar(2.3)
mov_med3=Funcion2_2(5,5)
girar(-2.3)
mov_med4=Funcion2_1(3,3)
girar(-2.3)
mov_med5=Funcion2_0(5,5)
girar(2.3)
mov_med6=Funcion2_1(3,3)
girar(2.3)
mov_med7=Funcion2_2(5,5)
final_med=[]
final_med.append(mov_med1)
final_med.append(mov_med2)
final_med.append(mov_med3)
final_med.append(mov_med4)
final_med.append(mov_med5)
final_med.append(mov_med6)
final_med.append(mov_med7)
Funcion3y4(final_med) #grafica todo el mapa
