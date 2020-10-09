import subprocess

import click
import RPi.GPIO as GPIO

from .clock_reader import ClockReader


def get_ip_address():
    cmd = "hostname -I | cut -d' ' -f1"
    return subprocess.check_output(cmd, shell=True).decode("utf-8")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("server")
def clock_machine(server):
    clock_reader = ClockReader(server)
    ip_address = get_ip_address()
    try:
        while True:
            clock_reader.screen_write("Ready...", '', '', ip_address)
            try:
                response = clock_reader.read()
            except Exception as e:
                clock_reader.error(e)
            else:
                clock_reader.clock_success(response)
    finally:
        GPIO.cleanup()


@cli.command()
@click.argument("server")
def make_card(server):
    clock_reader = ClockReader(server)
    clock_reader.make_card()
