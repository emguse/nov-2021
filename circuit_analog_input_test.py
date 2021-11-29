import board
from analogio import AnalogIn
import time

analog_in1 = AnalogIn(board.A1)

def get_voltage(pin):
    return (pin.value * 3.3 / 65536)

while True:
    print((get_voltage(analog_in1),))
    time.sleep(1)

#import board
#dir(board)
#help("modules")
#print("Hello World!")
