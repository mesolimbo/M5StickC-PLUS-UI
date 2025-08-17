"""
M5StickC-PLUS Graphics Library Deployment Script
Deploys the graphics library to M5StickC-PLUS via serial connection
Windows-specific deployment for COM4
"""

import os
import sys
import subprocess
import time

# Device configuration
DEVICE_PORT = "COM4"
BAUD_RATE = 115200

# Files to deploy
LIBRARY_FILES = [
    "m5graphics.py",
    "st7789.py", 
    "bmp_loader.py"
]

EXAMPLE_FILES = [
    "example.py",
    "boot.py"
]

def check_dependencies():
    """Check if required deployment tools are installed"""
    try:
        import serial
        print("✓ pyserial found")
    except ImportError:
        print("✗ pyserial not found - run: pip install pyserial")
        return False
    
    try:
        result = subprocess.run(["ampy", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ampy found")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print("✗ ampy not found - run: pip install adafruit-ampy")
        return False
    
    return True

def check_device_connection():
    """Check if M5StickC-PLUS is connected on COM4"""
    try:
        import serial
        ser = serial.Serial(DEVICE_PORT, BAUD_RATE, timeout=1)
        ser.close()
        print(f"✓ Device connected on {DEVICE_PORT}")
        return True
    except serial.SerialException:
        print(f"✗ Cannot connect to device on {DEVICE_PORT}")
        print("  - Check device is connected")
        print("  - Check COM port number")
        print("  - Try resetting the device")
        return False

def run_ampy_command(args):
    """Run ampy command with proper error handling"""
    cmd = ["ampy", "-p", DEVICE_PORT, "-b", str(BAUD_RATE)] + args
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"Command failed with error: {result.stderr}")
            return False
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print("Command timed out - device may be unresponsive")
        return False
    except Exception as e:
        print(f"Command failed: {e}")
        return False

def deploy_file(filename, remote_path=None):
    """Deploy a single file to the device"""
    if not os.path.exists(filename):
        print(f"✗ File not found: {filename}")
        return False
    
    remote_name = remote_path or filename
    print(f"Deploying {filename} -> {remote_name}")
    
    success = run_ampy_command(["put", filename, remote_name])
    if success:
        print(f"✓ {filename} deployed successfully")
    else:
        print(f"✗ Failed to deploy {filename}")
    
    return success

def list_device_files():
    """List files on the device"""
    print("\nFiles on device:")
    run_ampy_command(["ls"])

def test_deployment():
    """Test the deployment by running a simple import"""
    print("\nTesting deployment...")
    test_script = """
try:
    from m5graphics import M5Graphics
    print("✓ M5Graphics library imported successfully")
    print("✓ Deployment test passed")
except Exception as e:
    print(f"✗ Import failed: {e}")
"""
    
    # Write test script to temporary file
    with open("test_import.py", "w") as f:
        f.write(test_script)
    
    # Deploy and run test
    if deploy_file("test_import.py"):
        print("Running import test...")
        success = run_ampy_command(["run", "test_import.py"])
        
        # Clean up test file
        run_ampy_command(["rm", "test_import.py"])
        os.remove("test_import.py")
        
        return success
    
    return False

def main():
    """Main deployment function"""
    print("M5StickC-PLUS Graphics Library Deployment")
    print("==========================================")
    print(f"Target device: {DEVICE_PORT}")
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\nInstall missing dependencies with:")
        print("pipenv install")
        return False
    
    # Check device connection
    print("\nChecking device connection...")
    if not check_device_connection():
        return False
    
    # List current device files
    print("\nCurrent device files:")
    list_device_files()
    
    # Deploy library files
    print(f"\nDeploying {len(LIBRARY_FILES)} library files...")
    failed_files = []
    
    for filename in LIBRARY_FILES:
        if not deploy_file(filename):
            failed_files.append(filename)
        time.sleep(0.5)  # Small delay between files
    
    # Deploy example files
    print(f"\nDeploying {len(EXAMPLE_FILES)} example files...")
    for filename in EXAMPLE_FILES:
        if not deploy_file(filename):
            failed_files.append(filename)
        time.sleep(0.5)
    
    # Report results
    if failed_files:
        print(f"\n✗ Deployment failed for {len(failed_files)} files:")
        for filename in failed_files:
            print(f"  - {filename}")
        return False
    
    print("\n✓ All files deployed successfully!")
    
    # Test deployment
    if test_deployment():
        print("\n" + "="*50)
        print("Deployment completed successfully!")
        print("\nTo test the graphics library:")
        print("1. Connect to the device REPL")
        print("2. Run: exec(open('example.py').read())")
        print("\nOr use ampy to run directly:")
        print(f"ampy -p {DEVICE_PORT} run example.py")
        
        # Show final file listing
        print("\nFinal device files:")
        list_device_files()
        
        return True
    else:
        print("\n✗ Deployment test failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nDeployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nDeployment failed with error: {e}")
        sys.exit(1)