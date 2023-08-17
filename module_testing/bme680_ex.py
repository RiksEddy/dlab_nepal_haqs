import uos
import machine
import time
from machine import Pin, I2C
from bme680 import *

#brown board
I2C_PORT = 1
I2C_SDA = 26
I2C_SCL = 19
"""
#green board
I2C_PORT = 1
I2C_SDA = 18
I2C_SCL = 19
"""

i2c=I2C(I2C_PORT,sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=400000)

bme = BME680_I2C(i2c=i2c)

print(', '.join(["temperature", "humidity", "pressure", "gas"])+'\n')

while True:
    temperature = str(rou								nd(bme.temperature, 2)) + ' C'
    humidity = str(round(bme.humidity, 2)) + ' %'
    pressure = str(round(bme.pressure, 2)) + ' hPa'
    gas = str(round(bme.gas/1000, 2)) + ' KOhms'
    print(', '.join([temperature, humidity, pressure, gas])+'\n')
    time.sleep(1.0)
    
    