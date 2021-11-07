from gpiozero import TonalBuzzer
import time

BUZZER_PIN = 16 # slot D16
PIPI = 2

buzz = TonalBuzzer(BUZZER_PIN,octaves=3)

def pipi():
    for _ in range(PIPI):
        buzz.play("G7")
        time.sleep(0.04)
        buzz.stop()
        time.sleep(0.03)

def main():
    pipi()

if __name__ == "__main__":
    main()