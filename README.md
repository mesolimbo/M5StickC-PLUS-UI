# M5StickC-PLUS Graphics Library

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/gMZkxidlqgk/0.jpg)](https://www.youtube.com/watch?v=gMZkxidlqgk)

A complete MicroPython graphics library for the M5StickC-PLUS device featuring efficient framebuffer management, BMP image loading, and comprehensive drawing primitives with proper color handling.

## Features

- **ST7789 Display Driver**: Native support for 135×240 pixel display with proper offset correction
- **Framebuffer Management**: Flicker-free rendering with double-buffering
- **Drawing Primitives**: Lines, rectangles, circles, pixels, and text
- **BMP Image Loading**: Memory-efficient 24-bit BMP decoder (8-bit supported as well)
- **Color Management**: RGB565 with blending and manipulation utilities
- **Memory Optimized**: ~64KB framebuffer, designed for ESP32 constraints

## Quick Start

```python
from m5graphics import M5Graphics, RED, GREEN, BLUE, WHITE

# Initialize graphics
graphics = M5Graphics()
graphics.init_display()

# Draw something
graphics.clear()
graphics.text("Hello M5!", 10, 10, WHITE)
graphics.rect(10, 30, 50, 30, RED)
graphics.circle(60, 60, 20, GREEN, fill=True)
graphics.show()
```

## Installation

1. **Install dependencies:**
   ```bash
   pipenv install
   ```

2. **Deploy to M5StickC-PLUS:**
   ```bash
   pipenv shell
   python deploy.py
   ```

3. **Run example:**
   ```bash
   pipenv run ampy -p COM4 run example.py
   ```
   
   **Or reset the device** - `boot.py` will auto-run the example on startup!

## Library Files

- `bmp_loader.py` - BMP image loading functionality
- `boot.py` - Auto-run example on device startup
- `example.py` - Usage demonstration with BMP loading test
- `m5_logo.bmp` - 135×240 M5 logo test image
- `m5graphics.py` - Main graphics library
- `small_test.bmp` - 64×64 test image (colorful quadrants)
- `st7789.py` - ST7789 display driver with M5StickC-PLUS optimizations
- `test_pattern.bmp` - 135×240 TV test pattern (classic Indian Head style)

## API Reference

### Basic Usage
```python
graphics = M5Graphics()
graphics.init_display()           # Initialize display
graphics.clear(color)             # Clear screen
graphics.show()                   # Update display
```

### Drawing
```python
graphics.pixel(x, y, color)                        # Single pixel
graphics.line(x0, y0, x1, y1, color)              # Line
graphics.rect(x, y, w, h, color, fill=False)      # Rectangle
graphics.circle(x, y, radius, color, fill=False)  # Circle
graphics.text(string, x, y, color, bg_color=None) # Text (8x8 font)
```

### Images
```python
graphics.load_bmp(filename, x=0, y=0)  # Load 24-bit BMP image
graphics.get_bmp_info(filename)        # Get image info
```

### Colors
```python
# Predefined colors
BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA

# Custom colors
rgb565(r, g, b)                    # Convert RGB to RGB565
blend_colors(color1, color2, alpha) # Blend colors
```

## BMP Images

For best results with BMP images:
- **Format**: 24-bit RGB, uncompressed
- **Size**: 135×240 pixels or smaller
- **Tools**: Any graphics editor (GIMP, Photoshop, etc.)

## Hardware

- **Device**: M5StickC-PLUS 
- **Display**: 135×240 ST7789 TFT
- **Firmware**: MicroPython v1.26.0 or later
- **Memory**: ~67KB total usage (64KB framebuffer + 3KB library)

## Deployment

### Windows (COM4)
```bash
# Deploy all files
pipenv run ampy -p COM4 put m5graphics.py
pipenv run ampy -p COM4 put st7789.py
pipenv run ampy -p COM4 put bmp_loader.py
pipenv run ampy -p COM4 put example.py

# Run example
pipenv run ampy -p COM4 run example.py
```

### Automated Deployment
```bash
python scripts/deploy.py  # Uses settings in deploy.py
```

## Performance

- **Display Update**: ~25ms full screen refresh
- **BMP Loading**: 1-3 seconds (depends on image size)
- **Memory Usage**: 64KB framebuffer + 3KB library code
- **Drawing**: Hardware-accelerated primitives via framebuf

## Technical Details

- **Display Offset**: Automatically corrected (52, 40) for proper centering
- **Color Format**: RGB565 (16-bit, 65k colors) with byte swapping for M5StickC-PLUS
- **SPI Settings**: 27MHz, polarity=0, phase=0 (Arduino-compatible)
- **Power Management**: Automatic AXP192 initialization
- **Memory Usage**: 64KB framebuffer + ~3KB library code

## Example Output

The example demonstrates:
1. Basic shapes (rectangles, circles, lines)
2. Text rendering with custom colors
3. Color gradients
4. Simple animation
5. BMP image loading (small test image and full-size logo)
6. Final "GRAPHICS LIBRARY READY!" confirmation

## Troubleshooting

**Display not working:**
- Ensure M5StickC-PLUS is powered on
- Check MicroPython firmware is installed
- Verify COM port in deployment commands

**Memory errors:**
- Call `gc.collect()` periodically
- Use smaller images or process in chunks

**Import errors:**
- Ensure all library files are deployed to device
- Check file names match exactly

## License

Created for M5StickC-PLUS development and educational use.