"""
Dreidel Game for M5StickC-PLUS
Press Button A to spin the dreidel and play the dreidel song!
"""

import machine
import time
import random
from m5graphics import M5Graphics, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA
from music import MusicPlayer

# Dreidel symbols and their meanings
DREIDEL_SYMBOLS = [
    {"symbol": "נ", "name": "Nun", "meaning": "Nothing", "color": BLUE},
    {"symbol": "ג", "name": "Gimel", "meaning": "Get All", "color": GREEN}, 
    {"symbol": "ה", "name": "Hey", "meaning": "Half", "color": YELLOW},
    {"symbol": "ש", "name": "Shin", "meaning": "Put In", "color": RED}
]

# Alternative ASCII symbols if Hebrew doesn't display well
ASCII_SYMBOLS = [
    {"symbol": "N", "name": "Nun", "meaning": "Nothing", "color": BLUE},
    {"symbol": "G", "name": "Gimel", "meaning": "Get All", "color": GREEN},
    {"symbol": "H", "name": "Hey", "meaning": "Half", "color": YELLOW}, 
    {"symbol": "S", "name": "Shin", "meaning": "Put In", "color": RED}
]

class DreidlGame:
    """Dreidel game with button control and music"""
    
    def __init__(self):
        self.graphics = M5Graphics()
        self.music_player = MusicPlayer()
        self.last_button_time = 0
        self.use_ascii = True  # Use ASCII symbols by default
        
        # Game state
        self.current_result = None
        self.spinning = False
        
    def init_hardware(self):
        """Initialize display"""
        if not self.graphics.init_display():
            print("Failed to initialize display!")
            return False
        
        print("Display initialized successfully")
        return True
    
    def detect_button_press(self):
        """Detect button A press to spin dreidel"""
        current_time = time.ticks_ms()
        
        # Prevent too frequent button presses  
        if time.ticks_diff(current_time, self.last_button_time) < 3000:
            return False
        
        # Check button A
        button_a = machine.Pin(37, machine.Pin.IN, machine.Pin.PULL_UP)
        
        if not button_a.value():  # Button pressed (pulled low)
            self.last_button_time = current_time
            time.sleep_ms(200)  # Debounce
            return True
        
        return False
    
    def spin_dreidel(self):
        """Spin the dreidel and return random result"""
        print("Spinning dreidel...")
        self.spinning = True
        
        # Pick random result first (but don't show it yet)
        symbols = ASCII_SYMBOLS if self.use_ascii else DREIDEL_SYMBOLS
        result = random.choice(symbols)
        
        # Play music and show spinning animation simultaneously
        self.spin_with_music()
        
        self.current_result = result
        self.spinning = False
        
        return result
    
    def spin_with_music(self):
        """Play music while showing spinning animation"""
        try:
            import _thread
            
            # Start music in background thread
            _thread.start_new_thread(self.play_dreidel_song, ())
            
            # Show spinning animation for the duration of the song
            # Exact timing calculation at 250ms per note:
            # GGEGEGE (7 notes) + EGGFED (6 notes) + DFDFDFD (7 notes) + DGFEDC (6 notes) = 26 notes  
            # 26 notes * (250ms + 50ms pause) = 7800ms
            # + 3 phrase pauses * 200ms = 600ms
            # + startup 100ms + ending 100ms = 200ms
            # Total: ~8600ms, add buffer for safety
            self.show_spinning_animation_timed(9000)  # 9 seconds to ensure music finishes
            
        except:
            # Fallback: simpler approach without threading
            print("Using fallback music/animation...")
            self.play_music_with_simple_animation()
    
    def show_spinning_animation_timed(self, duration_ms):
        """Show spinning animation for a specific duration"""
        spin_chars = ["|", "/", "-", "\\"]
        start_time = time.ticks_ms()
        char_index = 0
        
        while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
            char = spin_chars[char_index % len(spin_chars)]
            char_index += 1
            
            self.graphics.clear(BLACK)
            self.graphics.text("DREIDEL", 35, 20, WHITE)
            self.graphics.text("Spinning...", 25, 60, YELLOW)
            
            # Draw larger spinning symbol using multiple characters
            for i in range(3):
                for j in range(3):
                    self.graphics.text(char, 55 + j*8, 100 + i*10, CYAN)
            
            self.graphics.text("Playing music!", 15, 180, MAGENTA)
            self.graphics.show()
            time.sleep_ms(300)  # Slower animation to reduce PWM interference
    
    def play_music_with_simple_animation(self):
        """Fallback: interleave music and animation"""
        phrases = ["GGEGEGE", "EGGFED", "DFDFDFD", "DGFEDC"]
        spin_chars = ["|", "/", "-", "\\"]
        
        for phrase_idx, phrase in enumerate(phrases):
            # Show spinning animation for this phrase
            for note_idx, note in enumerate(phrase):
                char = spin_chars[(phrase_idx * len(phrase) + note_idx) % len(spin_chars)]
                
                self.graphics.clear(BLACK)
                self.graphics.text("DREIDEL", 35, 20, WHITE)
                self.graphics.text("Spinning...", 25, 60, YELLOW)
                
                # Draw spinning symbol
                for i in range(3):
                    for j in range(3):
                        self.graphics.text(char, 55 + j*8, 100 + i*10, CYAN)
                
                self.graphics.text(f"Phrase {phrase_idx+1}", 30, 180, MAGENTA)
                self.graphics.show()
                
                # Play note while showing animation
                self.music_player.play_note(note, 250, 4)
            
            # Brief pause between phrases
            if phrase_idx < len(phrases) - 1:
                time.sleep_ms(200)
    
    def show_spinning_animation(self):
        """Show spinning animation"""
        spin_chars = ["|", "/", "-", "\\"]
        
        for _ in range(8):  # Shorter spin animation
            for char in spin_chars:
                self.graphics.clear(BLACK)
                self.graphics.text("DREIDEL", 35, 20, WHITE)
                self.graphics.text("Spinning...", 25, 60, YELLOW)
                
                # Draw larger spinning symbol using multiple characters
                for i in range(3):
                    for j in range(3):
                        self.graphics.text(char, 55 + j*8, 100 + i*10, CYAN)
                
                self.graphics.show()
                time.sleep_ms(150)
    
    def show_result(self, result):
        """Display the dreidel result"""
        self.graphics.clear(BLACK)
        
        # Title
        self.graphics.text("RESULT", 40, 10, WHITE)
        
        # Draw large symbol using multiple characters for visibility
        symbol = result["symbol"]
        for i in range(4):
            for j in range(4):
                self.graphics.text(symbol, 50 + j*8, 40 + i*12, result["color"])
        
        # Name and meaning (ensure text fits)
        name = result["name"][:8]  # Limit to 8 chars
        meaning = result["meaning"][:10]  # Limit to 10 chars
        
        self.graphics.text(name, 45, 110, WHITE)
        self.graphics.text(meaning, 30, 130, result["color"])
        
        # Instructions (fit within width)
        self.graphics.text("Press A", 40, 170, GREEN)
        self.graphics.text("to spin!", 35, 190, GREEN)
        
        self.graphics.show()
    
    def show_welcome_screen(self):
        """Show welcome screen"""
        self.graphics.clear(BLACK)
        self.graphics.text("DREIDEL", 35, 20, WHITE)
        self.graphics.text("GAME", 50, 40, WHITE)
        
        self.graphics.text("Press A", 40, 80, YELLOW)
        self.graphics.text("to spin!", 35, 100, YELLOW)
        
        # Show 4 dreidel symbols in a 2x2 grid
        symbols = ASCII_SYMBOLS if self.use_ascii else DREIDEL_SYMBOLS
        positions = [(30, 130), (80, 130), (30, 160), (80, 160)]
        
        for i, symbol in enumerate(symbols):
            if i < 4:
                x, y = positions[i]
                # Draw larger symbols
                for dx in range(2):
                    for dy in range(2):
                        self.graphics.text(symbol["symbol"], x + dx*8, y + dy*8, symbol["color"])
        
        self.graphics.text("Music & Fun!", 20, 200, MAGENTA)
        self.graphics.show()
    
    def play_dreidel_song(self):
        """Play the dreidel song"""
        try:
            print("Playing dreidel song...")
            self.music_player.play_dreidel_song(250)  # Fast tempo - 250ms per note
        except Exception as e:
            print(f"Music error: {e}")
    
    def run_game(self):
        """Main game loop"""
        print("Starting Dreidel Game!")
        
        if not self.init_hardware():
            print("Hardware initialization failed!")
            return
        
        self.show_welcome_screen()
        
        try:
            while True:
                if self.detect_button_press():
                    print("Button pressed! Spinning dreidel...")
                    
                    # Spin (music plays during spinning)
                    result = self.spin_dreidel()
                    
                    # Show result after music/spinning completes
                    self.show_result(result)
                    
                    print(f"Result: {result['name']} - {result['meaning']}")
                
                time.sleep_ms(50)  # Small delay to prevent busy waiting
                
        except KeyboardInterrupt:
            print("Game stopped by user")
        except Exception as e:
            print(f"Game error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.music_player.cleanup()
        except:
            pass
        print("Game cleanup complete")


def main():
    """Run the dreidel game"""
    game = DreidlGame()
    game.run_game()


if __name__ == "__main__":
    main()