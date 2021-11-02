from smbus2 import SMBus
import time

# All sensoers (Amphenol) DLHR-F50D-E1BD-C-NAV8
# for Raspberry Pi

ADDRESS = 0x29

OS_DIG = 0.5 * 2 ** 24 # For Differential Operating Range sensors
FSS_IN_H2O = 2 * 0.5 # For Differential Operating Range sensors : 2 x Full Scale Pressure.
PA_CONVERSION = 249.089 # Conversion factor from "inH2O" to "Pa"
FSS_PA = FSS_IN_H2O * PA_CONVERSION

START_SINGLE = 0xAA
START_AVERAGE2 = 0xAC
START_AVERAGE4 = 0xAD
START_AVERAGE8 = 0xAE
START_AVERAGE16 = 0xAF

class DLHR_F50D():
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

    def send_start(self):
        self.bus.write_byte_data(self.address, 0x00, START_SINGLE)
    
    def status_read(self):
        self.status = self.bus.read_byte_data(self.address, 0x00)
        if self.status and 0x40 == 0x40:
            self.power = True
        else:
            self.power = False
        if self.status and 0x20 == 0x20:
            self.busy = True
        else:
            self.busy = False
        self.mode = (self.status and 0x18) >> 3
        if self.status and 0x04 == 0x04:
            self.memory_error = True
        else:
            self.memory_error = False
        if self.status and 0x01 == 0x01:
            self.alu_error = True
        else:
            self.alu_error = False

    def read_busy(self) -> bool:
        self.status = self.bus.read_byte_data(self.address, 0x00)
        if self.status and 0x20 == 0x20:
            self.busy = True
        else:
            self.busy = False
        return self.busy

    def poll_busy(self):
        while self.read_busy():
            time.sleep(0.00001)
    
    def correction_p(self):
        self.pressure = 1.25 * ((self.rawp - OS_DIG)/ 2**24) * FSS_PA

    def correction_t(self):
        self.temprature = (self.rawt * 125)/ 2**24 - 40

    def read(self):
        data = self.bus.read_i2c_block_data(self.address, 0x00, 7)
        self.rawp = data[2] << 16 | data[3] << 8 | data[4]
        self.rawt = data[5] << 16 | data[6] << 8 | data[7]

    def read_p(self):
        self.send_start()
        self.poll_busy()
        self.read()
        self.correction_p()
    
    def read_t(self):
        self.send_start()
        self.poll_busy()
        self.read()
        self.correction_t()

def main():
    dlhr_f50d = DLHR_F50D()
    while True:
        dlhr_f50d.read_p()
        print(dlhr_f50d.pressure)
        time.sleep(0.01)

if __name__ == '__main__':
    main()