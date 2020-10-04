import threading
import time

import RPi.GPIO as GPIO


class Buzzer:
    pin_number = 22

    def __init__(self):
        GPIO.setup(self.pin_number, GPIO.OUT)
        self.pin = GPIO.PWM(self.pin_number, 100)

    def buzz(self, *frequencies):
        thread = threading.Thread(target=self.run_buzzer, args=(frequencies))
        thread.start()

    def run_buzzer(self, *frequencies):
        GPIO.output(self.pin_number, True)
        for frequency in frequencies:
            self.pin.ChangeFrequency(frequency)
            self.pin.start(90)
            time.sleep(0.25)
            self.pin.stop()

    def buzz_read(self):
        self.buzz(700)

    def buzz_in(self):
        self.buzz(700, 1000)

    def buzz_out(self):
        self.buzz(1000, 700)

    def buzz_err(self):
        self.buzz(500, 500)
