from collections import deque

class MovingAverage():
    def __init__(self, lenghs:int) -> None:
        self.lenghs = lenghs
        self.dq = deque([],maxlen=lenghs)
        pass
    def move_average(self, new_value) -> float: 
        self.dq.append(new_value)
        m_ave = sum(self.dq) / self.lenghs
        return m_ave

def main():
    m_ave = MovingAverage(3)
    l = [1,2,3,4,5,6,7,8,9,10]
    for i in l:
        print(m_ave.move_average(i))

if __name__ == "__main__":
    main()