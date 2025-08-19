"""
BMP Image Loader for MicroPython
Memory-efficient BMP file reader for M5StickC-PLUS
Supports 8-bit and 24-bit uncompressed BMP files with streaming decode
"""

import struct
import gc
from micropython import const

# BMP file header constants
_BMP_SIGNATURE = const(0x4D42)  # "BM"
_BMP_HEADER_SIZE = const(14)
_DIB_HEADER_SIZE = const(40)


def rgb565(r, g, b):
    """Convert 8-bit RGB to 16-bit RGB565 with byte swap"""
    color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return ((color & 0xFF) << 8) | ((color >> 8) & 0xFF)


class BMPLoader:
    """Memory-efficient BMP file loader"""
    
    def __init__(self):
        self.width = 0
        self.height = 0
        self.bits_per_pixel = 0
        self.data_offset = 0
        self.file_size = 0
        self.row_size = 0
        self.palette = None
        self.colors_used = 0
        
    def _read_header(self, file):
        """Read and parse BMP file header"""
        # Read file header (14 bytes)
        file_header = file.read(_BMP_HEADER_SIZE)
        if len(file_header) != _BMP_HEADER_SIZE:
            raise ValueError("Invalid BMP file: header too short")
        
        # Parse file header
        signature, self.file_size, _, _, self.data_offset = struct.unpack('<HLHHL', file_header)
        
        if signature != _BMP_SIGNATURE:
            raise ValueError("Invalid BMP file: wrong signature")
        
        # Read DIB header (40 bytes minimum)
        dib_header = file.read(_DIB_HEADER_SIZE)
        if len(dib_header) != _DIB_HEADER_SIZE:
            raise ValueError("Invalid BMP file: DIB header too short")
        
        # Parse DIB header
        (dib_size, self.width, self.height, planes, self.bits_per_pixel,
         compression, image_size, x_ppm, y_ppm, colors_used, colors_important) = struct.unpack('<LLLHHLLLLLL', dib_header)
        
        # Validate BMP format
        if self.bits_per_pixel not in (8, 24):
            raise ValueError(f"Unsupported BMP format: {self.bits_per_pixel} bits per pixel (only 8-bit and 24-bit supported)")
        
        if compression != 0:
            raise ValueError("Unsupported BMP format: compression not supported")
        
        if planes != 1:
            raise ValueError("Unsupported BMP format: multiple planes")
        
        # Store colors_used for palette loading
        self.colors_used = colors_used
        
        # Calculate row size (padded to 4-byte boundary)
        if self.bits_per_pixel == 8:
            self.row_size = ((self.width + 3) // 4) * 4
        else:  # 24-bit
            self.row_size = ((self.width * 3 + 3) // 4) * 4
        
        return True
    
    def _read_palette(self, file):
        """Read color palette for 8-bit BMP files"""
        if self.bits_per_pixel != 8:
            return True
        
        # Calculate number of palette entries
        palette_entries = self.colors_used if self.colors_used > 0 else 256
        palette_size = palette_entries * 4  # 4 bytes per entry (BGRA)
        
        # Read palette data
        palette_data = file.read(palette_size)
        if len(palette_data) != palette_size:
            raise ValueError("Failed to read color palette")
        
        # Convert palette to RGB565 format
        self.palette = []
        for i in range(palette_entries):
            offset = i * 4
            b = palette_data[offset]
            g = palette_data[offset + 1]
            r = palette_data[offset + 2]
            # Skip alpha byte (offset + 3)
            
            # Convert to RGB565
            color = rgb565(r, g, b)
            self.palette.append(color)
        
        return True
    
    def load_to_framebuffer(self, filename, framebuffer, dest_x=0, dest_y=0, max_width=None, max_height=None):
        """
        Load BMP image directly into framebuffer with memory optimization
        
        Args:
            filename: BMP file path
            framebuffer: Target framebuffer object
            dest_x, dest_y: Destination position in framebuffer
            max_width, max_height: Maximum dimensions to load (for clipping)
        """
        try:
            with open(filename, 'rb') as file:
                # Read and validate header
                self._read_header(file)
                
                # Read color palette for 8-bit BMPs
                self._read_palette(file)
                
                # Determine actual dimensions to load
                load_width = min(self.width, max_width or self.width)
                load_height = min(self.height, max_height or self.height)
                
                # Allocate row buffer (only needs space for one row)
                row_buffer = bytearray(self.row_size)
                
                # BMP rows are stored bottom-to-top, so we read from bottom
                for row in range(load_height):
                    # Calculate file position for this row (from bottom)
                    bmp_row = self.height - 1 - row
                    file_pos = self.data_offset + (bmp_row * self.row_size)
                    
                    # Seek to row start
                    file.seek(file_pos)
                    
                    # Read row data
                    bytes_read = file.readinto(row_buffer)
                    if bytes_read != self.row_size:
                        raise ValueError(f"Failed to read row {row}")
                    
                    # Convert pixels and write to framebuffer
                    for col in range(load_width):
                        if self.bits_per_pixel == 8:
                            # 8-bit BMP: read palette index and look up color
                            palette_index = row_buffer[col]
                            if palette_index < len(self.palette):
                                color = self.palette[palette_index]
                            else:
                                color = 0  # Black for invalid palette index
                        else:
                            # 24-bit BMP: read RGB values directly
                            pixel_offset = col * 3
                            b = row_buffer[pixel_offset]
                            g = row_buffer[pixel_offset + 1]
                            r = row_buffer[pixel_offset + 2]
                            
                            # Convert to RGB565
                            color = rgb565(r, g, b)
                        
                        # Set pixel in framebuffer
                        fb_x = dest_x + col
                        fb_y = dest_y + row
                        
                        if hasattr(framebuffer, 'pixel'):
                            framebuffer.pixel(fb_x, fb_y, color)
                    
                    # Periodic garbage collection for long images
                    if row % 20 == 0:
                        gc.collect()
                
                return True
                
        except OSError as e:
            print(f"File error loading {filename}: {e}")
            return False
        except Exception as e:
            print(f"Error loading BMP {filename}: {e}")
            return False
    
    def get_image_info(self, filename):
        """Get image dimensions and format info without loading"""
        try:
            with open(filename, 'rb') as file:
                self._read_header(file)
                palette_colors = 0
                if self.bits_per_pixel == 8:
                    palette_colors = self.colors_used if self.colors_used > 0 else 256
                return {
                    'width': self.width,
                    'height': self.height,
                    'bits_per_pixel': self.bits_per_pixel,
                    'file_size': self.file_size,
                    'palette_colors': palette_colors
                }
        except Exception as e:
            print(f"Error reading BMP info {filename}: {e}")
            return None