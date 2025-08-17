"""
Fixed ST7789 Display Driver for M5StickC-PLUS
Uses correct SPI settings and display offsets discovered through testing
"""

import time
from micropython import const

# ST7789 Commands
_SWRESET = const(0x01)
_SLPOUT = const(0x11)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_DISPON = const(0x29)
_INVON = const(0x21)
_NORON = const(0x13)

# M5StickC-PLUS display offsets (discovered through testing)
COL_OFFSET = const(52)
ROW_OFFSET = const(40)


class ST7789:
    """Fixed ST7789 TFT display driver for M5StickC-PLUS"""
    
    def __init__(self, spi, width, height, reset=None, dc=None, cs=None):
        self.spi = spi
        self.width = width
        self.height = height
        self.reset = reset
        self.dc = dc
        self.cs = cs
        
        # Configure pins
        if self.reset:
            self.reset.init(self.reset.OUT, value=1)
        if self.dc:
            self.dc.init(self.dc.OUT, value=0)
        if self.cs:
            self.cs.init(self.cs.OUT, value=1)
    
    def _write_cmd(self, cmd):
        """Write command to display"""
        if self.cs:
            self.cs.value(0)
        if self.dc:
            self.dc.value(0)  # Command mode
        self.spi.write(bytearray([cmd]))
        if self.cs:
            self.cs.value(1)
    
    def _write_data(self, data):
        """Write data to display"""
        if self.cs:
            self.cs.value(0)
        if self.dc:
            self.dc.value(1)  # Data mode
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        elif isinstance(data, (list, tuple)):
            self.spi.write(bytearray(data))
        else:
            self.spi.write(data)
        if self.cs:
            self.cs.value(1)
    
    def _write_cmd_data(self, cmd, data=None):
        """Write command followed by data"""
        self._write_cmd(cmd)
        if data is not None:
            if isinstance(data, (list, tuple)):
                for d in data:
                    self._write_data(d)
            else:
                self._write_data(data)
    
    def reset_display(self):
        """Hardware reset of the display"""
        if self.reset:
            self.reset.value(0)
            time.sleep_ms(20)
            self.reset.value(1)
            time.sleep_ms(120)
    
    def init(self):
        """Initialize the ST7789 display with correct M5StickC-PLUS settings"""
        self.reset_display()
        
        # Software reset
        self._write_cmd(_SWRESET)
        time.sleep_ms(150)
        
        # Sleep out
        self._write_cmd(_SLPOUT)
        time.sleep_ms(120)
        
        # Memory access control - normal orientation
        self._write_cmd_data(_MADCTL, 0x00)
        
        # Color mode - 16-bit RGB565
        self._write_cmd_data(_COLMOD, 0x05)
        
        # Inversion on (required for proper colors on M5StickC-PLUS)
        self._write_cmd(_INVON)
        
        # Normal display mode
        self._write_cmd(_NORON)
        time.sleep_ms(10)
        
        # Display on
        self._write_cmd(_DISPON)
        time.sleep_ms(120)
    
    def set_window(self, x0, y0, x1, y1):
        """Set the active drawing window with proper offsets"""
        # Apply M5StickC-PLUS offsets
        x0_offset = x0 + COL_OFFSET
        x1_offset = x1 + COL_OFFSET
        y0_offset = y0 + ROW_OFFSET
        y1_offset = y1 + ROW_OFFSET
        
        # Column address set
        self._write_cmd(_CASET)
        self._write_data(bytearray([
            (x0_offset >> 8) & 0xFF, x0_offset & 0xFF,
            (x1_offset >> 8) & 0xFF, x1_offset & 0xFF
        ]))
        
        # Row address set
        self._write_cmd(_RASET)
        self._write_data(bytearray([
            (y0_offset >> 8) & 0xFF, y0_offset & 0xFF,
            (y1_offset >> 8) & 0xFF, y1_offset & 0xFF
        ]))
        
        # Write to RAM
        self._write_cmd(_RAMWR)
    
    def blit_buffer(self, buffer, x, y, width, height):
        """Blit a buffer to the display at specified position"""
        x1 = x + width - 1
        y1 = y + height - 1
        
        self.set_window(x, y, x1, y1)
        self._write_data(buffer)
    
    def fill(self, color):
        """Fill entire display with a color"""
        # Convert 16-bit color to bytes (RGB565 format)
        color_bytes = bytearray([(color >> 8) & 0xFF, color & 0xFF])
        
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Write color data for entire screen efficiently
        self.cs.value(0)
        self.dc.value(1)
        
        for _ in range(self.width * self.height):
            self.spi.write(color_bytes)
            
        self.cs.value(1)
    
    def pixel(self, x, y, color):
        """Set a single pixel"""
        if 0 <= x < self.width and 0 <= y < self.height:
            color_bytes = bytearray([(color >> 8) & 0xFF, color & 0xFF])
            self.set_window(x, y, x, y)
            self._write_data(color_bytes)