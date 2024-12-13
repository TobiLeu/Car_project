from machine import I2C, Pin
import time

class LCD1602:
    def __init__(self, i2c, address=0x27, rows=2, cols=16):
        self.i2c = i2c
        self.address = address
        self.rows = rows
        self.cols = cols
        self._init_lcd()

    def _send_command(self, cmd):
        self.i2c.writeto(self.address, b'\x80' + bytes([cmd]))
        time.sleep_ms(1)

    def _send_data(self, data):
        self.i2c.writeto(self.address, b'\x40' + bytes([data]))
        time.sleep_ms(1)

    def _init_lcd(self):
        self._send_command(0x38)  # Function set: 2 lines, 8-bit mode
        self._send_command(0x0C)  # Display on, cursor off
        self._send_command(0x01)  # Clear display
        time.sleep_ms(2)

    def clear(self):
        self._send_command(0x01)  # Clear display
        time.sleep_ms(2)

    def write(self, row, col, text):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError("Row or column out of range")
        pos = 0x80 | (col + 0x40 * row)
        self._send_command(pos)
        for char in text:
            self._send_data(ord(char))