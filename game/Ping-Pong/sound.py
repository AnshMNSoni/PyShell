import os
import sys
import time

# Simple sound implementation that works cross-platform
class Sound:
    def __init__(self):
        self.sound_enabled = self._check_sound_support()
        
    def _check_sound_support(self):
        """Check if sound is supported on this platform"""
        try:
            # Try to import required modules
            import winsound
            return True
        except ImportError:
            try:
                # For Unix systems
                import subprocess
                return True
            except ImportError:
                return False
    
    def play_bounce(self):
        """Play bounce sound"""
        if self.sound_enabled:
            self._play_sound("bounce")
    
    def play_score(self):
        """Play score sound"""
        if self.sound_enabled:
            self._play_sound("score")
            
    def play_powerup(self):
        """Play power-up sound"""
        if self.sound_enabled:
            self._play_sound("powerup")
    
    def _play_sound(self, sound_type):
        """Play a sound based on platform"""
        try:
            if sys.platform.startswith('win'):
                import winsound
                frequencies = {
                    "bounce": 500,
                    "score": 800,
                    "powerup": 1200
                }
                durations = {
                    "bounce": 100,
                    "score": 300,
                    "powerup": 200
                }
                winsound.Beep(frequencies.get(sound_type, 500), durations.get(sound_type, 100))
            elif sys.platform.startswith('darwin'):  # macOS
                sounds = {
                    "bounce": "ping",
                    "score": "tink",
                    "powerup": "pop"
                }
                os.system(f"afplay /System/Library/Sounds/{sounds.get(sound_type, 'ping')}.aiff &")
            else:  # Linux and others
                frequencies = {
                    "bounce": "500",
                    "score": "800",
                    "powerup": "1200"
                }
                durations = {
                    "bounce": "0.1",
                    "score": "0.3",
                    "powerup": "0.2"
                }
                try:
                    import subprocess
                    subprocess.Popen(["play", "-q", "-n", "synth", 
                                     durations.get(sound_type, "0.1"), 
                                     "sine", frequencies.get(sound_type, "500")])
                except:
                    pass  # Silently fail if play command not available
        except:
            pass  # Silently fail if sound playback fails