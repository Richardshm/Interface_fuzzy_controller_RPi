"""
Librerias Controlador
----------------------
"""
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import threading
import daq as daq

"""
Librerias control PWM
-----------------------
"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Datos
gData_tc = []
gData_tc.append([0])
gData_tc.append([0])

gData_te = []
gData_te.append([0])
gData_te.append([0])

gData_st = []
gData_st.append([0])
gData_st.append([0])

GPIO.setup(18, GPIO.OUT)
modul_r_ter = GPIO.PWM(18, 500)
modul_r_ter.start(0)
"""
Clase que contiene el control fuzzy para la temperatura
--------------------------------------------------------
"""
class _Control_temp(threading.Thread):

    def __init__(self, sleep_interval = 2):
        
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        """
        Se crean las variables Fuzzy, antecedentes y consecuencia (entradas y salidas)
        --------------------------------------------------------------
        """
        error = ctrl.Antecedent(np.arange(-20, 160,1), 'error')
        d_error = ctrl.Antecedent(np.arange(-10,5,0.1), 'd_error')

        actuador = ctrl.Consequent(np.arange(0,100,0.1), 'actuador')

        """
        Se fuzzyfica las variables, metodo trapezoidal y triangular
        --------------------------------------------------------------
        """        
        error['P'] = fuzz.trapmf(error.universe,[-20, -20, -1, 0])
        error['Z'] = fuzz.trimf(error.universe,[-2, 0, 2])
        error['B'] = fuzz.trimf(error.universe,[0, 3, 6])
        error['M'] = fuzz.trimf(error.universe,[2, 9, 16])
        error['A'] = fuzz.trapmf(error.universe,[15, 20, 160, 160])

        d_error['N'] = fuzz.trapmf(d_error.universe,[-10, -10, -2, -1])
        d_error['Z'] = fuzz.trimf(d_error.universe,[-1.5, 0, 1.5])
        d_error['P'] = fuzz.trapmf(d_error.universe,[1, 2, 5, 5])

        actuador['Z'] = fuzz.trimf(actuador.universe,[0, 0.1, 0.2])
        actuador['ZB'] = fuzz.trimf(actuador.universe,[0.1, 6, 13])
        actuador['B'] = fuzz.trimf(actuador.universe,[8, 14, 20])
        actuador['BA'] = fuzz.trimf(actuador.universe,[16, 40, 64])
        actuador['MA'] = fuzz.trimf(actuador.universe,[53, 63, 73])
        actuador['AB'] = fuzz.trimf(actuador.universe,[70, 76, 82])
        actuador['A'] = fuzz.trapmf(actuador.universe,[80, 90, 100, 100])
        
        #error.view()
      
        """
        Reglas Fuzzy
        ------------
        """
        rule1 = ctrl.Rule(error['A'] & d_error['N'], actuador['A'])
        rule2 = ctrl.Rule(error['A'] & d_error['Z'], actuador['A'])
        rule3 = ctrl.Rule(error['A'] & d_error['P'], actuador['A'])

        rule4 = ctrl.Rule(error['M'] & d_error['N'], actuador['Z'])
        rule5 = ctrl.Rule(error['M'] & d_error['Z'], actuador['MA'])
        rule6 = ctrl.Rule(error['M'] & d_error['P'], actuador['AB'])

        rule7 = ctrl.Rule(error['B'] & d_error['N'], actuador['Z'])
        rule8 = ctrl.Rule(error['B'] & d_error['Z'], actuador['B'])
        rule9 = ctrl.Rule(error['B'] & d_error['P'], actuador['B'])
        
        rule10 = ctrl.Rule(error['Z'] & d_error['N'], actuador['Z'])
        rule11 = ctrl.Rule(error['Z'] & d_error['Z'], actuador['Z'])
        rule12 = ctrl.Rule(error['Z'] & d_error['P'], actuador['ZB'])
        
        rule13 = ctrl.Rule(error['P'] & d_error['N'], actuador['Z'])
        rule14 = ctrl.Rule(error['P'] & d_error['Z'], actuador['Z'])
        rule15 = ctrl.Rule(error['P'] & d_error['P'], actuador['Z'])
        
        """
        Se crea el sistema de control
        -----------------------------
        """
        
        self.actuador_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10
                                            ,rule11,rule12,rule13,rule14,rule15])

        self.actuador_t = ctrl.ControlSystemSimulation(self.actuador_ctrl)
    
    def _Update_set_point(self, set_point):
        self.set_point = set_point
        
    def run(self):
        
        e0 = 0
        e1 = 0

        de = 0
        t = daq.gData_t[1]
        while True:
            
            is_killed = self._kill.wait(self._interval)
            if not is_killed:
                set_point = self.set_point
                temp = t[-1]
                
                error = (set_point - temp)
                error = round(error, 2)
                
                e1 = e0
                e0 = error
                de = (e0-e1)*10
                
                self.actuador_t.input['error'] = error
                self.actuador_t.input['d_error'] = de

                self.actuador_t.compute()
                
                salida = self.actuador_t.output['actuador']
                salida = round(salida, 2)
                
                gData_tc[1].append(salida)
                gData_te[1].append(error)
                gData_st[1].append(set_point)
                
                if salida >1:
                    modul_r_ter.ChangeDutyCycle(salida)
                
                if salida < 1:
                    modul_r_ter.ChangeDutyCycle(0)
                    
    def salida(self):
        salida = self.salida
            
    def kill(self):
        self._kill.set()
       
    def reload(self):
        
        self._kill.clear()

dataCollector = _Control_temp(sleep_interval=2)
dataCollector._Update_set_point(set_point=0)
dataCollector.setDaemon(True)