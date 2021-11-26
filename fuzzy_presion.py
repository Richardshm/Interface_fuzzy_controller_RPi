"""
Librerias Controlador
----------------------
"""
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import daq as daq
"""
Librerias control PWM
-----------------------
"""
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import threading

"""Pines declarados para PWM"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

"""Se inicia el pwm en 0"""
modul_valvula = GPIO.PWM(23, 100)
modul_valvula.start(0)

gData_ep = []
gData_ep.append([0])
gData_ep.append([0])

gData_sp = []
gData_sp.append([0])
gData_sp.append([0])

""" 
Clase que contiene el control fuzzy para la presion
----------------------------------------------------
"""
class _Control_pres(threading.Thread):

    def __init__(self, sleep_interval):
                
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        """
        Se crean las variables Fuzzy, antecedentes y consecuencia (entradas y salidas)
        --------------------------------------------------------------
        """
        error = ctrl.Antecedent(np.arange(-25, 25,0.1), 'error')
        d_error = ctrl.Antecedent(np.arange(-10, 5, 1), 'd_error')

        actuador = ctrl.Consequent(np.arange(-0.2, 0.2, 0.01), 'actuador')

        """
        Se fuzzyfica las variables, metodo trapezoidal y triangular
        --------------------------------------------------------------
        """        
        
        error['N'] = fuzz.trapmf(error.universe,[-25, -25, -0.5, -0.5])
        error['Z'] = fuzz.trimf(error.universe,[-1, 0, 1])
        error['P'] = fuzz.trapmf(error.universe,[0.5, 0.5, 25, 25])


        d_error['N'] = fuzz.trapmf(d_error.universe,[-10, -10, -2, -1])
        d_error['Z'] = fuzz.trimf(d_error.universe,[-1.5, 0, 1.5])
        d_error['P'] = fuzz.trapmf(d_error.universe,[1, 2, 5, 5])

        actuador['N'] = fuzz.trapmf(actuador.universe,[-0.2, -0.2, -0.1, 0])
        actuador['Z'] = fuzz.trimf(actuador.universe,[-0.05, 0, 0.05])
        actuador['P'] = fuzz.trapmf(actuador.universe,[0, 0.1, 0.2, 0.2])

        """
        Graficas de la fuzzificacion
        -----------------------------------
        """
        #error['Z'].view()
        #d_error['Z'].view()
        #actuador['Z'].view()
        
        """
        Reglas Fuzzy
        ------------
        """
        rule1 = ctrl.Rule(error['N'] & d_error['N'], actuador['P'])
        rule2 = ctrl.Rule(error['N'] & d_error['Z'], actuador['P'])
        rule3 = ctrl.Rule(error['N'] & d_error['P'], actuador['P'])
        
        rule4 = ctrl.Rule(error['Z'] & d_error['N'], actuador['P'])
        rule5 = ctrl.Rule(error['Z'] & d_error['Z'], actuador['Z'])
        rule6 = ctrl.Rule(error['Z'] & d_error['P'], actuador['N'])
        
        rule7 = ctrl.Rule(error['P'] & d_error['N'], actuador['N'])
        rule8 = ctrl.Rule(error['P'] & d_error['Z'], actuador['N'])
        rule9 = ctrl.Rule(error['P'] & d_error['P'], actuador['N'])

        
        """
        Se crea el sistema de control
        -----------------------------
        """
        
        self.actuador_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9])

        self.actuador_t = ctrl.ControlSystemSimulation(self.actuador_ctrl)
        
    def _Update_set_point(self, set_point):
        self.set_point = set_point

    def run(self):
        
        e0 = 0
        e1 = 0
        
        s0 = 10
        s1 = 0
        
        de = 0
        p = daq.gData_p[1]
        while True:
            
            is_killed = self._kill.wait(self._interval)
            
            if not is_killed:
                set_point = self.set_point
                
                presion = p[-1]
                #print("presion:"+str(presion))
                error = (set_point - presion)
                error = round(error, 2)
                #print("error:"+str(error))
                e1 = e0
                e0 = error
                de = (e0-e1)*10
                #print("deror:"+str(de))
                
                self.actuador_t.input['error'] = error
                self.actuador_t.input['d_error'] = de

                self.actuador_t.compute()
                
                gData_ep[1].append(error)
                gData_sp[1].append(set_point)
                
                salida = self.actuador_t.output['actuador']
                salida = round(salida, 1)
                #print(salida)
                
                s1 = s0
                s0 = s1 + salida
                S0 = round(s0, 1)
                
                if s0 <= 0:
                    modul_valvula.ChangeDutyCycle(0)
                    
                else:
                    modul_valvula.ChangeDutyCycle(s0)
                    

                
    def kill(self):
        
        self._kill.set()

    def reload(self):
        
        self._kill.clear()
        
dataCollector1 = _Control_pres(sleep_interval=1)
dataCollector1._Update_set_point(set_point=0)
dataCollector1.setDaemon(True)
#dataCollector1.start()