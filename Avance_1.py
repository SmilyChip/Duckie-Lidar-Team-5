from gatitolabs.rosbot import Rosbot #Se importa la librerÃ­a para el robot.
#from sensor_msgs.msg import LaserScan
import numpy as np
import matplotlib.pyplot as plt

robot = Rosbot()
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
fig, ax = plt.subplots()
ax.plot(X,Y)
fig.savefig("aa")
print("Okey")
