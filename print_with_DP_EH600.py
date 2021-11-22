from thermalprinter import *
from PIL import Image,ImageDraw,ImageFont

'''
Print test for the DP-EH600 using the 'thermalprinter' module.
need to set serial to 'ON' and serial console to 'OFF' in raspi-config.
'''

FONT_PATH = './Mplus1-Regular.ttf'
FONT_SIZE = 24

# Image area
width = 500
height = 32
# If you do not use RTS/CTS for flow control, 
# please limit the height.

class PrintWithDpEh600():
    def __init__(self) -> None:
        self.width = 500
        self.height = 32
        self.set_canvas()
        self.font_path = FONT_PATH
        self.font_size = FONT_SIZE
        self.set_font()
    def set_canvas(self) -> None:
        self.image = Image.new('1', (self.width,self.height), 255)
        self.draw = ImageDraw.Draw(self.image)
    def set_font(self) -> None:
        self.font = ImageFont.truetype(self.font_path, self.font_size, encoding='unic')
    def printing(self, data :str) -> None:
        try:
            with ThermalPrinter(port='/dev/serial0', baudrate=115200) as printer:
                self.draw.text((0, 0), str(data), font=self.font, fill=0)
                printer.image(self.image)
        except:
            pass
    def line_feed(self, line :int):
        try:
            with ThermalPrinter(port='/dev/serial0', baudrate=115200) as printer:
                printer.feed(line)
        except:
            pass

def main():
    p = PrintWithDpEh600()
    p.printing("１２３４５６７８９０１２３４５６")
    p.line_feed(2)

if __name__ == '__main__':
    main()