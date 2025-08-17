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
    
    # Try to load test images
    if graphics.load_bmp("small_test.bmp", 35, 50):
        print("Small BMP loaded!")
        graphics.text("Small BMP OK", 15, 30, GREEN)
        graphics.show()
        time.sleep_ms(2000)
        
        # Try full-size image
        if graphics.load_bmp("m5_logo.bmp", 0, 0):
            print("Full-size BMP loaded!")
            graphics.show()
            time.sleep_ms(10000)
    else:
        print("No BMP images found")
        graphics.text("No BMP files", 20, 50, YELLOW)
        graphics.show()
        time.sleep_ms(1000)
    
    # # Final screen
    # graphics.clear(GREEN)
    # graphics.text("GRAPHICS", 25, 80, BLACK)
    # graphics.text("LIBRARY", 30, 100, BLACK)
    # graphics.text("READY!", 35, 120, BLACK)
    #
    # # Draw border
    # graphics.rect(0, 0, 135, 240, BLACK)
    #
    # graphics.show()
    
    print("Example completed successfully!")
    print("Graphics library is ready for use!")

if __name__ == "__main__":
    main()