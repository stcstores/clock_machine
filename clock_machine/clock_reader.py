import json
import time

import click
import requests

from .screen import Screen
from .buzzer import Buzzer
from .rfid import RFID


class ClockReader:
    buzzer = Buzzer()
    screen = Screen()

    reader = RFID()

    IN = "in"
    OUT = "out"

    def __init__(self, server):
        self.CLOCK_URL = f"http://{server}/clock_time"
        self.MAKE_CARD_URL = f"http://{server}/make_card"

    def error(self, e):
        self.screen_write("Error: ", str(e))
        click.echo(str(e))
        self.buzzer.buzz_err()
        time.sleep(3)

    def read(self):
        card_id, text = self.reader.read()
        click.echo(card_id)
        click.echo(text)
        self.screen_write("Reading...")
        card_data = json.loads(text)
        self.screen_write(card_data["name"], "Wait...")
        self.buzzer.buzz_read()
        return self.clock_request(card_id, card_data)

    def clock_success(self, response):
        response_data = response.json()
        if response_data["direction"] == self.IN:
            self.signal_clock_in(response_data["employee"], response_data["time"])
        else:
            self.signal_clock_out(response_data["employee"], response_data["time"])
        time.sleep(3)

    def signal_clock_in(self, name, clock_time):
        self.screen_write(name, "Clocked IN")
        self.buzzer.buzz_in()

    def signal_clock_out(self, name, clock_time):
        self.screen_write(name, "Clocked OUT")
        self.buzzer.buzz_out()

    def parse_card_read(self, card_id, card_data):
        name = card_data["name"]
        return {"card_id": card_id, "name": name}

    def clock_request(self, card_id, card_data):
        request_data = self.parse_card_read(card_id, card_data)
        response = requests.post(self.CLOCK_URL, request_data)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Request returned {response.text}")

    def make_card(self):
        employee_id = click.prompt("Employee ID", type=int)
        self.screen_write("Scan RFID card...")
        card_id, text = self.reader.read()
        self.buzzer.buzz_read()
        request_data = {"employee_id": employee_id, "card_id": card_id}
        response = requests.post(self.MAKE_CARD_URL, request_data)
        if response.status_code == 200:
            name = response.json()["name"]
            card_text = json.dumps({"name": name})
            self.reader.write(card_text)
            card_id, written_text = self.reader.read()
            if written_text != written_text:
                self.screen_write("Card write error, please try again.")
                self.buzzer.buzz_err()
            else:
                self.screen_write(f"{written_text} written to card")
                self.screen_write("Card write sucessful")
                self.buzzer.buzz_in()
        else:
            self.screen_write(f"Request returned {response.text}")
            self.buzzer.buzz_err()

    def screen_write(self, line_1="", line_2=""):
        click.echo(f"{line_1}\t{line_2}")
        self.screen.write(f"{line_1}\t{line_2}")
        self.screen.write(line_1, line_2)
