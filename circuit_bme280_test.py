import board
import time
from adafruit_bme280 import basic as adafruit_bme280

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

while True:
    print("\nTemperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%" % bme280.relative_humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)
    time.sleep(2)

'''
Circuit Python demo code for "Adafruit Feather STM32F405 Express" 
connected to "SparkFun Atmospheric Sensor Breakout - BME280 (Qwiic)" 
with STEMMAQT.
'''