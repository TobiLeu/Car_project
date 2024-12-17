from machine import Pin
from time import sleep

class LCD1602:
    def __init__(self, rs, e, d4, d5, d6, d7):
        self.rs = Pin(rs, Pin.OUT)
        self.e = Pin(e, Pin.OUT)
        self.data_pins = [Pin(d4, Pin.OUT), Pin(d5, Pin.OUT), Pin(d6, Pin.OUT), Pin(d7, Pin.OUT)]
        self._init_lcd()

    def _pulse_enable(self):
        self.e.off()
        sleep(0.000001)  # 1 µs
        self.e.on()
        sleep(0.000001)  # 1 µs
        self.e.off()
        sleep(0.0001)  # 100 µs

    def _send_nibble(self, nibble):
        for i in range(4):
            self.data_pins[i].value((nibble >> i) & 0x01)
        self._pulse_enable()

    def _send_byte(self, byte, mode):
        self.rs.value(mode)  # RS = 0 für Befehl, RS = 1 für Daten
        self._send_nibble(byte >> 4)  # Höhere 4 Bits
        self._send_nibble(byte & 0x0F)  # Niedrigere 4 Bits

    def _init_lcd(self):
        sleep(0.05)  # Warten auf Einschalten
        self._send_nibble(0x03)
        sleep(0.005)
        self._send_nibble(0x03)
        sleep(0.00015)
        self._send_nibble(0x03)
        self._send_nibble(0x02)  # 4-Bit-Modus
        self._send_byte(0x28, 0)  # 2 Zeilen, 5x8 Punktmatrix
        self._send_byte(0x0C, 0)  # Display ein, Cursor aus
        self._send_byte(0x01, 0)  # Display löschen
        sleep(0.002)
        self._send_byte(0x06, 0)  # Automatischer Cursor-Vorwärtsmodus

    def clear(self):
        self._send_byte(0x01, 0)  # Display löschen
        sleep(0.002)

    def write(self, row, col, text):
        address = col + (0x40 if row else 0x00)
        self._send_byte(0x80 | address, 0)  # Setze Cursor
        for char in text:
            self._send_byte(ord(char), 1)