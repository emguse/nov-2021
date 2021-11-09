import RPi.GPIO as gpio
import time

BUZZER_PIN = 16 # slot D16
FREQ = 3135
PIPIPI = 2

def main():
    gpio.setmode(gpio.BCM)
    gpio.setup(BUZZER_PIN,gpio.OUT)
    pi = gpio.PWM(16, FREQ)
    pi.start(0)
    for _ in range(PIPIPI):
        pi.ChangeDutyCycle(50)
        time.sleep(0.04)
        pi.ChangeDutyCycle(0)
        time.sleep(0.03)
    pi.stop()
    gpio.cleanup()

if __name__ == "__main__":
    main()