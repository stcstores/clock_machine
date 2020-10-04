import click
import RPi.GPIO as GPIO

from .clock_reader import ClockReader
import subprocess


def get_ip_address():
    cmd = "hostname -I | cut -d' ' -f1"
    return subprocess.check_output(cmd, shell=True).decode("utf-8")


@click.group()
def cli():
    pass


@cli.command()
def clock_machine():
    clock_reader = ClockReader()
    ip_address = get_ip_address()
    try:
        while True:
            clock_reader.screen_write("Ready...", ip_address)
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
