import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.mlab as mlab

_dir = "/home/pi/Proyectos/Interfaz/Datos/Data__100__grados.csv"

_datos = pd.read_csv(_dir)
        
time = _datos['Tiempo']
T = _datos['Temperatura']
C = _datos['Control']
E = _datos['Error_t']
S = _datos['Set_temp']

P = _datos['Presion']
V = _datos['Valvula']
F = _datos['Error_t']
Z = _datos['Set_pre']

rango_time_t = T.count()
rango_time_p = P.count()
limit_t = max(T) + 5
limit_p = max(P) + 5
line_time_t = np.arange(rango_time_t)
line_time_p = np.arange(rango_time_p)
        
fig = plt.figure(dpi=150)
"""
Grafica Temperatura
-------------------
"""
plt.subplot(311)
plt.plot(line_time_t, T, 'r',label='T [°C]')
plt.plot(line_time_t, S, 'b', label='set_t')
plt.legend(loc='upper left')
plt.ylim(0, limit_t)
plt.ylabel('Temperatura', fontsize=13)
plt.title('Curva Temperatura', fontsize=16), plt.grid(True)

"""
Grafica accion control temperatura
------------------------------------
"""
plt.subplot(312)
plt.plot(line_time_t, C,'r', label='[%]')
plt.legend(loc='upper left')
plt.ylim(0, 100)
plt.ylabel('Acción control', fontsize=13)
plt.grid(True)

"""
Grafica error temperatura
-------------------------
"""
plt.subplot(313)
plt.plot(line_time_t, E,'r', label='Error')
plt.legend(loc='upper left')
plt.xlabel('Time(s)', fontsize=13), plt.ylabel('Error', fontsize=13)
plt.grid(True)

"""Ajusta las graficas"""
plt.tight_layout()

#plt.show()

_dir_fig = "/home/pi/Proyectos/Interfaz/Datos/Data__100__grados.png"
fig.savefig(_dir_fig, quality=95, dpi=500)
print("Figura guardada")