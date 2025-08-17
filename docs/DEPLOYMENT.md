# M5StickC-PLUS Graphics Library Deployment Guide

## Windows Deployment to COM4

### Prerequisites

1. **M5StickC-PLUS connected via USB to COM4**
2. **MicroPython firmware installed** (from firmware_downloads directory)
3. **Python 3.12 with pipenv**

### Quick Deployment

```bash
# 1. Install dependencies
pipenv install

# 2. Activate virtual environment  
pipenv shell

# 3. Deploy to device
python deploy.py
```

### Manual Deployment (Alternative)

If the automated script fails, deploy manually:

```bash
# Install ampy if not already installed
pip install adafruit-ampy

# Deploy core library files
ampy -p COM4 put m5graphics.py
ampy -p COM4 put st7789.py  
ampy -p COM4 put bmp_loader.py

# Deploy example
ampy -p COM4 put example.py

# List files on device
ampy -p COM4 ls

# Test the library
ampy -p COM4 run example.py
```

### Testing the Installation

#### Option 1: Run example script
```bash
ampy -p COM4 run example.py
```

#### Option 2: Interactive REPL test
Connect to device REPL and run:
```python
from m5graphics import M5Graphics, WHITE, RED, GREEN
graphics = M5Graphics()
graphics.init_display()
graphics.clear()
graphics.text("Hello M5!", 10, 10, WHITE)
graphics.rect(10, 30, 50, 20, RED)
graphics.show()
```

### Troubleshooting

#### "Device not found on COM4"
- Check USB connection
- Verify COM port in Device Manager
- Try pressing reset button on M5StickC-PLUS
- Update COM port in `deploy.py` if different

#### "Permission denied" or "Access denied"
- Close any open serial monitors (Arduino IDE, PuTTY, etc.)
- Ensure no other programs are using COM4
- Try unplugging and reconnecting device

#### "Module not found" errors
```bash
# Install missing dependencies
pipenv install adafruit-ampy pyserial esptool
```

#### Memory errors on device
- Reset the device: `ampy -p COM4 reset`
- Check available memory in REPL:
```python
import gc
gc.collect()
print("Free memory:", gc.mem_free())
```

### File Structure on Device

After successful deployment:
```
/ (root)
├── m5graphics.py      # Main graphics library
├── st7789.py          # Display driver  
├── bmp_loader.py      # BMP image loader
└── example.py         # Usage examples
```

### Adding BMP Images

To test BMP loading functionality:

1. **Create BMP images** (24-bit, uncompressed, max 135×240)
2. **Transfer to device**:
```bash
ampy -p COM4 put sample.bmp
```
3. **Load in code**:
```python
graphics.load_bmp("sample.bmp")
```

### Performance Expectations

- **Library loading**: ~2-3 seconds
- **Display initialization**: ~1 second  
- **Full screen clear/show**: ~25ms
- **BMP image loading**: 1-3 seconds (depends on size)
- **Memory usage**: ~67KB (64KB framebuffer + 3KB library)

### Next Steps

1. **Run the example**: `python deploy.py` or `ampy -p COM4 run example.py`
2. **Create your own graphics**: Use the API from README.md
3. **Add custom images**: Follow BMP creation guide
4. **Build applications**: Integrate with sensors and UI elements

### Serial Monitor Access

To view debug output and interact with REPL:
```bash
# Using built-in Python
python -m serial.tools.miniterm COM4 115200

# Or using PuTTY/similar terminal emulator
# Port: COM4, Baud: 115200, Data: 8N1
```

### Common Commands

```bash
# Deploy all files
python deploy.py

# Run example on device  
ampy -p COM4 run example.py

# Check device files
ampy -p COM4 ls

# Get file from device
ampy -p COM4 get boot.py

# Remove file from device  
ampy -p COM4 rm filename.py

# Reset device
ampy -p COM4 reset
```

The graphics library is now ready for development on your M5StickC-PLUS!