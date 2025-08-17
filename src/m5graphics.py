"""
Working M5StickC-PLUS Graphics Library
Fixed version with correct SPI settings and display offsets
"""

import machine
import framebuf
import gc
import time
from micropython import const

# Display dimensions
DISPLAY_WIDTH = const(135)
DISPLAY_HEIGHT = const(240)
BYTES_PER_PIXEL = const(2)  # RGB565
BUFFER_SIZE = const(DISPLAY_WIDTH * DISPLAY_HEIGHT * BYTES_PER_PIXEL)

# Color constants (RGB565 with byte swap)
BLACK = const(0x0000)
WHITE = const(0xFFFF)
RED = const(0x00F8)      # Byte-swapped from 0xF800
GREEN = const(0xE007)    # Byte-swapped from 0x07E0
BLUE = const(0x1F00)     # Byte-swapped from 0x001F
YELLOW = const(0xE0FF)   # Byte-swapped from 0xFFE0
CYAN = const(0xFF07)     # Byte-swapped from 0x07FF
MAGENTA = const(0x1FF8)  # Byte-swapped from 0xF81F


def rgb565(r, g, b):
    """Convert 8-bit RGB values to 16-bit RGB565 color with byte swap"""
    color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return ((color & 0xFF) << 8) | ((color >> 8) & 0xFF)


def rgb565_to_rgb(color):
    """Convert RGB565 color back to 8-bit RGB tuple"""
    r = (color >> 8) & 0xF8
    g = (color >> 3) & 0xFC  
    b = (color << 3) & 0xF8
    return (r, g, b)


def blend_colors(color1, color2, alpha):
    """Blend two RGB565 colors with alpha (0.0 to 1.0)"""
    if alpha <= 0:
        return color2
    if alpha >= 1:
        return color1
    
    # Convert to RGB
    r1, g1, b1 = rgb565_to_rgb(color1)
    r2, g2, b2 = rgb565_to_rgb(color2)
    
    # Blend
    r = int(r1 * alpha + r2 * (1 - alpha))
    g = int(g1 * alpha + g2 * (1 - alpha))
    b = int(b1 * alpha + b2 * (1 - alpha))
    
    return rgb565(r, g, b)


def darken_color(color, factor):
    """Darken a color by a factor (0.0 to 1.0)"""
    r, g, b = rgb565_to_rgb(color)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return rgb565(r, g, b)


def lighten_color(color, factor):
    """Lighten a color by a factor (0.0 to 1.0)"""
    r, g, b = rgb565_to_rgb(color)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return rgb565(r, g, b)


class M5Graphics:
    """Working M5StickC-PLUS graphics library"""
    
    def __init__(self):
        self.display = None
        self.framebuffer = None
        self.buffer = None
        self._initialized = False
        
    def _init_power_management(self):
        """Initialize M5StickC-PLUS power management"""
        try:
            i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
            i2c.writeto_mem(0x34, 0x12, bytes([0x4D]))  # Enable LDO2&3
            time.sleep_ms(50)
            return True
        except:
            return False
    
    def init_display(self, spi_baudrate=27_000_000):
        """Initialize display with correct settings"""
        try:
            # Initialize power management
            self._init_power_management()
            
            # Setup SPI with correct settings (polarity=0, phase=0 like Arduino)
            spi = machine.SPI(1, baudrate=spi_baudrate, polarity=0, phase=0,
                             sck=machine.Pin(13), mosi=machine.Pin(15))
            
            # Initialize display with fixed driver
            from st7789 import ST7789
            self.display = ST7789(spi, 
                                DISPLAY_WIDTH, 
                                DISPLAY_HEIGHT,
                                reset=machine.Pin(18, machine.Pin.OUT),
                                dc=machine.Pin(23, machine.Pin.OUT),
                                cs=machine.Pin(5, machine.Pin.OUT))
            
            self.display.init()
            
            # Allocate framebuffer
            self.buffer = bytearray(BUFFER_SIZE)
            self.framebuffer = framebuf.FrameBuffer(self.buffer, 
                                                  DISPLAY_WIDTH, 
                                                  DISPLAY_HEIGHT, 
                                                  framebuf.RGB565)
            
            self._initialized = True
            print("Display initialized successfully")
            return True
            
        except Exception as e:
            print(f"Display initialization failed: {e}")
            return False
    
    def is_initialized(self):
        """Check if display is properly initialized"""
        return self._initialized
    
    def clear(self, color=BLACK):
        """Clear the framebuffer with specified color"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        self.framebuffer.fill(color)
    
    def show(self):
        """Display the current framebuffer on screen"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        self.display.blit_buffer(self.buffer, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    def pixel(self, x, y, color):
        """Set a pixel at (x, y) to specified color"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        if 0 <= x < DISPLAY_WIDTH and 0 <= y < DISPLAY_HEIGHT:
            self.framebuffer.pixel(x, y, color)
    
    def get_pixel(self, x, y):
        """Get the color of a pixel at (x, y)"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        if 0 <= x < DISPLAY_WIDTH and 0 <= y < DISPLAY_HEIGHT:
            return self.framebuffer.pixel(x, y)
        return 0
    
    # Drawing primitives
    def line(self, x0, y0, x1, y1, color):
        """Draw a line from (x0, y0) to (x1, y1)"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        self.framebuffer.line(x0, y0, x1, y1, color)
    
    def hline(self, x, y, length, color):
        """Draw a horizontal line"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        self.framebuffer.hline(x, y, length, color)
    
    def vline(self, x, y, length, color):
        """Draw a vertical line"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        self.framebuffer.vline(x, y, length, color)
    
    def rect(self, x, y, width, height, color, fill=False):
        """Draw a rectangle"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        if fill:
            self.framebuffer.fill_rect(x, y, width, height, color)
        else:
            self.framebuffer.rect(x, y, width, height, color)
    
    def circle(self, x, y, radius, color, fill=False):
        """Draw a circle"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        
        if radius <= 0:
            return
            
        # Use ellipse if available in framebuf
        if hasattr(self.framebuffer, 'ellipse'):
            self.framebuffer.ellipse(x, y, radius, radius, color, fill)
        else:
            # Fallback: implement midpoint circle algorithm
            self._draw_circle_midpoint(x, y, radius, color, fill)
    
    def _draw_circle_midpoint(self, cx, cy, radius, color, fill=False):
        """Midpoint circle algorithm implementation"""
        x = radius
        y = 0
        err = 0
        
        while x >= y:
            if fill:
                self.hline(cx - x, cy + y, 2 * x + 1, color)
                self.hline(cx - x, cy - y, 2 * x + 1, color)
                self.hline(cx - y, cy + x, 2 * y + 1, color)
                self.hline(cx - y, cy - x, 2 * y + 1, color)
            else:
                self.pixel(cx + x, cy + y, color)
                self.pixel(cx + y, cy + x, color)
                self.pixel(cx - y, cy + x, color)
                self.pixel(cx - x, cy + y, color)
                self.pixel(cx - x, cy - y, color)
                self.pixel(cx - y, cy - x, color)
                self.pixel(cx + y, cy - x, color)
                self.pixel(cx + x, cy - y, color)
            
            if err <= 0:
                y += 1
                err += 2 * y + 1
            
            if err > 0:
                x -= 1
                err -= 2 * x + 1
    
    def text(self, string, x, y, color, bg_color=None):
        """Draw text using the built-in 8x8 font"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        
        if bg_color is not None:
            # Draw background rectangle for text
            text_width = len(string) * 8
            text_height = 8
            self.rect(x, y, text_width, text_height, bg_color, fill=True)
        
        self.framebuffer.text(string, x, y, color)
    
    # Image loading functionality
    def load_bmp(self, filename, x=0, y=0, max_width=None, max_height=None):
        """Load a BMP image file and display it on the framebuffer"""
        if not self._initialized:
            raise RuntimeError("Display not initialized")
        
        try:
            from bmp_loader import BMPLoader
            loader = BMPLoader()
            
            # Set default max dimensions to screen size
            if max_width is None:
                max_width = DISPLAY_WIDTH - x
            if max_height is None:
                max_height = DISPLAY_HEIGHT - y
            
            success = loader.load_to_framebuffer(
                filename, 
                self.framebuffer, 
                x, y, 
                max_width, 
                max_height
            )
            
            if success:
                gc.collect()  # Clean up after image loading
                return True
            else:
                print(f"Failed to load BMP: {filename}")
                return False
                
        except ImportError:
            print("BMP loader module not found")
            return False
        except Exception as e:
            print(f"Error loading BMP {filename}: {e}")
            return False
    
    def get_bmp_info(self, filename):
        """Get information about a BMP file without loading it"""
        try:
            from bmp_loader import BMPLoader
            loader = BMPLoader()
            return loader.get_image_info(filename)
        except ImportError:
            print("BMP loader module not found")
            return None
        except Exception as e:
            print(f"Error reading BMP info {filename}: {e}")
            return None