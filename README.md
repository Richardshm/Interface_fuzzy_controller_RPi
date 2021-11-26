# Digital HMI scale with rfid tagging and sending data to thikspeak server.

It consists of a nodemcu microcontroller, which takes weight measurements taking into account rfid tags to add a 
certain quantity of a material to the inventory, the nodmcu control uses an HMI interface and also the data taken 
is stored in a thinkspeak server (https://thingspeak.com/channels/1546302).

### Pre-requisitos 📋

1.Nodemcu V3 (1).
```
Any microcontroller can be used, only the pin layout must be taken into account.
```
2.Load cell (1).

3.HX711 Load Cell Transmitter Module(1).

4.RFID Reader module RC522(1).

5.RFID tags (3).

### Installation 🔧

Save the .ino file on the nodemcu, you can see how to configure the nodemcu with the iddle of arduino here (https://github.com/esp8266/Arduino).

## Built with 🛠️

* [Librería Arduino List](https://github.com/luisllamasbinaburo/Arduino-List) - Arduino library that implements a dynamic array.
* [HX711](https://github.com/bogde/HX711) - An Arduino library to interface the Avia Semiconductor HX711.
* [MFRC522](https://github.com/miguelbalboa/rfid) - Arduino RFID Library for MFRC522.
* [ThingSpeak](https://github.com/mathworks/thingspeak-arduino) - ThingSpeak Communication Library for Arduino, ESP8266 and ESP32.

## Authors ✒️

* **Richard Hernández** - * All * - (https://github.com/Richardshm/)


## License 📄

This project is licensed under the GNU avr-gcc toolchain, GCC ARM Embedded toolchain, avr-libc, avrdude, bossac, openOCD and code from Processing and Wiring.
