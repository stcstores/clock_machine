import subprocess
import time

import busio
from board import SCL, SDA
from oled_text import BigLine, OledText, SmallLine


class Screen:
    i2c = busio.I2C(SCL, SDA)

    def __init__(self):
        self.oled = OledText(self.i2c, 128, 64)
        self.oled.layout = {
            1: BigLine(0, 0, size=15, font="FreeSans.ttf"),
            2: BigLine(0, 15, size=15, font="FreeSans.ttf"),
            3: BigLine(0, 30, size=15, font="FreeSans.ttf"),
            4: SmallLine(0, 50, size=10, font="FreeSans.ttf"),
        }
        self.oled.auto_show = False
        self.blank()

    def write(self, line_1=None, line_2=None, line_3=None, line_4=None):
        if line_1 is not None:
            self.line_1 = line_1
        if line_2 is not None:
            self.line_2 = line_2
        if line_3 is not None:
            self.line_3 = line_3
        self.oled.text(self.line_1, 1)
        self.oled.text(self.line_2, 2)
        self.oled.text(self.line_3, 3)
        self.oled.text(self.get_ip_address(), 4)
        self.oled.show()

    def blank(self):
        self.line_1 = ""
        self.line_2 = ""
        self.line_3 = ""
        self.line_4 = ""
        self.write("", "", "", "")

    def get_ip_address(self):
        cmd = "hostname -I | cut -d' ' -f1"
        ip_address = ""
        for i in range(100):
            ip_address = (
                subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            )
            if ip_address:
                return ip_address
            time.sleep(0.25)
        return "No IP address found"
