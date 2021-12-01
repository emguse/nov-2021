import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice

RANGE_100 = 100  # ±50Pa(D6F-PH0505)
RANGE_1000 = 1000  # ±500Pa(D6F-PH5050)
RANGE_250 = 250  # 0-250Pa(D6F-PH0025)

I2C_ADDRES = 0x6C  # i2c addres
CRC_ENABLE = False

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)  # Pi Pico RP2040 (SDA0,SCL0)
device = I2CDevice(i2c, I2C_ADDRES)

with device:
    init_order = bytes([0x0B, 0x00])
    time.sleep(0.0002)
    device.write(init_order)
while True:
    with device:
        start_order = bytes([0x00, 0xD0, 0x40, 0x18, 0x06])
        device.write(start_order)
        time.sleep(0.033)
    with device:
        read_order = bytes([0x00, 0xD0, 0x51, 0x2C])
        device.write(read_order)
        read_addres = bytes([0x07])
        raw = bytearray(2)
        device.write_then_readinto(read_addres, raw)
        pv = raw[0] << 8 | raw[1]
        diff_p = (pv - 1024) / 60000 * RANGE_100 - RANGE_100 / 2
        print(diff_p)
