import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice

RANGE_100 = 100  # ±50Pa(D6F-PH0505)
RANGE_1000 = 1000  # ±500Pa(D6F-PH5050)
RANGE_250 = 250  # 0-250Pa(D6F-PH0025)

I2C_ADDRES = 0x6C  # i2c addres
CRC_ENABLE = False

class DifferentialPressureSensorD6F_PH0505():
    def __init__(self, i2c: I2C) -> None:
        self.d6f_addres = I2C_ADDRES
        self.crc_enable = CRC_ENABLE
        self.device = I2CDevice(i2c, self.d6f_addres)
        self.diff_p = 0
        with self.device:
            init_order = bytes([0x0B, 0x00])
            time.sleep(0.0002)
            self.device.write(init_order)
        if self.crc_enable == True:
            with self.device:
                crc_enable_order = bytes([0xD0, 0x49, 0x18, 0x02])
                self.device.write(crc_enable_order)
    def CRC(d):
        crc = 0x00
        for s in d:
            crc ^= s
            for _ in range(8):
                if crc & 0x80:
                    crc <<= 1
                    crc ^= 0x131
                else:
                    crc <<= 1
        return crc
    def start_order(self) -> None:
        with self.device:
            start_order = bytes([0x00, 0xD0, 0x40, 0x18, 0x06])
            self.device.write(start_order)
            time.sleep(0.033)
    def read_order(self) -> None:
        with self.device:
            read_order = bytes([0x00, 0xD0, 0x51, 0x2C])
            self.device.write(read_order)
            read_addres = bytes([0x07])
            if self.crc_enable == True:
                raw = bytearray(3)
                self.device.write_then_readinto(read_addres, raw)
                pv = raw[0] << 8 | raw[1]
                self.diff_p = (pv - 1024) / 60000 * RANGE_100 - RANGE_100 / 2
                if raw[2] != self.CRC(raw[:2]):
                    raise RuntimeError("CRC Error!!")
            else:
                raw = bytearray(2)
                self.device.write_then_readinto(read_addres, raw)
                pv = raw[0] << 8 | raw[1]
                self.diff_p = (pv - 1024) / 60000 * RANGE_100 - RANGE_100 / 2
    def hw_reset(self):
        with self.device:
            reset_order = bytes([0x00, 0x80])
            self.device.write(reset_order)

def main(): 
    I2C_SCL = board.GP1
    I2C_SDA = board.GP0  
    i2c = busio.I2C(scl=I2C_SCL, sda=I2C_SDA)
    d6f_ph0505 = DifferentialPressureSensorD6F_PH0505(i2c)
    while True:
        d6f_ph0505.start_order()
        d6f_ph0505.read_order()
        print("diff_p:" + str(round(d6f_ph0505.diff_p, 4)))

if __name__ == "__main__":
    main()

