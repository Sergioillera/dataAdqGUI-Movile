# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 20:00:18 2019

@author: Usuario
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
import threading, queue
import sys


class MainWindow(QtWidgets.QWidget): #creamos la ventana principal
    
    ancho=600
    alto=700
    
    def __init__(self, parent=None): #el constructor de la ventana principal
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Main window")
        self.resize(self.ancho,self.alto) #ancho, alto
        
        #donde plotearemos
        self.figura_plots = PlotCanvas(self,width=6, height=6) #el width y height es como *100

        #el boton_init
        boton_init = QPushButton('Iniciar', self)
        boton_init.move(self.ancho/2-70,self.alto-120)
        boton_init.resize(140,100)
        boton_init.clicked.connect(self.iniciar)
        
        #el boton_pause
        boton_pause =QPushButton('Pause',self)
        boton_pause.move(self.ancho/2+100,self.alto-90)
        boton_pause.resize(50,50)
        boton_pause.clicked.connect(self.pause)

        #el boton_exit
        boton_exit = QPushButton('Salir', self)
        boton_exit.move(self.ancho-70,self.alto-70)
        boton_exit.resize(50,50)
        boton_exit.clicked.connect(self.salir)
        
        #text box status + label
        status_text = QLabel('Estado: ',self)
        status_text.move(20, self.alto-100)
        self.status_label = QLabel('Sin conexion        ',self)
        self.status_label.move(70, self.alto-100)
                
        #text box medidas + label
        measure_text = QLabel('Num. medidas: ',self)
        measure_text.move(20, self.alto-80)
        self.measure_label = QLabel('       ',self)
        self.measure_label.move(100, self.alto-80)
        
                
    def iniciar(self):
        archivo='ej_datos.txt'
        self.start=True
        q = queue.Queue()
        self.thread1 = threading.Thread(target=self.read_data,args=(archivo,q))
        self.thread2 = threading.Thread(target=self.recibir_and_plot,args=(q,))
        print ('Iniciamos los threads')
        self.thread1.start()
        self.thread2.start()    
    
    
    def read_data(self,arch,q):
        self.status_label.setText('Leyendo datos...')
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


    def recibir_and_plot(self,q):
        dt=q.get() #hasta que reciba el primer dato
        print('El dt',dt)
        i=0
        while self.start:
            dato=q.get() #las acceleraciones
            #print(i,dato)
            self.status_label.setText('Leyendo datos...')
            if dato==None:
                self.status_label.setText('Datos leidos')
                break
            else:
                self.figura_plots.ax1.cla()
                self.figura_plots.ax1.set_xlim(-12,12)
                self.figura_plots.ax1.set_ylim(-12,12)
                self.figura_plots.ax1.set_zlim(-12,12)
                self.figura_plots.ax1.margins(0.05)
                self.figura_plots.ax1.quiver3D(0,0,0,dato[0],0,0,arrow_length_ratio=0.3,color='r')
                self.figura_plots.ax1.quiver3D(0,0,0,0,dato[1],0,arrow_length_ratio=0.3,color='g')
                self.figura_plots.ax1.quiver3D(0,0,0,0,0,dato[2],arrow_length_ratio=0.3,color='k')
    
                self.figura_plots.ax2.scatter(i,dato[0],color='r')
                self.figura_plots.ax3.scatter(i,dato[1],color='g')
                self.figura_plots.ax4.scatter(i,dato[2],color='k')

                self.figura_plots.draw()
                i+=1
                if i%10==0:
                    print(i)
                    self.measure_label.setText(str(i))
        return         
    
    
    def salir(self):
        self.start=False #in order to kill the recibir_and_plot thread
        self.close()
        return 
    
    def pause(self):
        self.start=False #in order to kill the recibir_and_plot thread
        self.status_label.setText('Pausado')
        return


class PlotCanvas(FigureCanvas):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(hspace=0.4)
        fig.subplots_adjust(wspace=0.3)
        gs = gridspec.GridSpec(nrows=2, ncols=3, height_ratios=[2, 1])
        
        self.ax1 = fig.add_subplot(gs[0, :], projection='3d')
    
        self.ax2 = fig.add_subplot(gs[1,0])
        self.ax2.set_ylim(-12,12)
        self.ax2.set_title("Acc_x ($m/s^2$)")

        self.ax3 = fig.add_subplot(gs[1,1])
        self.ax3.set_ylim(-12,12)
        self.ax3.set_title("Acc_y ($m/s^2$)")

        self.ax4 = fig.add_subplot(gs[1,2])
        self.ax4.set_ylim(-12,12)
        self.ax4.set_title("Acc_z ($m/s^2$)")       

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    gui=MainWindow()
    gui.show()
    sys.exit(app.exec_())


























