# Wheather_PROD

## 一、專案緣起

對於天氣本身就有一定的研究，想說透過本們IoT的課程，配合Raspberry Pi的建置，研究並建置一個天氣偵測的專案。

## 二、專案設備

  1. Raspberry Pi 4 \* 1台
  2. HT22 \* 1個
  3. BMP180 \* 1個
  4. GUVA-S12SD \* 1個
  5. MCP3008 \* 1個
  6. 麵包板 \* 1個

## 三、專案建置
  1. 安裝DHT11程式庫
```
pip3 install dht11
```
  2. 測試DHT22運作狀況
撰寫一個 Python 程式「dht11\_test.py」，用來讀取感測器溫濕度的輸出。
```
import RPi.GPIO as GPIO

import dht11

# intialise GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

while True:
  instance = dht11.DHT11(pin = 14)
  result = instance.read()
  if result.is\_valid():
    print("Temperature: %-3.1f C" % result.temperature, "Humidity: %-3.1f %%" % result.humidity, end = "\r")
```
執行 dht11\_test.py 程式，可以嘗試在感測器旁呼氣，檢查溫度與濕度是否有正常運作讀取數值。

  3. 連接類比數位轉換器(MCP3008)
由於紫外線感測器輸出為類比訊號，所以我們要利用類比數位轉換器 MCP3008 (ADC, analogue-to-digital converter)來將數值作轉換讀取，轉換器總共有 8 個輸入通道。
![image](https://github.com/motorora2002k/Wheather_PROD/assets/134987892/cdc60fcf-bcc5-41e4-9de8-69c5bb725c58)
因為MCP3008是SPI通訊介面，需要透過Python 3在Raspberry Pi配置工具啟用SPI，並在Terminal輸入以下指令便可安裝：
```
sudo apt-get install python3-spidev
```
※紫外線感測器可以任意連接到MCP3008的8個輸入通道，本實作使用第 0 個輸入通道（CH0）。

  4. 連接HT22、MCP3008、紫外線感測器（GUVA-S12D）及壓力感測器（BMP180）
![image](https://github.com/motorora2002k/Wheather_PROD/assets/134987892/93037b0b-b1ae-4eaa-a283-05a00403b6c0)
  5. 紫外線測試
建立一個程式「uv\_test.py」來測試紫外線感測器。
```
from gpiozero import MCP3008

uv = MCP3008(0)

#測試紫外線是否可以正常讀取
while True:
  print("UV: %-3.5f V" % (3.3 \* uv.value), end = "\r")
```
  6. 紫外線指數
轉換電壓數值成國際標準的紫外線指數。
![image](https://github.com/motorora2002k/Wheather_PROD/assets/134987892/5f5b0df3-2fbe-4e1a-a27c-952815dc64b2)
   GND：0V（接地）
   VCC：3.3V至5.5V
   OUT：0V至1V（0至10 UV指數）
```
from gpiozero import MCP3008

uv = MCP3008(0)

#定義不同電壓的UV值
def uv\_range():
  global uv\_mv
  global uv\_index
  uv\_mv = int(3300 \* uv.value)
  if uv\_mv in range (0,227):
    uv\_index = 0
  elif uv\_mv in range(227,318):
    uv\_index = 1
  elif uv\_mv in range(318,408):
    uv\_index = 2
  elif uv\_mv in range(408,503):
    uv\_index = 3
  elif uv\_mv in range(503,606):
    uv\_index = 4
  elif uv\_mv in range(606,696):
    uv\_index = 5
  elif uv\_mv in range(696,795):
    uv\_index = 6
  elif uv\_mv in range(795,881):
    uv\_index = 7
  elif uv\_mv in range(881,976):
    uv\_index = 8
  elif uv\_mv in range(976,1079):
    uv\_index = 9
  elif uv\_mv in range(1079,1170):
    uv\_index = 10
  elif uv\_mv \>= 1170:
    uv\_index = 11

while True:
  uv\_range()
  print("UV index: ",uv\_index, end = "\r")
```
※在「uv\_index.py」程式碼中，我們建立一個uv\_range功能，以及一系列的if和elif來處理感測器所讀取到的數直落在哪個範圍(將uv mv 轉換為微伏特)，並設定相對應的紫外線指數(uv\_index)

  7. 安裝BMP180，並寫一個bmp180\_test.py進行設備測試
```
import Adafruit\_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()

#顯示溫度
print('Temp = {0:0.2f} \*C'.format(sensor.read\_temperature()))

#顯示氣壓
print('Pressure = {0:0.2f} Pa'.format(sensor.read\_pressure()))

#顯示高度
print('Altitude = {0:0.2f} m'.format(sensor.read\_altitude()))

#顯示海平面氣壓
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read\_sealevel\_pressure()))
```
  8. 最後整合所有程式碼。
```
import RPi.GPIO as GPIO
import dht11
from gpiozero import MCP3008
import Adafruit\_BMP.BMP085 as BMP085

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

uv = MCP3008(0)

sensor = BMP085.BMP085()

def uv\_range():
  global uv\_mv
  global uv\_index
  uv\_mv = int(3300 \* uv.value)
  if uv\_mv in range (0,227):
    uv\_index = 0
  elif uv\_mv in range(227,318):
    uv\_index = 1
  elif uv\_mv in range(318,408):
    uv\_index = 2
  elif uv\_mv in range(408,503):
    uv\_index = 3
  elif uv\_mv in range(503,606):
    uv\_index = 4
  elif uv\_mv in range(606,696):
    uv\_index = 5
  elif uv\_mv in range(696,795):
    uv\_index = 6
  elif uv\_mv in range(795,881):
    uv\_index = 7
  elif uv\_mv in range(881,976):
    uv\_index = 8
  elif uv\_mv in range(976,1079):
    uv\_index = 9
  elif uv\_mv in range(1079,1170):
    uv\_index = 10
  elif uv\_mv \>= 1170:
    uv\_index = 11

uv_range()
instance = dht11.DHT11(pin = 14)
result = instance.read()

print("UV index: ", uv\_index)
print("Humidity: %-3.1f %%" % result.humidity)
print('Temp = {0:0.2f} *C'.format(sensor.read\_temperature()))
print('Pressure = {0:0.2f} Pa'.format(sensor.read\_pressure()))
print('Altitude = {0:0.2f} m'.format(sensor.read\_altitude()))
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read\_sealevel\_pressure()))
print(end = "\r")
```
## 四、專案總結

這樣就完成了一個簡易的氣象偵測站台，因為BMP180未能偵測濕度，故還是需要使用DHT22或DHT11來進行濕度的監測，本項專案後續可以不斷擴充（如：風速計、雨量、風向…等等）

## 五、DEMO
[![image](https://github.com/motorora2002k/Wheather_PROD/assets/134987892/d7c4b8f6-eab2-4f7c-b66d-c374f056b3aa)](https://youtu.be/abUCQVT44-k)

## 六、資料來源
[樹莓派感測器實作(三)：簡易氣象站](https://www.circuspi.com/index.php/2022/09/02/weather-station/)

[Sensors - Pressure, Temperature and Altitude with the BMP180](https://thepihut.com/blogs/raspberry-pi-tutorials/18025084-sensors-pressure-temperature-and-altitude-with-the-bmp180)

[用树莓派DIY自动“气象站”](https://shumeipai.nxez.com/2017/12/04/how-to-build-a-raspberry-pi-weather-station.html)
