# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:29:37 2019

@author: Usuario
"""


import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import socket
import pickle
import os
from plyer import accelerometer




HOST = '192.168.1.14'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
dT = 1./10 #tiempo de adquisicion de medidas



Builder.load_string('''
<ClientInterface>:
    boton : boton
    label1 : label1
    label2 : label2
    FloatLayout:
        orientation: 'horizontal'
        Button:
            id: boton
            text: 'Iniciar'
            disabled: False
            size_hint_x: .2
            size_hint_y: .2
            pos_hint: {'x':.2,'y':.1}
            on_press:
                root.iniciar()
        Button:
            id: boton2
            text: 'Guardar en archivo'
            disable: False
            size_hint_x: .4
            size_hint_y: .2
            pos_hint: {'x':.5,'y':.1}
            on_press:
                root.tofile()
        Label:
            id: label1
            text: 'Desconectado'
            pos_hint: {'x':0,'y':0.1}
        Label:
            id: label2
            text: 'Sin datos'
            pos_hint: {'x':0,'y':0.3}          
            
''')

    
class ClientInterface(FloatLayout):
    '''Root Widget.'''
    label1 = ObjectProperty()
    label2 = ObjectProperty()
    boton = ObjectProperty()
    boton2 = ObjectProperty()

    
    def __init__(self):
        super(ClientInterface,self).__init__()
        self.pressed_start = False
        self.contador = 0
        
    def tofile(self):
        try:
            if self.pressed_start != True: #pulsamos start
                self.label1.text='Guardando datos en archivo'
                self.archivo=open('Datos.txt','w')
                self.archivo.write('dT=' + str(dT)+'\n')
                self.pressed_start = True
                self.medida_y_envio(True)
            else: #pulsamos finalizar
                accelerometer.disable()
                Clock.unschedule(self.write_accelero)
                self.label1.text = 'Desconectado'
                self.label2.text= 'Datos guardados en \n'+os.getcwd()
                self.archivo.close()
                self.pressed_start =False #reiniciamos el start/stop
                self.contador = 0
            
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            
        
    def iniciar(self):
        try:
            if self.pressed_start != True: #pulsamos start
                self.label1.text='Conectando ....'
            
                if self.conectar(): #conectado
                    self.label1.text ='Conectado'
                    self.pressed_start = True
                    self.boton.text = 'Parar'
                    self.medida_y_envio()#realizar la lectura y el envio de datos en loop
                    
                else:
                    self.label1.text='Error conexion'
                    self.pressed_start =False #lo mantenemos como false
            
            else: #pulsamos finalizar
                accelerometer.disable()
                Clock.unschedule(self.obtener_accelero)
                self.label1.text = 'Desconectado'
                self.label2.text= 'Sin datos'
                self.boton.text = 'Iniciar'
                self.pressed_start =False #reiniciamos el start/stop
                self.contador = 0
                self.desconectar()
                
        except NotImplementedError:
            import traceback
            traceback.print_exc()
        
        
    def medida_y_envio(self,*args):
        try:
            accelerometer.enable()
            #print('Encenddido?',accelerometer.enable())
            if args[0]==True:
                print()
                Clock.schedule_interval(self.write_accelero, dT)
            else:
                Clock.schedule_interval(self.obtener_accelero, dT)
            
        except:
            self.label1.text='Error al encender el accelerometro'
            
    
    def write_accelero(self,*args):
        val = accelerometer.acceleration[:3]
        if val != (None,None,None):
            self.archivo.write(str(val)+'\n')
            self.contador+=1
            if self.contador%10==0:
                self.label2.text = 'Guardadas {} medidas'.format(self.contador)
                
        
    def obtener_accelero(self,*args):
        val = accelerometer.acceleration[:3]
        if val != (None,None,None):
            self.conexion.sendall(pickle.dumps(val))
            self.contador+=1
            print(val, self.contador)
            if self.contador%10==0:
                self.label2.text = 'Enviadas {} medidas'.format(self.contador)

    
    def conectar(self):
        self.conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexion.connect((HOST, PORT))
        self.conexion.sendall(pickle.dumps('START')) #enviamos una cosa
        if pickle.loads(self.conexion.recv(1024))=='TRUE': #conexion establecida
            self.conexion.sendall(pickle.dumps(dT))#enviamos el dT
            return True
        else:
            return False

    
    def desconectar(self):
        self.conexion.sendall(pickle.dumps('END')) #enviamos una cosa
        self.conexion.close()
        return 
    
    

class Aplicacion(App):

    def build(self):
        return ClientInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    app=Aplicacion()
    app.run()

















    
 
        

            








