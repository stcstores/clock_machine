import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import json

reader = SimpleMFRC522()
try:
    data = {"name": "Jake Richardson", "id": "186115"}
    json = json.dumps(data, indent=4, sort_keys=True)
    reader.write(json)
    print("Written")
finally:
    GPIO.cleanup()
