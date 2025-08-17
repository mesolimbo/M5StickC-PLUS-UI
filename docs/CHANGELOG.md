# Changelog

## [1.0.0] - 2025-08-17

### Added
- Complete M5StickC-PLUS graphics library implementation
- ST7789 display driver with proper offset correction (52, 40)
- Framebuffer management for flicker-free rendering
- BMP image loading with memory-efficient streaming
- Full drawing primitives: pixels, lines, rectangles, circles, text
- RGB565 color management with proper byte swapping
- Example demonstrations and test images
- Windows deployment automation via ampy
- Comprehensive documentation

### Technical Details
- Display: 135×240 ST7789 with RGB565 color space
- Memory: 64KB framebuffer optimized for ESP32 constraints
- SPI: 27MHz, polarity=0, phase=0 for M5StickC-PLUS compatibility
- Power: Automatic AXP192 initialization
- Colors: RGB565 with byte swap for correct color display

### Files
- `m5graphics.py` - Main graphics library
- `st7789.py` - Display driver with M5StickC-PLUS optimizations
- `bmp_loader.py` - BMP image loading functionality
- `example.py` - Usage demonstration
- Test images: `small_test.bmp`, `m5_logo.bmp`, `test_pattern.bmp`
- `deploy.py` - Automated Windows deployment script

### Fixed
- Display offset alignment for centered graphics
- RGB565 color byte order for correct color representation
- SPI configuration for stable M5StickC-PLUS communication
- Memory management for large image loading