from collections import deque

class MovingAverage():
    def __init__(self, length:int) -> None:
        self.length = abs(length)
        if self.length == 0:
            self.length = 1
        self.dq = deque([],maxlen=self.length)
        pass
    def simple_moving_average(self, new_value) -> float: 
        self.dq.append(new_value)
        sma = sum(self.dq) / self.length
        return sma
    def weighted_moving_average(self, new_value) -> float:
        a = []
        b = []
        self.dq.append(new_value)
        for i in range(len(self.dq)):
            a.append(self.dq[i]*(i+1))
            b.append(i + 1)
        wma = sum(a) / sum(b)
        return wma

def main():
    ma = MovingAverage(5)
    l = [1,2,3,4,5,6,7,8,9,10]
    for i in l:
        print(ma.weighted_moving_average(i))

if __name__ == "__main__":
    main()