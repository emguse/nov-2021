from thermalprinter import *
from PIL import Image,ImageDraw,ImageFont

'''
- 2021/11/27 ver.1.01
- Author : emguse
- License: MIT License
'''

# Font setting
FONT_PATH = './Mplus1-Regular.ttf'
FONT_SIZE = 24

# Image area　
WIDTH = 500
HEIGHT = 32

class PrintWithDpEh600():
    '''
    ### Print for the DP-EH600 using the 'thermalprinter' module.
    - need to set serial to 'ON' and serial console to 'OFF' in raspi-config.
    - If you do not use RTS/CTS for flow control, please limit the image height.
    - The output is not sent as serial characters via printer commands, but as an image using the Pillow module.
    - The output is not limited to the fonts owned by the printer, but can be in any typeface and language you like.

    How to use
    1. p = PrintWithDpEh600()
    1. data = "YYYY-mm-ddTHH:MM:SS:ffffff"
    1. p.printing(data)
    1. p.line_feed(2)
    '''
    def __init__(self) -> None:
        self.width = WIDTH
        self.height = HEIGHT
        self.font_path = FONT_PATH
        self.font_size = FONT_SIZE
        self.set_font()
    def set_canvas(self) -> None:
        '''
        ### When you call the 'set_canvas()' method, the canvas will be initialized with the pre-defined 'width' and 'height' variables.
        - Note that 'height' will be severely limited if the printer is not RTS/CTS flow controlled.
        - For repetitive output, the campus needs to be refreshed each time, but the 'set_canvas()' method is included in the 'printing()' method, so it usually does not need to be called alone.
        '''
        self.image = Image.new('1', (self.width,self.height), 255)
        self.draw = ImageDraw.Draw(self.image)
    def set_font(self) -> None:
        '''
        ### Calling the 'set_font()' method will create an image font with the pre-set 'font_path' and 'font_size' variables.
        - If you want to specify a font or font size other than the default setting, rewrite the variables and then call this method.
        - If you change the font and font size, you will need to adjust the campus size as well in many cases.
        - The font file must be placed in the 'font_path' location in '.ttf' or '.otf' format.
        '''
        self.font = ImageFont.truetype(self.font_path, self.font_size, encoding='unic')
    def printing(self, data :str) -> None:
        '''
        ### Execute printing. After initializing the campus, it generates an image from the image font using the received string and outputs it.
        - Printing is performed via the 'Try - Except' statement and any exceptions raised are ignored because 'Except' is 'pass'.
        '''
        try:
            with ThermalPrinter(port='/dev/serial0', baudrate=115200) as printer:
                self.set_canvas()
                self.draw.text((0, 0), str(data), font=self.font, fill=0)
                printer.image(self.image)
        except:
            print('Printer other errors')
            pass
    def line_feed(self, line :int) -> None:
        '''
        ### Execute the paper feed. Sends an integer value of the received value to execute paper feed.
        - The paper feed is executed via the 'Try - Except' statement, and any exceptions raised will be ignored since 'Except' is 'pass'.
        '''
        try:
            with ThermalPrinter(port='/dev/serial0', baudrate=115200) as printer:
                printer.feed(line)
        except:
            print('line feed error')
            pass
    def online(self) -> None:
        try:
            with ThermalPrinter(port='/dev/serial0', baudrate=115200) as printer:
                printer.online()
        except:
            print('printer error')
            pass

def main():
    p = PrintWithDpEh600()
    import datetime
    now = datetime.datetime.now()
    p.printing(now)
    p.line_feed(2)

    p = PrintWithDpEh600()
    data = ['2021-11-27T20:51:11.762737', 'DP:-0.3558  delta P:0.2208']
    for s in data:
        p.set_canvas()
        p.printing(s)
    p.line_feed(1)

if __name__ == '__main__':
    main()