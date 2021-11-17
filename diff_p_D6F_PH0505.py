from smbus2 import SMBus
import time

'''
- 2021/11/17 ver.1.00
- Author : emguse
- License: MIT License
'''

I2C_ADDRES = 0x6C # i2c addres
CRC_ENABLE = False

RANGE_100 = 100 # ±50Pa(D6F-PH0505)
RANGE_1000 = 1000 # ±500Pa(D6F-PH5050)
RANGE_250 = 250 # 0-250Pa(D6F-PH0025)

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

class D6F_PH0505():
    '''
    ### Class for using OMRON D6F-PH0505 Differential pressure sensor with Raspberry Pi
    1. Instantiation
    2. start_measurement()
    3. 33ms or more elapsed
    4. read()
    5. Using the 'dp' variable
    '''
    def __init__(self) -> None:
        self.d6f_addres = I2C_ADDRES
        self.crc_enable = CRC_ENABLE
        self.bus = SMBus(1)
        self.dp = 0
        time.sleep(0.0002)
        self.initializing()
        if self.crc_enable == True:
            self.crc_emable()
    def initializing(self):
        '''
        ### Write the command to initialize the sensor to the register. This command must be executed at least 200 usec after power-on.
        - It is included in __init__ and does not need to be called again.
        '''
        self.bus.write_byte_data(self.d6f_addres, 0x0B, 0x00)
    def crc_emable(self):
        '''
        ### Set the bit in the CRC Calculation Function Register to '1'.
        - To call this method, set the variable 'crc_enable' to 'True' in advance.
        '''
        d = [0xD0, 0x49, 0x18, 0x02]
        self.bus.write_i2c_block_data(self.d6f_addres, 0x00, d)
    def start_measurement(self):
        '''
        ### Issue the measurement start command.
        - You can read the value from the sensor more than 33m after calling this method.
        '''
        d = [0xD0 ,0x40 ,0x18, 0x06]
        self.bus.write_i2c_block_data(self.d6f_addres, 0x00, d)
    def read(self):
        '''
        ### Issues the measurement data read command.
        - At least 33 ms must have elapsed since the call to start_measurement().
        - After reading the raw data, the conversion is performed and the differential pressure value is stored in the variable 'dp'.
        - If 'crc_enable' is 'True', the CRC byte is also read and calculated.
        - The CRC calculation result is compared with the CRC byte, and if there is a mismatch, 'RuntimeError' is called.
        '''
        d2 = [0xD0, 0x51, 0x2C]
        self.bus.write_i2c_block_data(self.d6f_addres, 0x00, d2)
        if self.crc_enable == True:
            raw = self.bus.read_i2c_block_data(self.d6f_addres, 0x07, 3)
            if raw[2] != CRC(raw[:2]):
                raise RuntimeError("CRC Error!!")
        else:
            raw = self.bus.read_i2c_block_data(self.d6f_addres, 0x07, 2)
        pv = raw[0] << 8 | raw[1]
        self.dp = (pv - 1024) / 60000 * RANGE_100 - RANGE_100 / 2
    def hw_reset(self):
        '''
        ### A hardware reset is performed by writing 1 to bit 7 of the power sequence register.
        '''
        self.bus.write_byte_data(self.d6f_addres, 0x00, 0x80)

def main():
    d6f_ph0505 = D6F_PH0505()
    while True:
        d6f_ph0505.start_measurement()
        time.sleep(0.033)
        d6f_ph0505.read()
        print("diff_p:" + str(round(d6f_ph0505.dp, 4)))
        time.sleep(0.005)

if __name__ == '__main__':
    main()