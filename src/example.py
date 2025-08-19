"""
M5StickC-PLUS Graphics Library Example
Demonstrates basic usage of the graphics library
"""

from m5graphics import M5Graphics, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, rgb565
import time

def main():
    """Demonstrate graphics library features"""
    print("M5StickC-PLUS Graphics Library Example")
    print("======================================")
    
    # Initialize graphics
    graphics = M5Graphics()
    
    if not graphics.init_display():
        print("Failed to initialize display!")
        return
    
    print("Display initialized successfully!")
    
    # Demo 1: Basic shapes
    print("Drawing basic shapes...")
    graphics.clear(BLACK)
    
    # Draw shapes
    graphics.rect(10, 10, 50, 30, WHITE)              # Rectangle outline
    graphics.rect(70, 10, 50, 30, GREEN, fill=True)   # Filled rectangle
    graphics.line(10, 50, 125, 50, RED)               # Line
    graphics.circle(30, 80, 15, BLUE)                 # Circle outline
    graphics.circle(100, 80, 15, YELLOW, fill=True)   # Filled circle
    
    graphics.show()
    time.sleep_ms(2000)
    
    # Demo 2: Text rendering
    print("Drawing text...")
    graphics.clear(BLACK)
    
    graphics.text("M5StickC-PLUS", 10, 20, WHITE)
    graphics.text("Graphics Lib", 15, 40, GREEN)
    graphics.text("Working!", 30, 60, YELLOW)
    graphics.text("RGB565 Colors", 5, 90, rgb565(255, 128, 0))
    graphics.text("BG Text", 30, 120, BLACK, WHITE)  # Text with background
    
    graphics.show()
    time.sleep_ms(2000)
    
    # Demo 3: Color gradient
    print("Drawing color gradient...")
    graphics.clear(BLACK)
    
    # Create a rainbow gradient
    for x in range(120):
        r = int(255 * (x / 120))
        g = int(255 * (1 - x / 120))
        b = 128
        color = rgb565(r, g, b)
        graphics.vline(x + 7, 50, 100, color)
    
    graphics.text("Gradient", 35, 20, WHITE)
    graphics.text("Demo", 45, 170, WHITE)
    
    graphics.show()
    time.sleep_ms(2000)
    
    # Demo 4: Animation
    print("Simple animation...")
    for i in range(15):
        graphics.clear(BLACK)
        
        # Moving circle
        x = 10 + i * 8
        graphics.circle(x, 120, 8, RED, fill=True)
        
        # Frame counter
        graphics.text(f"Frame {i+1}", 10, 10, WHITE)
        
        graphics.show()
        time.sleep_ms(150)
    
    # Demo 5: BMP loading (if available)
    print("Testing BMP loading...")
    graphics.clear(BLACK)
    graphics.text("BMP Test", 35, 10, WHITE)
    
    # Test different BMP formats
    bmp_files = [
        ("icon_8bit.bmp", "8-bit icon"),
        ("photo_24bit.bmp", "24-bit photo"),
        ("small_test.bmp", "Test image"),
        ("m5_logo.bmp", "M5 logo")
    ]
    
    loaded_any = False
    for filename, description in bmp_files:
        print(f"Trying to load {filename} ({description})...")
        
        # Get image info first
        info = graphics.get_bmp_info(filename)
        if info:
            print(f"  {info['width']}x{info['height']}, {info['bits_per_pixel']}-bit")
            if info.get('palette_colors', 0) > 0:
                print(f"  Palette: {info['palette_colors']} colors")
        
        # Position image based on size - center small images, top-left for large ones
        if info and info['width'] <= 64:
            # Small image - center it
            x_pos = (135 - info['width']) // 2
            y_pos = (240 - info['height']) // 2
        else:
            # Large image - top-left corner
            x_pos = 0
            y_pos = 0
        
        if graphics.load_bmp(filename, x_pos, y_pos):
            print(f"  {description} loaded successfully!")
            graphics.text(f"{info['bits_per_pixel']}-bit BMP", 10, 30, GREEN)
            graphics.text("Loaded OK", 20, 200, GREEN)
            graphics.show()
            time.sleep_ms(2000)
            loaded_any = True
            graphics.clear(BLACK)
            graphics.text("BMP Test", 35, 10, WHITE)
    
    if not loaded_any:
        print("No BMP images found")
        graphics.text("No BMP files", 20, 50, YELLOW)
        graphics.text("8-bit & 24-bit", 15, 70, CYAN)
        graphics.text("supported!", 25, 90, CYAN)
        graphics.show()
        time.sleep_ms(2000)
    
    print("Example completed successfully!")
    print("Graphics library is ready for use!")

if __name__ == "__main__":
    main()