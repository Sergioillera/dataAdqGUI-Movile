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

        #el boton_exit
        boton_exit = QPushButton('Salir', self)
        boton_exit.move(self.ancho-70,self.alto-70)
        boton_exit.resize(50,50)
        boton_exit.clicked.connect(self.salir)
    
    
    def iniciar(self):
        archivo='ej_datos.txt'
        start=True
        q = queue.Queue()
        thread1 = threading.Thread(target=self.read_data,args=(archivo,q))
        thread2 = threading.Thread(target=self.recibir_and_plot,args=(start,q))
        print ('Iniciamos los threads')
        thread1.start()
        thread2.start()    
    
    
    def read_data(self,arch,q):
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


    def recibir_and_plot(self,start,q):
        dt=q.get() #hasta que reciba el primer dato
        print('El dt',dt)
        i=0
        while start:
            dato=q.get() #las acceleraciones
            print(i,dato)
            if dato==None:
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
        return         
    
    
    def salir(self):
        self.close()
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

































'''
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This s an example button')
        button.move(500,0)
        button.resize(140,100)

        self.show()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #self.plot()


    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
'''