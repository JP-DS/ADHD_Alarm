#!/usr/bin/env python3
"""
Utility script to create a test sound file for the Focus Alarm app.
This creates a pleasant chime sound that users can use as an example.
"""

import numpy as np
import wave
import os

def create_chime_sound():
    """Create a pleasant chime sound"""
    sample_rate = 44100
    duration = 1.0  # seconds
    
    # Create a more pleasant sound with multiple frequencies
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Mix multiple frequencies for a chime-like sound
    tone = (0.4 * np.sin(2 * np.pi * 800 * t) +  # Base frequency
            0.3 * np.sin(2 * np.pi * 1200 * t) +  # Higher harmonic
            0.2 * np.sin(2 * np.pi * 1600 * t) +  # Even higher harmonic
            0.1 * np.sin(2 * np.pi * 2000 * t))   # Highest harmonic
    
    # Apply fade in/out to avoid clicks
    fade_samples = int(0.1 * sample_rate)  # 0.1 second fade
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    tone[:fade_samples] *= fade_in
    tone[-fade_samples:] *= fade_out
    
    # Convert to 16-bit integer
    tone = (tone * 16383).astype(np.int16)  # Reduced volume to avoid clipping
    
    # Save as WAV file
    with wave.open('test_chime.wav', 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(tone.tobytes())
    
    print("Test chime sound created: test_chime.wav")
    print("You can use this file in the Focus Alarm app!")

if __name__ == "__main__":
    create_chime_sound()
