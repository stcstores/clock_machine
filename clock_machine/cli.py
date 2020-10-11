import click
import RPi.GPIO as GPIO

from .clock_reader import ClockReader


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
