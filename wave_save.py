import numpy as np
import struct
import wave
import datetime

'''
- 2021/11/12 ver.0.02
- Author : emguse
- License: MIT License
'''

class WavSave():
    '''
    ### This class uses the wave module to provide a series of operations to save the received array of sequential numbers as a '.wav' file.
    - Passing the array as an argument to the 'save()' method will save the 'wave.wav' file.
    - You can override the parameters by executing the 'set_' method.
    - The sample size supports only 16bit.
    '''
    def __init__(self) -> None:
        self.nchannels :int = 1 
        self.sampwidth :int = 2 # 2byte = 16bits
        self.framerate :int = 44100
        self.save_dir :str = './'
        self.fname :str = 'wave'
        self.ext :str = '.wav'
        self.path :str = ''
        self.max_value = 1
        self.bin_wf :list = []
        pass
    def set_wav_param(self, nchannels :int = 1, sampwidth: int = 2, framerate: int = 44100) -> None:
        '''
        ### Set the parameter to be passed to the wave module.
        - Do not pass any value other than 2 to the 'sampwidth' argument, as only 16-bit is supported.
        - Do not set values that are not supported by the wave module.
        '''
        self.nchannels = nchannels
        self.sampwidth = sampwidth
        self.framerate = framerate
    def set_path(self, save_dir :str, file_name :str = 'wave', file_ext :str = '.wav') -> None:
        '''
        ### Set the path to save the file.
        - You can override the directory, file name and extension.
        - Default path is './wave.wav'.
        '''
        self.save_dir = save_dir
        self.fname = file_name
        self.ext = file_ext
        self.path = self.save_dir + self.fname + self.ext
    def set_norm(self, max_value) -> None:
        '''
        ### set the maximum value in the array that will be passed as a waveform.
        - The value received as an argument will be used for normalization.
        - Default value is '1'
        '''
        self.max_value
    def to_bin(self, data) -> None:
        '''
        ### Use the Stract module to provide 16-bit binaryization
        - The array received as an argument is normalized by '32767 / max_value' and then binaryized.
        '''
        wf16 = [int(x * 32767.0 / self.max_value) for x in data] # 16-bit normalization
        self.bin_wf = struct.pack("h" *len(wf16), *wf16) # 16-bit binaryization
    def save(self, data :list) -> None:
        '''
        ### Save the array received as an argument as a '.wav' file.
        - Pass a non-binary array
        - The number of channels, frame rate, and maximum normalization value should be set in advance using the 'set_' method.
        - The save location can be changed using the 'set_path()' method
        '''
        self.to_bin(data)
        # File output
        with wave.Wave_write(self.path) as f:
            # param = (nchannels, sampwidth, framerate, nframes, comptype, compname)
            param = (1, 2, self.framerate, len(self.bin_wf),'NONE','not compressed')
            f.setparams(param)
            f.writeframes(self.bin_wf)
    def save_w_date(self, data :list) -> None:
        '''
        ### Saves a file with the current date and time as the file name.
        - The file name is the ISO format ':' and '. in the ISO format with '_'.
        - For example, '2021-11-13T14_01_39_244906.wav'.
        '''
        now = datetime.datetime.now()
        dat = now.strftime('%Y-%m-%d') + 'T' + now.strftime('%H_%M_%S_%f')
        self.set_path(self.save_dir, dat, self.ext)
        self.save(data)

def main():
    # Waveform generation
    sec = 1 
    note_hz = 440
    sample_hz = 44100   # sampling frequency
    t = np.arange(0, sample_hz * sec)   # Allocate an array of time
    wf = np.sin(2 * np.pi * note_hz * t/sample_hz)

    wavesave = WavSave()
    wavesave.set_wav_param(1,2,44100)
    wavesave.set_norm(1)
    wavesave.save_w_date(wf)

if __name__ == '__main__':
    main()