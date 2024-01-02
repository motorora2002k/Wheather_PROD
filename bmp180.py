import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()

//顯示溫度
print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
//顯示氣壓
print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
//顯示高度
print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
//顯示海平面氣壓
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
