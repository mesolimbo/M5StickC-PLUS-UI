"""
Music Module for M5StickC-PLUS
Simple music player using the built-in buzzer
"""

import machine
import time
from micropython import const

# M5StickC-PLUS buzzer pin
BUZZER_PIN = const(2)

# Note frequencies in Hz (4th octave)
NOTE_FREQUENCIES = {
    'C': 261,
    'C#': 277,
    'Db': 277,
    'D': 294,
    'D#': 311,
    'Eb': 311,
    'E': 330,
    'F': 349,
    'F#': 370,
    'Gb': 370,
    'G': 392,
    'G#': 415,
    'Ab': 415,
    'A': 440,
    'A#': 466,
    'Bb': 466,
    'B': 494,
    'REST': 0  # Silence
}

# Different octave multipliers
OCTAVE_MULTIPLIERS = {
    3: 0.5,   # Lower octave
    4: 1.0,   # Base octave
    5: 2.0,   # Higher octave
    6: 4.0    # Very high octave
}


class MusicPlayer:
    """Simple music player for M5StickC-PLUS buzzer"""
    
    def __init__(self):
        self.buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
        self.buzzer.duty(0)  # Start silent
        self._playing = False
        
    def play_note(self, note, duration_ms=500, octave=4):
        """
        Play a single note
        
        Args:
            note: Note name (C, D, E, F, G, A, B, C#, etc.) or 'REST'
            duration_ms: Duration in milliseconds
            octave: Octave number (3, 4, 5, 6)
        """
        if note.upper() not in NOTE_FREQUENCIES:
            print(f"Unknown note: {note}")
            return
            
        freq = NOTE_FREQUENCIES[note.upper()]
        
        if freq > 0:  # Not a rest
            # Apply octave multiplier
            freq = int(freq * OCTAVE_MULTIPLIERS.get(octave, 1.0))
            
            # Simple, reliable PWM setup
            self.buzzer.freq(freq)
            self.buzzer.duty(512)  # Back to 50% duty cycle
        else:
            # Rest (silence)
            self.buzzer.duty(0)
        
        # Play for specified duration
        time.sleep_ms(duration_ms)
        
        # Brief pause between notes
        self.buzzer.duty(0)
        time.sleep_ms(50)
    
    def play_melody(self, notes, note_duration=400, octave=4):
        """
        Play a sequence of notes
        
        Args:
            notes: String of notes like "CDEFGAB" or list of note names
            note_duration: Duration of each note in milliseconds
            octave: Base octave for all notes
        """
        self._playing = True
        
        try:
            if isinstance(notes, str):
                # Parse string of notes
                i = 0
                while i < len(notes) and self._playing:
                    note = notes[i]
                    
                    # Check for sharp/flat
                    if i + 1 < len(notes) and notes[i + 1] in '#b':
                        note += notes[i + 1]
                        i += 1
                    
                    # Skip spaces
                    if note == ' ':
                        i += 1
                        continue
                    
                    self.play_note(note, note_duration, octave)
                    i += 1
            
            elif isinstance(notes, list):
                # List of notes
                for note in notes:
                    if not self._playing:
                        break
                    self.play_note(note, note_duration, octave)
        
        finally:
            self._playing = False
            self.buzzer.duty(0)
    
    def play_dreidel_song(self, tempo=600):
        """
        Play the dreidel song: "GGEGEGE EGGFED DFDFDFD DGFEDC"
        """
        print("Playing dreidel song...")
        
        # Simple initialization
        self.buzzer.duty(0)
        time.sleep_ms(100)
        
        # Break the song into phrases with appropriate timing
        phrases = [
            "GEGEGE",   # First phrase
            "EGGFED",    # Second phrase  
            "DFDFDFD",   # Third phrase
            "DGFEDC"     # Final phrase
        ]
        
        for i, phrase in enumerate(phrases):
            print(f"Playing phrase {i+1}: {phrase}")
            self.play_melody(phrase, tempo, octave=4)
            
            # Brief pause between phrases
            if i < len(phrases) - 1:
                time.sleep_ms(200)
        
        # Smooth ending - ensure last note fades cleanly
        time.sleep_ms(100)
        self.buzzer.duty(0)
        
        print("Dreidel song complete!")
    
    def play_scale(self, octave=4):
        """Play a simple C major scale"""
        scale = "CDEFGABC"
        print(f"Playing C major scale (octave {octave})")
        self.play_melody(scale, 300, octave)
    
    def stop(self):
        """Stop playing music"""
        self._playing = False
        self.buzzer.duty(0)
    
    def cleanup(self):
        """Clean up PWM resources"""
        self.stop()
        self.buzzer.deinit()


# Quick test function
def test_music():
    """Test the music player"""
    print("Testing M5StickC-PLUS music player...")
    
    player = MusicPlayer()
    
    try:
        # Test individual notes
        print("Testing individual notes...")
        for note in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
            print(f"Playing {note}")
            player.play_note(note, 300)
        
        time.sleep_ms(500)
        
        # Test the dreidel song
        player.play_dreidel_song()
        
    finally:
        player.cleanup()


if __name__ == "__main__":
    test_music()