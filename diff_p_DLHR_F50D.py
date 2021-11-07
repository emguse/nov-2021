from smbus2 import SMBus
import time

'''
- 2021/11/07 ver.1.02
- Author : emguse
- License: MIT License
'''

ADDRESS = 0x29

OS_DIG = 0.5 * 2 ** 24 # For Differential Operating Range sensors
FSS_IN_H2O = 2 * 0.5 # For Differential Operating Range sensors : 2 x Full Scale Pressure.
PA_CONVERSION = 249.089 # Conversion factor from "inH2O" to "Pa"
FSS_PA = FSS_IN_H2O * PA_CONVERSION # FSS/2 for "Pa"

START_SINGLE = 0xAA
START_AVERAGE2 = 0xAC
START_AVERAGE4 = 0xAD
START_AVERAGE8 = 0xAE
START_AVERAGE16 = 0xAF

class DifferentialPressureSensorDLHR_F50D():
    '''
    ### Class for using All sensoers (Amphenol) DLHR-F50D-E1BD-C-NAV8 with Raspberry Pi
    For simple use, you can instantiate it and then call the method "read_p()" to get the differential pressure in the return value.
    '''
    def __init__(self) -> None:
        self.address = ADDRESS
        self.status = 0x00
        self.power = False
        self.busy = False
        self.mode = 0x00
        self.memory_error = False
        self.alu_error = False
        self.rawp = 0
        self.rawt = 0
        self.pressure = 0
        self.temprature = 0
        self.bus = SMBus(1)
        pass

    def send_start(self) -> None:
        '''Send Measurement Commands to the sensor when called'''
        self.bus.write_byte(self.address, START_AVERAGE4)
    
    def status_read(self) -> None:
        self.status = self.bus.read_byte(self.address)
        if self.status & 0x40 == 0x40:
            self.power = True
        else:
            self.power = False
        if self.status & 0x20 == 0x20:
            self.busy = True
        else:
            self.busy = False
        self.mode = (self.status & 0x18) >> 3
        if self.status & 0x04 == 0x04:
            self.memory_error = True
        else:
            self.memory_error = False
        if self.status & 0x01 == 0x01:
            self.alu_error = True
        else:
            self.alu_error = False

    def read_busy(self) -> bool:
        '''
        ### After reading the status register, it retrieves only the Busy status from the result and returns the result.
        Return:
            Sensor busy status (bool)
        '''
        self.status = self.bus.read_byte(self.address)
        if self.status & 0x20 == 0x20:
            self.busy = True
        else:
            self.busy = False
        return self.busy
    
    def poll_busy(self):
        '''Keep reading the status until Busy becomes False.'''
        while self.read_busy():
            pass
    
    def correction_p(self) -> None:
        '''Returns the raw pressure value as a translated pressure value.'''
        self.pressure = 1.25 * ((self.rawp - OS_DIG)/ 2**24) * FSS_PA

    def correction_t(self) -> None:
        '''Returns the raw temperature value as a translated temperature value.'''
        self.temprature = (self.rawt * 125)/ 2**24 - 40

    def read(self):
        '''Get the raw value from the sensor.'''
        data = self.bus.read_i2c_block_data(self.address, 0x00, 7)
        self.rawp = (data[1] << 16) | (data[2] << 8) | data[3]
        self.rawt = (data[4] << 16) | (data[5] << 8) | data[6]

    def read_p(self) -> float:
        '''
        ### Get the corrected differential pressure
        Return:
            Corrected differential pressure
        '''
        self.send_start()
        self.poll_busy()
        self.read()
        self.correction_p()
        return self.pressure
    
    def read_t(self) -> float:
        '''
        ### Get the corrected temprature
        Return:
            Corrected temprature
        '''
        self.send_start()
        self.poll_busy()
        self.read()
        self.correction_t()
        return self.temprature

def main(): # Sample usage
    ZERO_OFFSET = 2 # Zero point correction
    dlhr_f50d = DifferentialPressureSensorDLHR_F50D()
    while True:
        p = dlhr_f50d.read_p()
        print("pressure :" + str(round(p - ZERO_OFFSET ,4)))
        time.sleep(1)

if __name__ == '__main__':
    main()