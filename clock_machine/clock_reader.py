import json
import time

import click
import requests

from .buzzer import Buzzer
from .rfid import RFID


class ClockReader:
    buzzer = Buzzer()

    CLOCK_URL = "http://127.0.0.1:8000/clock_time"
    MAKE_CARD_URL = "http://127.0.0.1:8000/make_card"
    reader = RFID()

    IN = "in"
    OUT = "out"

    def error(self, e):
        click.echo(f"Error: {e}")
        self.buzzer.buzz_err()
        time.sleep(0.5)

    def read(self):
        card_id, text = self.reader.read()
        click.echo(card_id)
        click.echo(text)
        card_data = json.loads(text)
        self.buzzer.buzz_read()
        return self.clock_request(card_id, card_data)

    def clock_success(self, response):
        response_data = response.json()
        if response_data["direction"] == self.IN:
            self.signal_clock_in(response_data["employee"], response_data["time"])
        else:
            self.signal_clock_out(response_data["employee"], response_data["time"])
        time.sleep(1)

    def signal_clock_in(self, name, clock_time):
        click.echo(f"{name} clocked IN at {clock_time}")
        self.buzzer.buzz_in()

    def signal_clock_out(self, name, clock_time):
        click.echo(f"{name} clocked OUT at {clock_time}")
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
        click.echo("Scan RFID card...")
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
                click.echo("Card write error, please try again.")
                self.buzzer.buzz_err()
            else:
                click.echo(f"{written_text} written to card")
                click.echo("Card write sucessful")
                self.buzzer.buzz_in()
        else:
            click.echo(f"Request returned {response.text}")
            self.buzzer.buzz_err()
