import RPi.GPIO as gpio
import time

BUZZER_PIN = 16 # slot D16
FREQ = 3135
PIPIPI = 2

class PiPi():
    def __init__(self) -> None:
        gpio.setmode(gpio.BCM)
        gpio.setup(BUZZER_PIN,gpio.OUT)
        self.pi = gpio.PWM(16, FREQ)
    def pipi(self):
        self.pi.start(0)
        for _ in range(PIPIPI):
            self.pi.ChangeDutyCycle(50)
            time.sleep(0.04)
            self.pi.ChangeDutyCycle(0)
            time.sleep(0.03)
        self.pi.stop()
        gpio.cleanup(BUZZER_PIN)

def main():
    pipi = PiPi()
    pipi.pipi()

if __name__ == "__main__":
    main()