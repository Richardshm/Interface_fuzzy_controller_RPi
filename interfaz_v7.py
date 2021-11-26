"""
Librerias Controlador
----------------------
"""
import time
import daq as daq
import threading
import fuzzy_temp as tp
import fuzzy_presion as pr

modul_r_ter = tp.modul_r_ter
modul_valvula = pr.modul_valvula
"""
Librerias GUI
-------------------
"""
from tkinter import*
import tkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2TkAgg)
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import gc
"""
Clase que contiene todos los componentes de la interfaz
-------------------------------------------------------
"""
class Window():           
    #Crea la ventana
    window = Tk()
    #Establece la resolucion y el titulo
    window.geometry('1280x750')
    window.title("Monitorizacion de Variables")
    window.resizable(0, 0)

    #pestanas
    tab = ttk.Notebook(window)
    tab1 = ttk.Frame(tab)
    tab2 = ttk.Frame(tab)

    tab.add(tab1, text='First')
    tab.add(tab2, text='Second')

    tab.pack(expand=1, fill= 'both')

    #Toolbar superior tab1
    toolbar_top = LabelFrame(tab1, text ="R. Hernandez, F.Moreno, S.Castro", font=('Verdana', 12))
    toolbar_top.pack(side=tkinter.BOTTOM)
    toolbar_top.place(x=0, y=0, height=125, width=1280)

    #Toolbar superior tab2
    toolbar_top_2 = LabelFrame(tab2, text ="R. Hernandez, F.Moreno, S.Castro", font=('Verdana', 12))
    toolbar_top_2.pack(side=tkinter.BOTTOM)
    toolbar_top_2.place(x=0, y=0, height=125, width=1280) 

    #Figura embebida
    canvas = FigureCanvasTkAgg(daq.fig,master=tab1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM)
    canvas.get_tk_widget().place(x=150, y=125, height=475, width=980)

    #Figura embebida data logger final en blanco
    canvas = FigureCanvasTkAgg(daq.fig_data_logger,master=tab2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM)
    canvas.get_tk_widget().place(x=0, y=125, height=500, width=1280)

    #Toolbar inferior tab1
    toolbar_down = LabelFrame(tab1, text="Tablero de control", font=('Verdana', 12))
    toolbar_down.pack(side=tkinter.BOTTOM)
    toolbar_down.place(x=0, y= 610, height=200, width=1280)

    #Toolbar inferior tab2 
    toolbar_down_2 = LabelFrame(tab2, text="Tablero de control", font=('Verdana', 12))
    toolbar_down_2.pack(side=tkinter.BOTTOM)
    toolbar_down_2.place(x=0, y= 625, height=175, width=1280)

    #Toolbar lateral izquierda
    toolbar_izq = LabelFrame(tab1, text="Set point \n temperatura", font=('Verdana', 12))
    toolbar_izq.pack(side=tkinter.BOTTOM)
    toolbar_izq.place(x=0, y= 125, height=475, width=150)

    #Toolbar lateral derecha
    toolbar_der = LabelFrame(tab1, text="Set point \n presión", font=('Verdana', 12))
    toolbar_der.pack(side=tkinter.BOTTOM)
    toolbar_der.place(x=1130, y= 125, height=475, width=150)

    #label temperatura actual
    L1 = Label(toolbar_izq, text="T [°C]:", font=('Verdana', 14))
    L1.pack(side=tkinter.BOTTOM)
    L1.place(x=10, y=10)

    #label resistencia actual
    L2 = Label(toolbar_izq, text="[%]:", font=('Verdana', 14))
    L2.pack(side=tkinter.BOTTOM)
    L2.place(x=10, y=35)

    #label presion actual
    L3 = Label(toolbar_der, text="Psi:", font=('Verdana', 14))
    L3.pack(side=tkinter.BOTTOM)
    L3.place(x=10, y=10)

    #label APERTURA VALVULA actual
    L3 = Label(toolbar_der, text="[%]:", font=('Verdana', 14))
    L3.pack(side=tkinter.BOTTOM)
    L3.place(x=10, y=35)

    #Logo tab1
    contenedor_ufps = tkinter.Canvas(toolbar_top, bg="white", height=100, width=100, bd=1, relief=tkinter.RAISED)
    contenedor_ufps.pack()
    contenedor_ufps.place(relx=0.1, rely=0)
    filename_ufps = PhotoImage(file = 'logo_ufps.png',master=toolbar_top)
    contenedor_ufps.create_image(0, 0, anchor='nw', image=filename_ufps)

    #Logo tab2
    contenedor_ufps_2 = tkinter.Canvas(toolbar_top_2, bg="white", height=100, width=100, bd=1, relief=tkinter.RAISED)
    contenedor_ufps_2.pack()
    contenedor_ufps_2.place(relx=0.1, rely=0)
    filename_ufps_2 = PhotoImage(file = 'logo_ufps.png',master=toolbar_top_2)
    contenedor_ufps_2.create_image(0, 0, anchor='nw', image=filename_ufps_2)
    
    def __init__(self):
        tab1 = Window.tab1
        tab2 = Window.tab2
        
        toolbar_top = Window.toolbar_top
        toolbar_top_2 = Window.toolbar_top_2
        toolbar_down = Window.toolbar_down
        toolbar_down_2 = Window.toolbar_down_2
        toolbar_izq = Window.toolbar_izq
        toolbar_der = Window.toolbar_der
        
        #Encabezado
        #Titulo tab1
        texto_t ="Universidad Francisco de Paula Santander \n Adquisición de variables térmicas y neumáticas"
        boton_titulo = tkinter.Button(master=toolbar_top, text=texto_t)
        boton_titulo.configure(font=('Verdana', 15), state=NORMAL)
        boton_titulo.pack()
        boton_titulo.place(x=300, y = 8, width=700, height=75)
        
        #Titulo tab2
        texto_t_2 ="Universidad Francisco de Paula Santander \n Adquisición de variables térmicas y neumáticas"
        boton_titulo_2 = tkinter.Button(master=toolbar_top_2, text=texto_t_2)
        boton_titulo_2.configure(font=('Verdana', 15), state=NORMAL)
        boton_titulo_2.pack()
        boton_titulo_2.place(x=300, y = 8, width=700, height=75)

        #Boton Ayuda tab1
        boton_ayuda = tkinter.Button(master=toolbar_top, text="Ayuda", command=self._ayuda_tab1)
        boton_ayuda.configure(font=('Verdana', 15))
        boton_ayuda.pack()
        boton_ayuda.place(x=1075, y=8, width=125, height=75)
             
        #Boton Ayuda tab2
        boton_ayuda_2 = tkinter.Button(master=toolbar_top_2, text="Ayuda", command=self._ayuda_tab2)
        boton_ayuda_2.configure(font=('Verdana', 15))
        boton_ayuda_2.pack()
        boton_ayuda_2.place(x=1075, y=8, width=125, height=75)
        
        #Boton salir
        boton_salir = tkinter.Button(master=toolbar_down, text="Salir", command=self._quit)
        boton_salir.configure(font=('Verdana', 15))
        boton_salir.pack()
        boton_salir.place(x=1145, y=0, width=125, height=75)
        
        #Boton salir tab2
        boton_salir_2 = tkinter.Button(master=toolbar_down_2, text="Salir", command=self._quit)
        boton_salir_2.configure(font=('Verdana', 15))
        boton_salir_2.pack()
        boton_salir_2.place(x=1145, y=0, width=125, height=60)
        
        #Boton de inicio
        self.boton_start = tkinter.Button(toolbar_down, text="Iniciar", command=self._start)
        self.boton_start.configure(font=('Verdana', 15))
        self.boton_start.pack()
        self.boton_start.place(x=10, y=0, width=125, height=75)
        
        #Boton actuador termico
        self.boton_termico = tkinter.Button(master=toolbar_down, text="Actuador térmico ON", command=self._pwm_temp)
        self.boton_termico.configure(font=('Verdana', 15), activebackground='red', bg='red', state=DISABLED)
        self.boton_termico.pack()
        self.boton_termico.place(x=145, y=0, width=250, height=30)
        
        #PWM actuador termico
        self.scale_pwm_t = Scale(toolbar_down, orient=HORIZONTAL, from_=0, to=100)
        self.scale_pwm_t.pack()
        self.scale_pwm_t.place(x=145, y=30, width=250, height=50)

        #Boton actuador neumatico
        self.boton_neumatico= tkinter.Button(master=toolbar_down, text="Actuador neumático ON", command=self._pwm_presion)
        self.boton_neumatico.configure(font=('Verdana', 15), activebackground='red', bg='red', state=DISABLED)
        self.boton_neumatico.pack()
        self.boton_neumatico.place(x=400, y=0, width=250, height=30)

        #PWM actuador neumatico
        self.scale_pwm_n = Scale(toolbar_down, orient=HORIZONTAL, from_=0, to=100)
        self.scale_pwm_n.pack()
        self.scale_pwm_n.place(x=400, y=30, width=250, height=50)
        
        #Boton detener
        self.boton_detener = tkinter.Button(master=toolbar_down, text="Pausar", command=self._stop)
        self.boton_detener.configure(font=('Verdana', 15), state=DISABLED)
        self.boton_detener.pack()
        self.boton_detener.place(x=670, y=0, width=125, height=75)

        #Boton Reanudar
        self.boton_reanudar = tkinter.Button(master=toolbar_down, text="Reanudar", command=self._reloading)
        self.boton_reanudar.configure(font=('Verdana', 15), state=DISABLED)
        self.boton_reanudar.pack()
        self.boton_reanudar.place(x=805, y=0, width=125, height=75)

        #Boton Guardar
        self.boton_save = tkinter.Button(master=toolbar_down, text="Guardar \n Datos ", command=self._save)
        self.boton_save.configure(font=('Verdana', 15), state=DISABLED)
        self.boton_save.pack()
        self.boton_save.place(x=940, y=0, width=125, height=75)
           
        #Boton de abrir csv
        self.boton_open = tkinter.Button(toolbar_down_2, text="Abrir archivo \n .csv ", command=self._file)
        self.boton_open.configure(font=('Verdana', 15))
        self.boton_open.pack()
        self.boton_open.place(x=250, y=0, width=200, height=60)
                   
        #Boton graficar archivo .csv
        self.boton_graf = tkinter.Button(toolbar_down_2, text=" Graficar \n archivo .csv", command=self._graf)
        self.boton_graf.configure(font=('Verdana', 15), state= DISABLED)
        self.boton_graf.pack()
        self.boton_graf.place(x=500, y=0, width=200, height=60)
        
        #Boton guardar imagenes
        self.boton_graf2 = tkinter.Button(toolbar_down_2, text="Guardar \n figura", command=self.save_graf)
        self.boton_graf2.configure(font=('Verdana', 15), state= DISABLED)
        self.boton_graf2.pack()
        self.boton_graf2.place(x=750, y=0, width=200, height=60)
        
        #scale set point temperatura
        self.scale_set = Scale(toolbar_izq, from_=50, to=150, width=50)
        self.scale_set.pack(side=tkinter.BOTTOM)
        self.scale_set.place(x=15, y=70, height=250)
        
        #Boton iniciar fuzzy temp
        self.btn_on_t = Button(toolbar_izq, text="ON FUZZY \n TEMP ", command=self._on_t)
        self.btn_on_t.configure(activebackground='red', bg='red', state=DISABLED)
        self.btn_on_t.pack(side=tkinter.BOTTOM)
        self.btn_on_t.place(x=25.5, y=325)
        
        #Boton iniciar fuzzy presion
        self.btn_on_p = Button(toolbar_der, text="ON FUZZY \n PRESION ", command=self._on_p)
        self.btn_on_p.configure(activebackground='red', bg='red', state=DISABLED)
        self.btn_on_p.pack(side=tkinter.BOTTOM)
        self.btn_on_p.place(x=25.5, y=325)
        
        #Boton get set point
        self.btn_set = Button(toolbar_izq, text="Set point", command=self._get_set_t)
        self.btn_set.configure(state=DISABLED)
        self.btn_set.pack(side=tkinter.BOTTOM)
        self.btn_set.place(x=31, y=370)
        
        #Label set point temperatura
        self.label_set = Label(toolbar_izq, text="Set point =", font=('Verdana', 13))
        self.label_set.pack(side=tkinter.BOTTOM)
        self.label_set.place(x=5, y=400)
        
        #scale set point presion
        self.scale_set_p = Scale(toolbar_der, from_=5, to=20, width=50)
        self.scale_set_p.pack(side=tkinter.BOTTOM)
        self.scale_set_p.place(x=15, y=70, height=250)
        
        #Boton get set point presion
        self.btn_set_p = Button(toolbar_der, text="Set point", command=self._get_set_p)
        self.btn_set_p.configure(state=DISABLED)
        self.btn_set_p.pack(side=tkinter.BOTTOM)
        self.btn_set_p.place(x=31, y=370)
        
        #Label set point presion
        self.label_set_p = Label(toolbar_der, text="Set point =", font=('Verdana', 13))
        self.label_set_p.pack(side=tkinter.BOTTOM)
        self.label_set_p.place(x=5, y=400)
        
        #Botones on pwm
        self.conteo_on_t = False
        self.conteo_on_p = False
        #Botones on fuzzy
        self.conteo_on_ft = False
        self.conteo_on_fp = False
               
    def _get_set_t(self):
        self.point_t = self.scale_set.get()
        sel = "Set point =" + str(self.point_t)
        self.label_set.configure(text=sel)
               
        if tp.dataCollector.is_alive():
            tp.dataCollector.kill()
            tp.dataCollector._Update_set_point(set_point=self.point_t)
            tp.dataCollector.reload()
            #self.conteo_on_ft = not self.conteo_on_ft
        else:
            pass
        
    def _on_t(self):
                        
             if self.conteo_on_ft == False:
                 self.boton_termico.configure(state=DISABLED)
                 self.btn_on_t.configure(bg = 'green', activebackground='green')
                 self.btn_set.configure(state=NORMAL)
                 if tp.dataCollector.is_alive():
                     tp.dataCollector.reload()
                     self._get_set_t()
                 else:
                     tp.dataCollector.start()
                     self._get_set_t()
                
             if self.conteo_on_ft == True:
                 self.boton_termico.configure(state=NORMAL)
                 self.btn_on_t.configure(bg = 'red', activebackground='red')
                 self.btn_set.configure(state=DISABLED)
                 tp.dataCollector.kill()
                 modul_r_ter.ChangeDutyCycle(0)
                 
             self.conteo_on_ft = not self.conteo_on_ft

    def _get_set_p(self):
        self.point_p = self.scale_set_p.get()
        sel_p = "Set point =" + str(self.point_p)
        self.label_set_p.configure(text=sel_p)
                
        if pr.dataCollector1.is_alive():
            pr.dataCollector1.kill()
            pr.dataCollector1._Update_set_point(set_point=self.point_p)
            pr.dataCollector1.reload()
        else:
            pass   
                
    def _on_p(self):
        
        if self.conteo_on_fp == False:
            self.boton_neumatico.configure(state=DISABLED)
            self.btn_on_p.configure(bg = 'green', activebackground='green')
            self.btn_set_p.configure(state=NORMAL)
        if pr.dataCollector1.is_alive():
            pr.dataCollector1.reload()
            self._get_set_p()
        else:
            pr.dataCollector1.start()
            self._get_set_p()
        
        if self.conteo_on_fp == True:
            self.boton_neumatico.configure(state=NORMAL)
            self.btn_on_p.configure(bg = 'red', activebackground='red')
            self.btn_set_p.configure(state=DISABLED)
            pr.dataCollector1.kill()
            modul_valvula.ChangeDutyCycle(0)
            tp.gData_tc[1].append(0)
         
        self.conteo_on_fp = not self.conteo_on_fp
            
    def _pwm_temp(self):
            
        if self.conteo_on_t == False:
            self.btn_on_t.configure(state=DISABLED)
            point_pwm_t = self.scale_pwm_t.get()
            modul_r_ter.ChangeDutyCycle(point_pwm_t)
            tp.gData_tc[1].append(point_pwm_t)
            self.boton_termico.configure(bg = 'green', activebackground='green')            
         
        if self.conteo_on_t == True:
            self.btn_on_t.configure(state=NORMAL)
            self.boton_termico.configure(bg = 'red', activebackground='red')
            modul_r_ter.ChangeDutyCycle(0)
            tp.gData_tc[1].append(0)
            
        self.conteo_on_t = not self.conteo_on_t
        
    def _pwm_presion(self):
        
        if self.conteo_on_p == False:
            self.btn_on_p.configure(state=DISABLED)
            point_pwm_p = self.scale_pwm_n.get()
            modul_valvula.ChangeDutyCycle(point_pwm_p)
            self.boton_neumatico.configure(bg = 'green', activebackground='green')            
         
        if self.conteo_on_p == True:
            self.btn_on_p.configure(state=NORMAL)
            self.boton_neumatico.configure(bg = 'red', activebackground='red')
            modul_valvula.ChangeDutyCycle(0)
        
        self.conteo_on_p = not self.conteo_on_p            
    
    def _ayuda_tab1(self):
        titulo = 'Instrucciones'
        mensaje = 'contenido'
        messagebox.showinfo(titulo, mensaje)
        
    def _ayuda_tab2(self):
        titulo = 'Instrucciones'
        mensaje = 'contenido'
        messagebox.showinfo(titulo, mensaje)
        
    def _quit(self):
        
        window = Window.window
        window.quit() #detiene el mainloop
        window.destroy() # Evita errores
        daq.GPIO.cleanup()
        sys.exit()
                    
    def _start(self):
        
        daq.dataCollector2.start()
        l.start()

        self.boton_detener.configure(state=NORMAL)
        self.boton_save.configure(state=NORMAL)
        self.boton_start.configure(state=DISABLED)
        self.btn_on_p.configure(state=NORMAL)
        self.btn_on_t.configure(state=NORMAL)
        self.boton_termico.configure(state=NORMAL)
        self.boton_neumatico.configure(state=NORMAL)
        
    def _stop(self):
        l.kill()
        daq.dataCollector2.kill()
        print("stop")
        self.boton_detener.configure(state=DISABLED)
        self.boton_start.configure(state=DISABLED)
        self.boton_reanudar.configure(state=NORMAL)
        
    def _reloading(self):
        print("reload")
        daq.dataCollector2.reload()
        l.reload()

        self.boton_reanudar.configure(state=DISABLED)
        self.boton_detener.configure(state=NORMAL)

    def _save(self):
        
        daq.dataCollector2._save_data()
        
        print("Archivo .csv creado")
         
    def _file(self):
        
        _dir = "/home/pi/Proyectos/Interfaz/Datos"
        Window.window.filename = filedialog.askopenfilename(initialdir = _dir, title="Seleccionar archivo", filetypes=(("csv files","*.csv"),("all files","*.*")))
        self.dir = Window.window.filename
        print(self.dir)
        self.boton_graf.configure(state= NORMAL)
        self.boton_graf2.configure(state= NORMAL)
        
    def save_graf(self):
        _now = daq.datetime.now().replace(microsecond=0)
        _dir = "/home/pi/Proyectos/Interfaz/Figuras/Figura"+str(_now)+".jpg"
        self.fig_data_logger_final.savefig(_dir, quality=95, dpi=500)
        print("Figura guardada")
        
    """        
    Función que actualizará los datos de la gráfica
    Se llama periódicamente desde el 'FuncAnimation'
    -------------------------------------------------
    """
    def update_line_t(num, hl, data_t, hlr, data_r, hlp, data_p, hlv, data_v):
        hl.set_data(range(len(data_t[1])), data_t[1])
        hlr.set_data(range(len(data_r[1])), data_r[1])
        hlp.set_data(range(len(data_p[1])), data_p[1])
        hlv.set_data(range(len(data_v[1])), data_v[1])
        return hl, hlr, hlp, hlv

    def _graf(self):
        
        _datos = daq.pd.read_csv(self.dir)
        
        time = _datos['Tiempo']
        T = _datos['Temperatura']
        C = _datos['Control']
        E = _datos['Error_t']
        S = _datos['Set_temp']
        
        P = _datos['Presion']
        V = _datos['Valvula']
        F = _datos['Error_p']
        Z = _datos['Set_pre']

        rango_time_t = T.count()
        rango_time_p = P.count()
        limit_t = max(T) + 5
        limit_p = max(P) + 5
        line_time_t = np.arange(rango_time_t)
        line_time_p = np.arange(rango_time_p)
                
        self.fig_data_logger_final = daq.plt.figure(dpi=100)

        """
        Grafica Temperatura
        -------------------
        """
        ax = self.fig_data_logger_final.add_subplot(321)
        daq.plt.plot(line_time_t, T, 'r',label='T [°C]')
        daq.plt.plot(line_time_t, S, 'b', label='set_t')
        daq.plt.legend(loc='upper left')
        daq.plt.ylim(0, limit_t)
        daq.plt.ylabel('Temperatura', fontsize=13)
        daq.plt.title('Curva Temperatura', fontsize=16), daq.plt.grid(True)

        """
        Grafica accion control temperatura
        ------------------------------------
        """
        ax = self.fig_data_logger_final.add_subplot(323)
        daq.plt.plot(line_time_t, C,'r', label='[%]')
        daq.plt.legend(loc='upper left')
        daq.plt.ylim(0, 100)
        daq.plt.ylabel('Acción control', fontsize=13)
        daq.plt.grid(True)

        """
        Grafica error temperatura
        -------------------------
        """
        ax = self.fig_data_logger_final.add_subplot(325)
        daq.plt.plot(line_time_t, E,'r', label='Error')
        daq.plt.legend(loc='upper left')
        daq.plt.xlabel('Time(s)', fontsize=13), daq.plt.ylabel('Error', fontsize=13)
        daq.plt.grid(True)
        """
        Grafica MC3008 presion
        ------------------------
        """
        ax = self.fig_data_logger_final.add_subplot(322)
        daq.plt.plot(line_time_p, P, 'c', label='Psi')
        daq.plt.plot(line_time_p, Z, 'k', label='set_p')
        daq.plt.legend(loc='upper left')
        daq.plt.ylim(0, limit_p)
        daq.plt.ylabel('Presion (var)', fontsize=13)
        daq.plt.title('Lectura presión', fontsize=16), daq.plt.grid(True)

        """
        Grafica MC3008 apertura valvula
        --------------------------------
        """
        ax = self.fig_data_logger_final.add_subplot(324)
        daq.plt.plot(line_time_p, V, 'c', label='[%]')
        daq.plt.legend(loc='upper left')
        daq.plt.ylabel('Aperura \n valvula', fontsize=13)
        daq.plt.grid(True)

        """
        Grafica error presion
        ----------------------
        """
        ax = self.fig_data_logger_final.add_subplot(326)
        daq.plt.plot(line_time_p, F, 'c',label='Error')
        daq.plt.legend(loc='upper left')
        daq.plt.xlabel('Time(s)', fontsize=13), daq.plt.ylabel('Error', fontsize=13)
        daq.plt.grid(True)

        """Ajusta las graficas"""
        daq.plt.tight_layout()

        #Figura embebida data logger final
        canvas = FigureCanvasTkAgg(self.fig_data_logger_final,master=Window.tab2)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.BOTTOM)
        canvas.get_tk_widget().place(x=0, y=125, height=500, width=1280)
      
        
a = Window()

# Configuramos e iniciamos la función que "animará" nuestra gráfica
argumentos = [daq.hl, daq.gData_t, daq.hlr, daq.gData_r, daq.hlp, daq.gData_p, daq.hlv, daq.gData_v]
line_ani_t = daq.animation.FuncAnimation(daq.fig, daq._Hilo_grafica.update_line_t,fargs=(argumentos),
                     save_count=0, blit=True)
gc.enable()
class _actualiza_labels(threading.Thread):
    
    def __init__(self, sleep_interval=1):
        
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self.t = daq.gData_t[1]
        self.r = daq.gData_r[1]
        self.p = daq.gData_p[1]
        self.v = daq.gData_v[1]
    def run(self):
        
        while True:
            is_killed = self._kill.wait(self._interval)
            temp = self.t[-1]
            tempc = self.r[-1]
            presion = self.p[-1]
            valvula = self.v[-1]
            
            if not is_killed:
                
                """Label temperatura actual"""
                Lt = Label(Window.toolbar_izq, text="        ", font=('Verdana', 14))
                Lt.pack(side=tkinter.BOTTOM)
                Lt.place(x=75, y=10)
                Lt = Label(Window.toolbar_izq, text=str(temp), font=('Verdana', 14))
                Lt.pack(side=tkinter.BOTTOM)
                Lt.place(x=75, y=10)
                
                """Label accion control actual"""
                Lr = Label(Window.toolbar_izq, text="         ", font=('Verdana', 14))
                Lr.pack(side=tkinter.BOTTOM)
                Lr.place(x=75, y=35)
                Lr = Label(Window.toolbar_izq, text=str(tempc), font=('Verdana', 14))
                Lr.pack(side=tkinter.BOTTOM)
                Lr.place(x=75, y=35)
                
                """label presion actual"""
                Lp = Label(Window.toolbar_der, text="         ", font=('Verdana', 14))
                Lp.pack(side=tkinter.BOTTOM)
                Lp.place(x=60, y=10)
                Lp = Label(Window.toolbar_der, text=str(presion), font=('Verdana', 14))
                Lp.pack(side=tkinter.BOTTOM)
                Lp.place(x=60, y=10)
                
                """label aperutra actual"""
                La = Label(Window.toolbar_der, text="          ", font=('Verdana', 14))
                La.pack(side=tkinter.BOTTOM)
                La.place(x=60, y=35)
                La = Label(Window.toolbar_der, text=str(valvula), font=('Verdana', 14))
                La.pack(side=tkinter.BOTTOM)
                La.place(x=60, y=35)

    def kill(self):
        self._kill.set()
        
    def reload(self):
        self._kill.clear()
        
l = _actualiza_labels(sleep_interval=1)
l.setDaemon(True)

a.window.mainloop()