# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:46:05 2019

@author: Usuario
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
import threading, queue


archivo='ej_datos.txt'
start=True

def read_data(arch,q):
    archivo=open(arch,'r')
    dT=archivo.readline()
    dt=float(dT[dT.index('=')+1:-1])
    q.put(dt) #envia el dt
    for line in archivo.readlines():
        accs=line.replace('\n','')[1:-1].split(',')
        dato=[]
        for acc in accs:
            dato.append(float(acc))
        q.put(dato) #envia el dato
    q.put(None) #enviamos el fin del archivo
    return


def recibir_and_plot(start,q):
    dt=q.get() #hasta que reciba el primer dato
    print('El dt',dt)
    
    #generamos el plot
    origin = [0,0,0]
    X, Y, Z = zip(origin,origin,origin) 
    fig = plt.figure()
    gs = gridspec.GridSpec(nrows=2, ncols=3, height_ratios=[2, 1])

    ax1 = fig.add_subplot(gs[0, :], projection='3d')
    
    ax2 = fig.add_subplot(gs[1,0])
    ax2.set_ylim(-12,12)
    ax2.set_title("Acc_x ($m/s^2$)")

    ax3 = fig.add_subplot(gs[1,1])
    ax3.set_ylim(-12,12)
    ax3.set_title("Acc_y ($m/s^2$)")

    ax4 = fig.add_subplot(gs[1,2])
    ax4.set_ylim(-12,12)
    ax4.set_title("Acc_z ($m/s^2$)")   
    
    i=0
    while start:
        dato=q.get() #las acceleraciones
        print(i,dato)
        if dato==None:
            break
        else:
            ax1.cla()
            ax1.set_xlim(-12,12)
            ax1.set_ylim(-12,12)
            ax1.set_zlim(-12,12)
            ax1.margins(0.05)
            ax1.quiver3D(0,0,0,dato[0],0,0,arrow_length_ratio=0.3,color='r')
            ax1.quiver3D(0,0,0,0,dato[1],0,arrow_length_ratio=0.3,color='g')
            ax1.quiver3D(0,0,0,0,0,dato[2],arrow_length_ratio=0.3,color='k')
    
            ax2.scatter(i,dato[0],color='r')
            ax3.scatter(i,dato[1],color='g')
            ax4.scatter(i,dato[2],color='k')

            plt.show()
            plt.pause(dt)
            i+=1
    return     
    
    
q = queue.Queue()
thread1 = threading.Thread(target=read_data,args=(archivo,q))
thread2 = threading.Thread(target=recibir_and_plot,args=(start,q))
print ('Iniciamos los threads')
thread1.start()
thread2.start()

