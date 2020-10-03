import click
import RPi.GPIO as GPIO

from .clock_reader import ClockReader


@click.group()
def cli():
    pass


@cli.command()
def clock_machine():
    clock_reader = ClockReader()
    click.echo("Ready...")
    try:
        while True:
            try:
                response = clock_reader.read()
            except Exception as e:
                clock_reader.error(e)
            else:
                clock_reader.clock_success(response)
    finally:
        GPIO.cleanup()


@cli.command()
def make_card():
    clock_reader = ClockReader()
    clock_reader.make_card()
