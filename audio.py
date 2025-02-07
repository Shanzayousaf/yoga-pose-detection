import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

class BeepSoundManager:
    def __init__(self, sound_file="beep.wav"):
        """Initialize the BeepSoundManager and load the beep sound."""
        self.beep_sound = None
        try:
            self.beep_sound = pygame.mixer.Sound(sound_file)
            print(f"Sound file '{sound_file}' loaded successfully.")
        except pygame.error as e:
            print(f"Error loading sound file: {e}")

    def play_beep(self):
        """Play the beep sound."""
        if self.beep_sound:
            try:
                self.beep_sound.play()
                print("Beep sound played.")
            except Exception as e:
                print(f"Error playing beep sound: {e}")
        else:
            print("No sound file loaded.")

    def set_volume(self, volume):
        """Set the volume of the beep sound.
        
        Args:
            volume (float): Volume level between 0.0 (mute) and 1.0 (max volume).
        """
        if self.beep_sound:
            try:
                self.beep_sound.set_volume(volume)
                print(f"Volume set to {volume}.")
            except Exception as e:
                print(f"Error setting volume: {e}")
        else:
            print("No sound file loaded.")

    def stop_beep(self):
        """Stop the beep sound if it's playing."""
        if self.beep_sound:
            try:
                self.beep_sound.stop()
                print("Beep sound stopped.")
            except Exception as e:
                print(f"Error stopping beep sound: {e}")
        else:
            print("No sound file loaded.")

# Example usage
if __name__ == "__main__":
    sound_manager = BeepSoundManager("beep.wav")
    sound_manager.set_volume(0.5)
    sound_manager.play_beep()
    # Let the sound play for a while
    pygame.time.wait(2000)  # Wait for 2 seconds
    sound_manager.stop_beep()