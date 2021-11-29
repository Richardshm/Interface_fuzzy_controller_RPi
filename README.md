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

* [Librería Arduino List](https://github.com/luisllamasbinaburo/Arduino-List) - Arduino library that implements a dynamic array.
* [HX711](https://github.com/bogde/HX711) - An Arduino library to interface the Avia Semiconductor HX711.
* [MFRC522](https://github.com/miguelbalboa/rfid) - Arduino RFID Library for MFRC522.
* [ThingSpeak](https://github.com/mathworks/thingspeak-arduino) - ThingSpeak Communication Library for Arduino, ESP8266 and ESP32.

## Authors ✒️

* **Richard Hernández** - * All * - (https://github.com/Richardshm/)


## License 📄

This project is licensed under the GNU avr-gcc toolchain, GCC ARM Embedded toolchain, avr-libc, avrdude, bossac, openOCD and code from Processing and Wiring.
