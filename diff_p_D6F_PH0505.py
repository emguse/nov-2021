from smbus2 import SMBus
import time

'''
# 2021/11/07 ver.0.02
# Author : emguse
# License: MIT License
# Note: This code does not work yet. It has not been tested with a real sensor.
'''

I2C_ADDRES = 0x6C # i2c addres
CRC_ENABLE = False

RANGE_100 = 100 # ±50Pa(D6F-PH0505)
RANGE_1000 = 1000 # ±500Pa(D6F-PH5050)
RANGE_250 = 250 # 0-250Pa(D6F-PH0025)

def CRC(d):
  crc = 0xff
  for s in d:
    crc ^= s
    for i in range(8):
      if crc & 0x80:
        crc <<= 1
        crc ^= 0x131
      else:
        crc <<= 1
  return crc

class D6F_PH0505():
    '''
    # OMRON D6F-PH0505 Differential pressure sensor
    # for Raspberry Pi
    '''
    def __init__(self) -> None:
        self.d6f_addres = I2C_ADDRES
        self.bus = SMBus(1)
        self.dp = 0
        time.sleep(0.0002)
        self.initializing()
        if CRC_ENABLE == True:
            self.crc_emable()
        pass

    def initializing(self):
        self.bus.write_byte_data(self.d6f_addres, 0x0B, 0x00)

    def crc_emable(self):
        d = [0xD0, 0x49, 0x18, 0x02]
        self.bus.write_i2c_block_data(self.d6f_addres, 0x00, d)
    
    def start_measurement(self):
        d = [0xD0 ,0x40 ,0x18, 0x06]
        self.bus.write_i2c_block_data(self.d6f_addres, 0x00, d)
        #Always read after 33 milliseconds have elapsed after the command is issued.
    
    def read(self):
        d1 = [0xD0, 0x51, 0x2C]
        self.bus.write_i2c_block_data(self.d6f_addres, 0x00, d1)
        if CRC_ENABLE == True:
            raw = self.bus.read_i2c_block_data(self.d6f_addres, 0x07, 3)
            if raw[2] != CRC(raw):
                raise RuntimeError("CRC Error!!")
        else:
            raw = self.bus.read_i2c_block_data(self.d6f_addres, 0x07, 2)
        pv = raw[0] << 8 | raw[1]
        self.dp = (pv - 1024) / 60000 * RANGE_100 - RANGE_100 / 2

    def hw_reset(self):
        self.bus.write_byte_data(self.d6f_addres, 0x00, 0x80)

def main():
    d6f_ph0505 = D6F_PH0505()
    while True:
        d6f_ph0505.start_measurement()
        time.sleep(0.033)
        d6f_ph0505.read()
        print("diff_p:" + str(round(d6f_ph0505.dp, 4)))
        time.sleep(1)

if __name__ == '__main__':
    main()