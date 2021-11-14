from collections import deque
from scipy import interpolate
import numpy as np
import pandas as pd

class ReSample():
    def __init__(self, resampling_rate = 44100, chunk_size = 4) -> None:
        self.resampling_rate = resampling_rate # Hz
        self.chunk_size = chunk_size # sec
    def resample(self, data :list) -> list:
        dq = deque(data)
        # Find number of chunks
        start_time = dq[0][0]
        last_time = dq[len(dq)-1][0]
        total_time = last_time - start_time
        chunk_count = divmod(total_time, self.chunk_size)
        if chunk_count[1] == 0:
            chunk_count = chunk_count[0]
        else:
            chunk_count = int(chunk_count[0]) + 1
        for i in range(chunk_count):
            if i == chunk_count-1: # Zero-filling of the last chunk
                last_chunk_head = dq[0][0]
                while last_chunk_head + self.chunk_size >= dq[len(dq)-1][0]:
                    last_time = dq[len(dq)-1][0]
                    fill_zero = [last_time+1, 0]
                    dq.append(fill_zero)
            # Get seconds of data as a single chunks
            start_row = dq[0][0]
            chunk = []
            while start_row + self.chunk_size >= dq[0][0]:
                chunk.append(dq.popleft())
            # resample
            df = pd.DataFrame(chunk)
            df = df.set_axis(['time', 'pressure'], axis=1)
            df = df.set_index('time')
            f = interpolate.interp1d(df.index, df.pressure, kind='cubic')
            re_x = np.arange(df.index.min(), df.index.max(), 1/self.resampling_rate)
            re_y = f(re_x)
            if i == 0:    # Store the first chunk
                first_a = np.stack([re_x, re_y],1)
                store_a = first_a
            elif i == chunk_count-1:  # Store the last chunk
                last_a = np.stack([re_x, re_y],1)
                store_a = np.concatenate([store_a, last_a])
            else:   # intermediate lump
                intermediate_a = np.stack([re_x, re_y],1)
                store_a = np.concatenate([store_a, intermediate_a])
        store_a = np.delete(store_a, slice(int(total_time*self.resampling_rate), None) , 0)
        return store_a
def main():
    pass

if __name__ == '__main__':
    main()