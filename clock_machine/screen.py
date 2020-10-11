import busio
from board import SCL, SDA
from oled_text import BigLine, OledText, SmallLine


class Screen:
    i2c = busio.I2C(SCL, SDA)

    def __init__(self):
        self.oled = OledText(self.i2c, 128, 64)
        self.oled.layout = {
            1: BigLine(0, 0, size=15, font="FreeSans.ttf"),
            2: SmallLine(0, 15, size=15, font="FreeSans.ttf"),
            3: SmallLine(0, 20, size=10, font="FreeSans.ttf"),
            4: SmallLine(0, 20, size=10, font="FreeSans.ttf"),
        }
        self.oled.auto_show = False
        self.blank()

    def write(self, line_1=None, line_2=None, line_3=None, line_4=None):
        if line_1:
            self.line_1 = line_1
        if line_2:
            self.line_2 = line_2
        if line_3:
            self.line_3 = line_3
        if line_4:
            self.line_4 = line_4
        self.oled.text(self.line_1, 1)
        self.oled.text(self.line_2, 2)
        self.oled.text(self.line_3, 3)
        self.oled.text(self.line_4, 4)
        self.oled.show()

    def blank(self):
        self.line_1 = ""
        self.line_2 = ""
        self.line_3 = ""
        self.line_4 = ""
        self.write()
