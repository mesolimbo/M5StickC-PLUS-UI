"""
Dreidel Game for M5StickC-PLUS
Press Button A to spin the dreidel and play the dreidel song!
"""

import machine
import time
import random
from m5graphics import M5Graphics
from music import MusicPlayer

# Dreidel symbols mapped to BMP files
DREIDEL_SYMBOLS = [
    {"name": "Nun", "meaning": "Nothing", "bmp": "nun.bmp"},
    {"name": "Gimel", "meaning": "Everything", "bmp": "gimel.bmp"}, 
    {"name": "Hey", "meaning": "Half", "bmp": "hey.bmp"},
    {"name": "Shin", "meaning": "Put In", "bmp": "shin.bmp"}
]

class DreidlGame:
    """Dreidel game with button control and music"""
    
    def __init__(self):
        self.graphics = M5Graphics()
        self.music_player = MusicPlayer()
        self.last_button_time = 0
        
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
        result = random.choice(DREIDEL_SYMBOLS)
        
        # Play music and show spinning animation simultaneously
        self.spin_with_music()
        
        self.current_result = result
        self.spinning = False
        
        return result
    
    def spin_with_music(self):
        """Start spinning animation immediately, then play music simultaneously"""
        try:
            import _thread
            
            # Start spinning animation immediately
            # Start music in background thread at the same time
            _thread.start_new_thread(self.play_dreidel_song, ())
            
            # Show spinning animation for the exact duration of the song
            # Precise timing calculation at 250ms per note:
            # GGEGEGE (7 notes) + EGGFED (6 notes) + DFDFDFD (7 notes) + DGFEDC (6 notes) = 26 notes  
            # 26 notes * (250ms + 50ms pause) = 7800ms
            # + 3 phrase pauses * 200ms = 600ms
            # + startup 100ms + ending 100ms = 200ms
            # Total: ~8600ms - match exactly
            self.show_spinning_animation_timed(8600)  # Exact music duration
            
        except:
            # Fallback: simpler approach without threading
            print("Using fallback music/animation...")
            self.play_music_with_simple_animation()
    
    def show_spinning_animation_timed(self, duration_ms):
        """Show spinning animation for a specific duration using bitmap alternation"""
        start_time = time.ticks_ms()
        left_turn = True
        
        # Start spinning immediately - show first frame right away
        self.graphics.load_bmp("left.bmp", 0, 0)  # Start with left image
        self.graphics.load_bmp("base.bmp", 0, 164)  # Base at bottom
        self.graphics.show()
        
        while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
            left_turn = not left_turn  # Toggle for next frame
            
            # Alternate between left and right dreidel images
            if left_turn:
                self.graphics.load_bmp("left.bmp", 0, 0)
            else:
                self.graphics.load_bmp("right.bmp", 0, 0)
            
            self.graphics.show()
            time.sleep_ms(150)  # Faster spin animation
    
    def play_music_with_simple_animation(self):
        """Fallback: interleave music and animation using bitmaps"""
        phrases = ["GGEGEGE", "EGGFED", "DFDFDFD", "DGFEDC"]
        
        # Start spinning immediately - show first frame right away
        self.graphics.load_bmp("left.bmp", 0, 0)  # Start with left image
        self.graphics.load_bmp("base.bmp", 0, 164)  # Base at bottom
        self.graphics.show()
        
        left_turn = True
        
        for phrase_idx, phrase in enumerate(phrases):
            # Show spinning animation for this phrase
            for note_idx, note in enumerate(phrase):
                left_turn = not left_turn  # Toggle for next frame
                
                # Alternate between left and right dreidel images
                if left_turn:
                    self.graphics.load_bmp("left.bmp", 0, 0)
                else:
                    self.graphics.load_bmp("right.bmp", 0, 0)
                
                self.graphics.show()
                
                # Play note while showing animation
                self.music_player.play_note(note, 250, 4)
            
            # Brief pause between phrases
            if phrase_idx < len(phrases) - 1:
                time.sleep_ms(200)
    
    
    def show_result(self, result):
        """Display the dreidel result using BMP graphics"""
        # Load the result image (contains symbol, name, and meaning)
        self.graphics.load_bmp(result["bmp"], 0, 0)
        
        # Load prompt image at bottom (always show prompt on results)
        self.graphics.load_bmp("prompt.bmp", 0, 164)
        
        self.graphics.show()
    
    
    def show_welcome_screen(self):
        """Show welcome screen with blinking prompt"""
        # Show intro image at top (135x164)
        self.graphics.load_bmp("intro.bmp", 0, 0)
        
        # Blinking prompt animation at bottom - faster
        for blink in range(6):  # Blink 3 times
            # Show base image
            self.graphics.load_bmp("base.bmp", 0, 164)
            self.graphics.show()
            time.sleep_ms(250)  # Faster blinking
            
            # Show prompt image
            self.graphics.load_bmp("prompt.bmp", 0, 164)
            self.graphics.show()
            time.sleep_ms(250)  # Faster blinking
        
        # End with prompt visible
        self.graphics.load_bmp("prompt.bmp", 0, 164)
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
        
        # Track when to do periodic blinking
        last_blink_time = time.ticks_ms()
        blink_state = True  # True = prompt visible, False = base visible
        
        try:
            while True:
                if self.detect_button_press():
                    print("Button pressed! Spinning dreidel...")
                    
                    # Spin (music plays during spinning)
                    result = self.spin_dreidel()
                    
                    # Show result after music/spinning completes
                    self.show_result(result)
                    print(f"Result: {result['name']} - {result['meaning']}")
                    
                    # Reset blink timing after showing result
                    last_blink_time = time.ticks_ms()
                    blink_state = True
                else:
                    # Periodic blinking when idle (every 2 seconds)
                    current_time = time.ticks_ms()
                    if time.ticks_diff(current_time, last_blink_time) > 2000:
                        # Quick blink to show activity
                        if blink_state:
                            # Show base briefly
                            self.graphics.load_bmp("base.bmp", 0, 164)
                            self.graphics.show()
                            time.sleep_ms(200)
                            # Back to prompt
                            self.graphics.load_bmp("prompt.bmp", 0, 164)
                            self.graphics.show()
                        
                        last_blink_time = current_time
                
                time.sleep_ms(20)  # Smaller delay for better button responsiveness
                
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