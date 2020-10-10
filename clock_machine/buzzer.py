import time

import RPi.GPIO as GPIO


class Buzzer:
    pin_number = 21

    def __init__(self):
        GPIO.setup(self.pin_number, GPIO.OUT)
        self.pin = GPIO.PWM(self.pin_number, 100)

    def buzz(self, *frequencies):
        GPIO.output(self.pin_number, True)
        for frequency in frequencies:
            self.pin.ChangeFrequency(frequency)
            self.pin.start(90)
            time.sleep(0.25)
        self.buzz_stop()

    def buzz_read(self):
        GPIO.output(self.pin_number, True)
        self.pin.ChangeFrequency(700)
        self.pin.start(90)

    def buzz_stop(self):
        self.pin.stop()

    def buzz_in(self):
        self.buzz(700, 1000)

    def buzz_out(self):
        self.buzz(1000, 700)

    def buzz_err(self):
        self.buzz(500, 500)
