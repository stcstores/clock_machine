import busio
from board import SCL, SDA
from oled_text import BigLine, OledText, SmallLine


class Screen:
    i2c = busio.I2C(SCL, SDA)

    def __init__(self):
        self.oled = OledText(self.i2c, 128, 32)
        self.oled.layout = {
            1: BigLine(0, 0, size=15, font="FreeSans.ttf"),
            2: SmallLine(0, 15, size=15, font="FreeSans.ttf"),
            # 3: BigLine(0, 20, size=10, font="FreeSans.ttf"),
        }

    def write(self, line_1="", line_2=""):
        self.oled.text(line_1, 1)
        self.oled.text(line_2, 2)
