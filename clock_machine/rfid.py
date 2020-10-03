from mfrc522 import SimpleMFRC522


class RFID:
    reader = SimpleMFRC522()

    def read(self):
        return self.reader.read()

    def write(self, text):
        self.reader.write(text)
