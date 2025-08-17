"""
M5StickC-PLUS Graphics Library Setup
Simple setup utility for deploying the graphics library to M5StickC-PLUS
"""

import os
import sys

def check_files():
    """Check if all required files are present"""
    required_files = [
        'm5graphics.py',
        'st7789.py', 
        'bmp_loader.py',
        'example.py',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("All required files found:")
    for file in required_files:
        size = os.path.getsize(file)
        print(f"  ✓ {file} ({size} bytes)")
    
    return True

def estimate_memory_usage():
    """Estimate memory usage of the library"""
    core_files = ['m5graphics.py', 'st7789.py', 'bmp_loader.py']
    total_size = 0
    
    print("\nEstimated memory usage:")
    for file in core_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            total_size += size
            print(f"  {file}: ~{size // 1024 + 1}KB")
    
    print(f"  Framebuffer: ~64KB")
    print(f"  Total estimated: ~{(total_size // 1024) + 64 + 5}KB")
    print("\nNote: Actual runtime memory usage may differ.")

def create_sample_bmp_info():
    """Create instructions for BMP sample creation"""
    bmp_info = """
# Creating Sample BMP Images

To test BMP loading functionality, create sample images:

1. Use any graphics editor (GIMP, Photoshop, Paint.NET, etc.)
2. Create image with dimensions 135×240 or smaller
3. Save/Export as:
   - Format: BMP (Bitmap)
   - Color depth: 24-bit RGB
   - Compression: None/Uncompressed
   - File name: sample.bmp

4. Transfer to M5StickC-PLUS flash storage
5. Run example.py to test loading

Sample image ideas:
- Simple logo or icon
- Gradient patterns
- Test patterns with different colors
- Text or diagrams

File size recommendations:
- Small images (64×64): ~12KB
- Medium images (135×120): ~48KB  
- Full screen (135×240): ~97KB
"""
    
    with open('bmp_guide.txt', 'w') as f:
        f.write(bmp_info)
    
    print("Created 'bmp_guide.txt' with BMP creation instructions")

def main():
    """Main setup function"""
    print("M5StickC-PLUS Graphics Library Setup")
    print("=====================================")
    
    # Check files
    if not check_files():
        print("\nSetup incomplete - missing files!")
        return False
    
    # Memory estimation
    estimate_memory_usage()
    
    # Create BMP guide
    create_sample_bmp_info()
    
    print("\n" + "="*50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy all .py files to your M5StickC-PLUS")
    print("2. Run 'example.py' to test the library")
    print("3. Create BMP images following 'bmp_guide.txt'")
    print("4. Read 'README.md' for full documentation")
    print("\nQuick test:")
    print(">>> from m5graphics import M5Graphics")
    print(">>> graphics = M5Graphics()")
    print(">>> graphics.init_display()")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)