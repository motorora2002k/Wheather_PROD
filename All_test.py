import RPi.GPIO as GPIO
import dht11
from gpiozero import MCP3008
import Adafruit_BMP.BMP085 as BMP085

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

uv = MCP3008(0)

sensor = BMP085.BMP085()

def uv_range():
    global uv_mv
    global uv_index
    uv_mv = int(3300 * uv.value)
    if uv_mv in range (0,227):
        uv_index = 0
    elif uv_mv in range(227,318):
        uv_index = 1
    elif uv_mv in range(318,408):
        uv_index = 2
    elif uv_mv in range(408,503):
        uv_index = 3
    elif uv_mv in range(503,606):
        uv_index = 4
    elif uv_mv in range(606,696):
        uv_index = 5
    elif uv_mv in range(696,795):
        uv_index = 6
    elif uv_mv in range(795,881):
        uv_index = 7
    elif uv_mv in range(881,976):
        uv_index = 8
    elif uv_mv in range(976,1079):
        uv_index = 9
    elif uv_mv in range(1079,1170):
        uv_index = 10
    elif uv_mv >= 1170:
        uv_index = 11

#while True:
uv_range()
instance = dht11.DHT11(pin = 14)
result = instance.read()
#if result.is_valid():
#print("UV: %-3.5f V" % (3.3 * uv.value), end = "\r")
print("UV index: ", uv_index)
print("Humidity: %-3.1f %%" % result.humidity)
print('Temp = {0:0.2f} ^C'.format(sensor.read_temperature()))
print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
print(end = "\r")
#print("UV index: ", uv_index, "Humidity: %-3.1f %%" % result.humidity, 'Temp = {0:0.2f} ^C'.format(sensor.read_temperature()), 'Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()), 'Altitude = {0:0.2f} m'.format(sensor.read_altitude()), 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()), end = "\r") 