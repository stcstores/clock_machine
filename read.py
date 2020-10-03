import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import random
from datetime import datetime
import json
from pathlib import Path

reader = SimpleMFRC522()

IN = "in"
OUT = "out"


class Buzzer:
    pin_number = 15

    def __init__(self):
        GPIO.setup(self.pin_number, GPIO.OUT)
        self.pin = GPIO.PWM(self.pin_number, 100)

    def buzz(self, *frequencies):
        GPIO.output(self.pin_number, True)
        for frequency in frequencies:
            self.pin.ChangeFrequency(frequency)
            self.pin.start(90)
            time.sleep(0.25)
            self.pin.stop()

    def buzz_in(self):
        self.buzz(700, 1000)

    def buzz_out(self):
        self.buzz(1000, 700)

    def buzz_err(self):
        self.buzz(500, 500)

file_path = Path("../times.json")

def add_time(name):
    clock_time = datetime.now()
    try:
        current_time = times[name][-1]
    except (IndexError, KeyError):
        times[name] = [[str(clock_time), None]]
        direction = IN
    else:
        if current_time[1] is None:
            current_time[1] = str(clock_time)
            direction = OUT
        else:
            times[name].append([str(clock_time), None])
            direction = IN
    with open(file_path, "w") as f:
        json.dump(times, f, sort_keys=True, indent=4)
    return direction, clock_time


buzzer = Buzzer()


with open(file_path, "r") as f:
    times = json.load(f)

try:
    while True:
        try:
            rfid_id, text = reader.read()
            if random.randint(0, 50) > 40:
                raise Exception("Test Error")
        except Exception as e:
            print(f"Error: {e}")
            buzzer.buzz_err()
            time.sleep(0.5)
        else:
            print(rfid_id)
            print(text)
            try:
                data = json.loads(text)
            except Exception as e:
                print(f"Error: {e}")
            else:
                name = data["name"]
                direction, clock_time = add_time(name)
                if direction == IN:
                    print(f"{name} clocked IN at {clock_time}")
                    buzzer.buzz_in()
                else:
                    print(f"{name} clocked OUT at {clock_time}")
                    buzzer.buzz_out()
            time.sleep(0.5)
finally:
    GPIO.cleanup()
