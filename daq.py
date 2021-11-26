"""
Librerias graficas
-------------------
"""
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation

"""
Librerias sensor PT100
-------------------
"""
import board
import busio
import digitalio
import adafruit_max31865
import RPi.GPIO as GPIO

"""
Librerias conversor A/D MCP3008
--------------------------------
"""
from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

"""
Librerias data logger
----------------------
"""
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import threading

import fuzzy_temp as tp
import fuzzy_presion as pr

"""
Se configura el tipo de PT100
------------------------------
"""
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D24)  # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=3)

"""
Se configura el MCP3008
----------------------
"""
SPI_PORT   = 0
SPI_DEVICE = 1
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#CLK  = 11
#MISO = 9
#MOSI = 10
#CS   = 7
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

rango = 30

"""
Figura datalogger
-----------------
"""
fig_data_logger = plt.figure(dpi=100)

"""
Grafica Temperatura
-------------------
"""
ax = fig_data_logger.add_subplot(321)
plt.plot(0, 0)
plt.ylim(0, 180), plt.xlim(0,rango)
plt.ylabel('Temperatura', fontsize=13)
plt.title('Curva Temperatura', fontsize=16), plt.grid(True)

"""
Grafica accion control temperatura
------------------------------------
"""
ax = fig_data_logger.add_subplot(323)
plt.plot(0, 0)
plt.ylim(0, 100), plt.xlim(0,rango)
plt.ylabel('Acción control', fontsize=13)
plt.grid(True)

"""
Grafica error temperatura
-------------------------
"""
ax = fig_data_logger.add_subplot(325)
plt.plot(0, 0)
plt.ylim(0, 100), plt.xlim(0,rango)
plt.xlabel('Time(s)', fontsize=13), plt.ylabel('Error', fontsize=13)
plt.grid(True)
"""
Grafica MC3008 presion
------------------------
"""
ax = fig_data_logger.add_subplot(322)
plt.plot(0, 0)
plt.ylim(0, 25), plt.xlim(0,rango)
plt.ylabel('Presion (var)', fontsize=13)
plt.title('Lectura presión', fontsize=16), plt.grid(True)

"""
Grafica MC3008 apertura valvula
--------------------------------
"""
ax = fig_data_logger.add_subplot(324)
plt.plot(0, 0)
plt.ylim(0, 25), plt.xlim(0,rango)
plt.ylabel('Aperura valvula', fontsize=13)
plt.grid(True)

"""
Grafica error presion
----------------------
"""
ax = fig_data_logger.add_subplot(326)
plt.plot(0, 0)
plt.ylim(0, 100), plt.xlim(0,rango)
plt.xlabel('Time(s)', fontsize=13), plt.ylabel('Error', fontsize=13)
plt.grid(True)

"""Ajusta las graficas"""
plt.tight_layout()


"""
Se crean las listas que contienen los datos
--------------------------------------------
"""
"""Lista temperatura"""
gData_t = []
gData_t.append([0])
gData_t.append([0])

"""Lista resistencia"""
gData_r = []
gData_r.append([0])
gData_r.append([0])

"""Lista Presion"""
gData_p = []
gData_p.append([0])
gData_p.append([0])

"""Lista apertura valvula"""
gData_v = []
gData_v.append([0])
gData_v.append([0])

fig = plt.figure(dpi=100)

"""
Grafica Temperatura
-------------------
"""
ax = fig.add_subplot(221)
hl, = plt.plot(gData_t[0], gData_t[1],'r', label='T [°C]')
plt.legend(loc='upper left')
plt.ylim(0, 180), plt.xlim(0,rango)
plt.ylabel('Temperatura', fontsize=13)
plt.title('Lectura Temperatura', fontsize=16), plt.grid(True)

"""
Grafica accion control temperatura
------------------------------------
"""
ax = fig.add_subplot(223)
hlr, = plt.plot(gData_r[0], gData_r[1], 'r', label='[%]')
plt.legend(loc='upper left')
plt.ylim(0, 100), plt.xlim(0,rango)
plt.xlabel('Time(s)', fontsize=13), plt.ylabel('Acción control', fontsize=13)
plt.grid(True)

"""
Grafica MC3008 presion
------------------------
"""
ax = fig.add_subplot(222)
hlp, = plt.plot(gData_p[0], gData_p[1], 'c', label='Psi')
plt.legend(loc='upper left')
plt.ylim(0, 25), plt.xlim(0,rango)
plt.ylabel('Presion (var)', fontsize=13)
plt.title('Lectura presión', fontsize=16), plt.grid(True)

"""
Grafica MC3008 apertura valvula
--------------------------------
"""
ax = fig.add_subplot(224)
hlv, = plt.plot(gData_v[0], gData_v[1], 'c', label='[ % ]')
plt.legend(loc='upper left')
plt.ylim(0, 100), plt.xlim(0,rango)
plt.xlabel('Time(s)', fontsize=13), plt.ylabel('Aperura valvula', fontsize=13)
plt.grid(True)

"""Ajusta las graficas"""
plt.tight_layout()

"""
Clase que se va a ejecutar en otro thread y que
guardará los datos del serial en las listas
--------------------------------------------------
"""

class _Hilo_grafica(threading.Thread):
        
    def __init__(self, sleep_interval=1):
        
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        
        #Listas para el data logger
        self.lista_tiempo = []
        
        self.lista_temp = []
        self.lista_tc = []
        self.lista_te = []
        self.lista_st = []
        
        self.lista_presion = []
        self.lista_valvula = []
        self.lista_epr = []
        self.lista_sp = []
                
    def run(self):
        tc = tp.gData_tc[1]
        te = tp.gData_te[1]
        st = tp.gData_st[1]
        
        ep = pr.gData_ep[1]
        sp = pr.gData_sp[1]
        
        y = 0.0
        alpha = 0.7
        s = 0.0
        
        while True:
            is_killed = self._kill.wait(self._interval)
           
            temp = sensor.temperature
            temp = round(temp, 2)
            
            tempc = tc[-1]
            tempe = te[-1]
            set_t = st[-1]
            
            presion = mcp.read_adc(2)
            presion = ((presion*21)/930)
            presion = round(presion,2)
            
            y = presion
            s = (alpha*y)+((1-alpha)*s)
            presion = s
            presion = round(presion,2)
            
            valvula = mcp.read_adc(1)
            print(valvula)
            valvula = ((valvula*100)/500)
            valvula = int(valvula)
            
            epr = ep[-1]
            set_p = sp[-1]
            
            if not is_killed:
                                
                now = datetime.now().replace(microsecond=0)
                now = str(now).split(" ")
                now = now[1]
                
                self.lista_tiempo.append(now)
                
                #Data logger
                self.lista_temp.append(temp)
                self.lista_tc.append(tempc)
                self.lista_te.append(tempe)
                self.lista_st.append(set_t)
                
                self.lista_presion.append(presion)
                self.lista_valvula.append(valvula)
                self.lista_epr.append(epr)
                self.lista_sp.append(set_p)
                
                #Graficas
                gData_t[1].append(temp)
                gData_r[1].append(tempc)
                gData_p[1].append(presion)
                gData_v[1].append(valvula)
                
            if len(gData_t[1]) > rango or len(gData_r[1]) > rango:
                gData_t[1].pop(0)
                gData_r[1].pop(0)
                
            if len(gData_p[1]) > rango or len(gData_v[1]) > rango:
                gData_p[1].pop(0)
                gData_v[1].pop(0)
            
    def kill(self):
        
        self._kill.set()
        
    def reload(self):
        
        self._kill.clear()

    def update_line_t(num, hl, data_t, hlr, data_r, hlp, data_p, hlv, data_v):
        hl.set_data(range(len(data_t[1])), data_t[1])
        hlr.set_data(range(len(data_r[1])), data_r[1])
        hlp.set_data(range(len(data_p[1])), data_p[1])
        hlv.set_data(range(len(data_v[1])), data_v[1])
        return hl, hlr, hlp, hlv
    
    def _save_data(self):
        _now = datetime.now().replace(microsecond=0)

        self._csv_data = {'Tiempo':self.lista_tiempo, 'Temperatura':self.lista_temp, 'Control':self.lista_tc,
                     'Error_t':self.lista_te, 'Set_temp':self.lista_st,'Presion':self.lista_presion,
                          'Valvula':self.lista_valvula, 'Error_p':self.lista_epr, 'Set_pre':self.lista_sp}
        
        df = pd.DataFrame(self._csv_data, columns=['Tiempo','Temperatura','Control','Error_t', 'Set_temp',
                                                   'Presion','Valvula', 'Error_p', 'Set_pre'])
        df.to_csv('/home/pi/Proyectos/Interfaz/Datos/Data__'+str(_now)+'.csv')
        
        self.lista_tiempo.clear()
        self.lista_temp.clear()
        self.lista_tc.clear()
        self.lista_te.clear()
        self.lista_st.clear()
        
        self.lista_presion.clear()
        self.lista_valvula.clear()
        self.lista_epr.clear()
        self.lista_sp.clear()

"""Se inicia el thread cada 1 segundo adquiere datos"""
dataCollector2 = _Hilo_grafica(sleep_interval=1)
dataCollector2.setDaemon(True)
