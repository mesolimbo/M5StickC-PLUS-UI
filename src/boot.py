"""
M5StickC-PLUS Graphics Library Boot Script
Automatically runs the graphics example on device startup
"""

import time
import gc

def main():
    """Boot sequence for M5StickC-PLUS"""
    print("M5StickC-PLUS Graphics Library")
    print("Boot sequence starting...")
    
    # Give system time to stabilize
    time.sleep_ms(1000)
    
    # Clean up memory before starting
    gc.collect()
    
    try:
        # Import and run the example
        print("Loading graphics example...")
        from example import main as run_example
        run_example()
        
    except ImportError:
        print("Graphics example not found")
        # Fallback: Basic display test
        try:
            from m5graphics import M5Graphics, WHITE, GREEN, RED
            graphics = M5Graphics()
            if graphics.init_display():
                graphics.clear()
                graphics.text("M5StickC-PLUS", 10, 50, WHITE)
                graphics.text("Graphics Lib", 15, 70, GREEN)
                graphics.text("Ready!", 35, 90, GREEN)
                graphics.rect(5, 45, 125, 55, WHITE)
                graphics.show()
                print("Basic graphics displayed")
            else:
                print("Display init failed")
        except Exception as e:
            print(f"Fallback failed: {e}")
            
    except Exception as e:
        print(f"Boot error: {e}")
        # Try to show error on display
        try:
            from m5graphics import M5Graphics, WHITE, RED
            graphics = M5Graphics()
            if graphics.init_display():
                graphics.clear()
                graphics.text("BOOT ERROR", 25, 100, RED)
                graphics.text("Check USB", 30, 120, WHITE)
                graphics.show()
        except:
            pass

if __name__ == "__main__":
    main()