import numpy as np
import matplotlib.pyplot as plt
import struct
import wave

# Waveform generation
sec = 1 
note_hz = 440
sample_hz = 44100   # sampling frequency
t = np.arange(0, sample_hz * sec)   # Allocate an array of time
wv = np.sin(2 * np.pi * note_hz * t/sample_hz)

# Binary digitization
# int16 is in the range of -32768~32767
# Divide 32767 by the maximum value of the waveform data
max_num = 32767.0 / max(wv)
# Convert to 16-bit signed integer
# Take the ratio of the value of one sample to the maximum value of 
# the entire sample and multiply by 32767
wv16 = [int(x * max_num) for x in wv] 
# h:2byte (16bit) integer format (short in C)
bi_wv = struct.pack("h" *len(wv16), *wv16) 

# File output
with wave.Wave_write("sin_wave.wav") as f:
    param = (1, 2, sample_hz, len(bi_wv),'NONE','not compressed')
    f.setparams(param)
    f.writeframes(bi_wv)

# plot
plt.plot(t,wv)
plt.xlim(0,500)
plt.title("wav")
plt.xlabel("sample")
plt.ylabel("y")
plt.tight_layout()
plt.savefig("sin.png")