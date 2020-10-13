import time

import click
import RPi.GPIO as GPIO

from .clock_reader import ClockReader
from .rfid import RFID
from .screen import Screen


@click.group()
def cli():
    pass


@cli.command()
@click.argument("server")
def clock_machine(server):
    clock_reader = ClockReader(server)
    clock_reader.screen_write(line_1="Initialising...")
    try:
        while True:
            try:
                response = clock_reader.read()
            except Exception as e:
                clock_reader.error(e)
            else:
                clock_reader.clock_success(response)
    finally:
        clock_reader.screen.blank()
        clock_reader.screen.write()
        GPIO.cleanup()


@cli.command()
@click.argument("server")
def make_card(server):
    clock_reader = ClockReader(server)
    clock_reader.make_card()


@cli.command()
def clear_screen():
    screen = Screen()
    screen.blank()


@cli.command()
def read():
    screen = Screen()
    rfid = RFID()
    line_length = 19
    try:
        while True:
            try:
                card_id, data = rfid.read()
            except Exception as e:
                click.echo(e)
                screen.write(e)
            else:
                click.echo(f"{card_id}: {data}")
                lines = [card_id]
                lines.extend(
                    [
                        data[i : i + line_length]
                        for i in range(0, len(data), line_length)
                    ]
                )
                screen.write(*lines)
                time.sleep(1)
    finally:
        screen.blank()
        screen.write()
        GPIO.cleanup()
