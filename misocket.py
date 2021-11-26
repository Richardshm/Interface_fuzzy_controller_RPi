import websocket
import time

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
Se configura el tipo de PT100
------------------------------
"""
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D26)  # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=3)

"""
Se configura el MCP3008
----------------------
"""
SPI_PORT   = 0
SPI_DEVICE = 1
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


def activar_error(ws, error):
    print(error)

def activar_cerrar(ws):
    print("### COMUNICACION FINALIZADA ###")

def activar_abrir(ws):
    while True:
        
        temp = sensor.temperature
        temp = round(temp, 2)
        temp = str(temp)

        res = sensor.resistance
        res = round(res, 2)
        res = str(res)
        
        presion = mcp.read_adc(2)
        presion = ((presion*20)/420)
        presion = round(presion,2)
        presion = str(presion)
        
        valvula = mcp.read_adc(1)
        valvula = ((valvula*100)/930)
        valvula = int(valvula)
        valvula = str(valvula)
        
        lista = [temp, res, presion, valvula]
    
        ws.send(str(lista))
   
        time.sleep(1)
'''
def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())
'''

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://10.0.17.249:8000",
                              on_error = activar_error,
                              on_close = activar_cerrar)
    ws.on_open = activar_abrir
    ws.run_forever()