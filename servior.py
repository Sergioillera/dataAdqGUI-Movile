# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:18:35 2019

@author: Usuario
"""

#!/usr/bin/env python3

### La ip del Host es la del portatil, la misma en el programa del cliente
### Tienes que ir al firewall de windows (Panel de control, Firewall) y desactivarlo
### en red privada para que el movil se pueda comunicar con el portatil

import socket
import pickle
import matplotlib.pyplot as plt
import numpy as np

HOST = '192.168.1.14'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        datos=[]
        while True:
            data = conn.recv(1024)
            print(pickle.loads(data))
            if pickle.loads(data) == 'START':
                conn.sendall(pickle.dumps('TRUE'))
                print('Se inicia el recibo de datos')
                dT = pickle.loads(conn.recv(1024))
            elif pickle.loads(data) == 'END':
                print('Finalizado el recibo de datos')
                break
            else:
                datos.append(pickle.loads(data))


####tratemos los datos
acc_x=[]
acc_y=[]
acc_z=[]

for data in datos:
    acc_x.append(data[0])
    acc_y.append(data[1])
    acc_z.append(data[2])
    
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.subplots_adjust(hspace=0.5)


ax1.plot(np.asarray(acc_x)-acc_x[0],'o-')
ax2.plot(np.asarray(acc_y)-acc_y[0],'o-')
ax3.plot(np.asarray(acc_z)-acc_z[0],'o-')
plt.show()

