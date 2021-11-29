# Digital HMI scale with rfid tagging and sending data to thikspeak server.

Consists of a RPi running a fuzzy controller to regulate two processes one thermal and one pneumatic, both processes are controlled 
by pwm to their respective actuators, also an HMI interface is used to enter and vary the controller parameters, graphs in real time 
the variables and the data are saved in csv to be plotted and analyzed.

## Pre-requisitos 📋

1.Raspberry Pi 3B.
```
Any microcontroller that uses Python can be used, and the pin layout must be taken into account.
```

## Thermal controller

1.RTD PT100 (1).

2.Thermal resistance (1).

3.RTD to digital circuit (1).

4.AC-DC pwm convert circuit (1).

## Pneumatic controller

1.MBS3000 (1).

2.Compressor (1).

3.I-V with ADC circuit (1).

4.Pwm-DC convert circuit (1).

### Installation 🔧

Clone or save the files on your deskopt, you can take a more detailed look at the operation of the system, its circuits and 
connections in the following article (https://publicaciones.eafit.edu.co/index.php/ingciencia/article/view/6555).

## Built with 🛠️

* [Tkinter](https://docs.python.org/es/3/library/tk.html) - Graphical user interfaces.
* [Numpy](https://numpy.org/doc/stable/) - Fundamental package for scientific computing in Python.
* [Matplotlib](https://matplotlib.org/stable/users/index) - Comprehensive library for creating static, animated, and interactive visualizations in Python.
* [MCP3008](https://github.com/adafruit/Adafruit_MCP3008) - 8-Channel 10-Bit ADC.
* [Pandas](https://pandas.pydata.org/docs/) - Fast, powerful, flexible and easy to use open source data analysis and manipulation tool.
* [scikit-fuzzy](https://github.com/scikit-fuzzy/scikit-fuzzy) - Fuzzy Logic SciKit (Toolkit for SciPy).

## Authors ✒️

* **Richard Hernández** - * All * - (https://github.com/Richardshm/)
* * **Francisco Moreno** - * Director * - (https://orcid.org/0000-0002-5227-1238 )
* * **Sergio Castro** - * Co-director * - (https://orcid.org/0000-0003-0962-9916 )

## License 📄

This project is licensed under the GNU, GPL and the python software foundation licence(PSF).
