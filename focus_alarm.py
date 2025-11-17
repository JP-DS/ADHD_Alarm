import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
import pygame
import os
import numpy as np
import wave
from datetime import datetime, timedelta
import sys
import subprocess

# Better error handling for standalone executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    import os
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

class FocusAlarm:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Alarm")
        self.root.geometry("400x500")
        self.root.configure(bg='#2c3e50')
        
        # Initialize pygame mixer for sounds
        self.audio_working = False
        
        # Check if we're running as a frozen app (double-clicked)
        if getattr(sys, 'frozen', False):
            print("Running as frozen app - may need audio permissions")
            # Try to request audio permissions first
            try:
                # Test system audio access
                subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                             capture_output=True, timeout=2)
                print("System audio access confirmed")
            except:
                print("System audio access failed - will use fallbacks")
                
            # Try to request audio permissions more directly
            try:
                # Force audio initialization by playing a silent sound
                subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                             capture_output=True, timeout=3)
                print("Audio permission test successful")
            except Exception as e:
                print(f"Audio permission test failed: {e}")
                # Try alternative approach
                try:
                    os.system('afplay /System/Library/Sounds/Glass.aiff &')
                    print("Audio permission test via os.system successful")
                except:
                    print("All audio permission tests failed")
        
        try:
            # Try multiple audio initialization methods
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            print("Pygame mixer initialized successfully")
            self.audio_working = True
        except Exception as e:
            print(f"Error initializing pygame mixer: {e}")
            # Try alternative initialization
            try:
                pygame.mixer.init()
                print("Pygame mixer initialized with defaults")
                self.audio_working = True
            except Exception as e2:
                print(f"Failed to initialize pygame mixer: {e2}")
                # Try with minimal settings
                try:
                    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=256)
                    print("Pygame mixer initialized with minimal settings")
                    self.audio_working = True
                except Exception as e3:
                    print(f"Failed to initialize pygame mixer: {e3}")
                    # Try with even more minimal settings for frozen apps
                    try:
                        pygame.mixer.quit()  # Ensure clean state
                        pygame.mixer.init(frequency=11025, size=-16, channels=1, buffer=128)
                        print("Pygame mixer initialized with ultra-minimal settings")
                        self.audio_working = True
                    except Exception as e4:
                        print(f"All pygame mixer initialization failed: {e4}")
                        self.audio_working = False
                    
        # If pygame failed, try to initialize system audio
        if not self.audio_working:
            print("Pygame failed - will use system audio fallbacks")
            # Test system audio
            try:
                subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                             capture_output=True, timeout=1)
                print("System audio working as fallback")
            except Exception as e:
                print(f"System audio also failed: {e}")
        
        # Timer variables
        self.is_running = False
        self.remaining_time = 0
        self.total_time = 0
        self.sound_thread = None
        self.timer_thread = None
        
        # Sound options
        self.sound_options = {
            "Default Beep": None,
            "iPhone Radar": None,
            "iPhone Beacon": None,
            "iPhone Bulletin": None,
            "iPhone Signal": None,
            "iPhone Hillside": None,
            "iPhone Playtime": None,
            "iPhone Sencha": None
        }
        self.current_sound = "Default Beep"
        self.custom_sound = None
        self.custom_sound_name = None
        
        # Create all sound options
        self.create_all_sounds()
        
        self.setup_ui()
        
        # Update audio status display
        self.update_audio_status()
        
    def reinitialize_audio(self):
        """Try to reinitialize audio system"""
        try:
            pygame.mixer.quit()
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.audio_working = True
            print("Audio reinitialized successfully")
            
            # Update UI
            self.audio_status_label.config(text="Audio: Working (Pygame)", fg='#27ae60')
            
        except Exception as e:
            print(f"Failed to reinitialize audio: {e}")
            # Try alternative settings
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=256)
                self.audio_working = True
                print("Audio reinitialized with alternative settings")
                self.audio_status_label.config(text="Audio: Working (Pygame)", fg='#27ae60')
            except Exception as e2:
                print(f"Alternative audio initialization also failed: {e2}")
                self.audio_working = False
                self.audio_status_label.config(text="Audio: Not Working", fg='#e74c3c')
    
    def update_audio_status(self):
        """Update the audio status display"""
        if self.audio_working:
            self.audio_status_label.config(text="Audio: Working (Pygame)", fg='#27ae60')
        else:
            # Check if system audio works as fallback
            try:
                subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                             capture_output=True, timeout=1)
                self.audio_status_label.config(text="Audio: Working (System)", fg='#f39c12')
            except:
                self.audio_status_label.config(text="Audio: Not Working", fg='#e74c3c')
    
    def test_system_sound(self):
        """Test macOS system sound directly"""
        try:
            subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                         capture_output=True, timeout=1)
            print("System sound played successfully")
        except Exception as e:
            print(f"System sound failed: {e}")
            print('\a')  # Fallback to terminal beep
    
    def get_system_sound_path(self):
        """Get a system sound path based on the selected sound type"""
        # Map sound types to specific system sounds
        sound_mapping = {
            "Default Beep": '/System/Library/Sounds/Glass.aiff',
            "iPhone Radar": '/System/Library/Sounds/Ping.aiff',
            "iPhone Beacon": '/System/Library/Sounds/Pop.aiff',
            "iPhone Bulletin": '/System/Library/Sounds/Tink.aiff',
            "iPhone Signal": '/System/Library/Sounds/Basso.aiff',
            "iPhone Hillside": '/System/Library/Sounds/Blow.aiff',
            "iPhone Playtime": '/System/Library/Sounds/Frog.aiff',
            "iPhone Sencha": '/System/Library/Sounds/Funk.aiff'
        }
        
        # Get the sound for the currently selected type
        selected_sound = sound_mapping.get(self.current_sound, '/System/Library/Sounds/Glass.aiff')
        return selected_sound
    
    def play_system_sound_bluetooth(self):
        """Play system sound with better Bluetooth compatibility"""
        try:
            # Try multiple approaches for Bluetooth compatibility
            sound_path = self.get_system_sound_path()
            
            # Method 1: afplay with longer timeout
            try:
                subprocess.run(['afplay', sound_path], 
                             capture_output=True, timeout=3)
                print(f"Played system sound via afplay: {os.path.basename(sound_path)}")
                return True
            except subprocess.TimeoutExpired:
                print("afplay timed out, trying alternative method")
            
            # Method 2: os.system (more reliable with Bluetooth)
            try:
                os.system(f'afplay "{sound_path}" &')
                print(f"Played system sound via os.system: {os.path.basename(sound_path)}")
                return True
            except:
                print("os.system failed")
            
            # Method 3: Use pygame if available
            if self.audio_working:
                try:
                    # Create a simple beep sound
                    sample_rate = 44100
                    duration = 0.5
                    t = np.linspace(0, duration, int(sample_rate * duration), False)
                    tone = np.sin(2 * np.pi * 800 * t)
                    tone = tone / np.max(np.abs(tone)) * 16383
                    tone = tone.astype(np.int16)
                    
                    temp_filename = 'temp_bluetooth_beep.wav'
                    with wave.open(temp_filename, 'w') as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2)
                        wav_file.setframerate(sample_rate)
                        wav_file.writeframes(tone.tobytes())
                    
                    sound = pygame.mixer.Sound(temp_filename)
                    sound.play()
                    print("Played pygame beep for Bluetooth")
                    return True
                except:
                    print("pygame beep failed")
            
            # Final fallback
            print('\a')  # Terminal beep
            return False
            
        except Exception as e:
            print(f"All Bluetooth audio methods failed: {e}")
            print('\a')  # Terminal beep
            return False
        
    def create_all_sounds(self):
        """Create all 8 sound options"""
        try:
            sample_rate = 44100
            
            # 1. Default Beep (simple beep)
            self.sound_options["Default Beep"] = self.create_sound(
                sample_rate, 0.5, [800], [1.0]
            )
            
            # 2. iPhone Radar (classic radar beep)
            self.sound_options["iPhone Radar"] = self.create_iphone_radar(sample_rate)
            
            # 3. iPhone Beacon (gentle beacon sound)
            self.sound_options["iPhone Beacon"] = self.create_iphone_beacon(sample_rate)
            
            # 4. iPhone Bulletin (news bulletin style)
            self.sound_options["iPhone Bulletin"] = self.create_iphone_bulletin(sample_rate)
            
            # 5. iPhone Signal (signal tone)
            self.sound_options["iPhone Signal"] = self.create_iphone_signal(sample_rate)
            
            # 6. iPhone Hillside (nature-inspired)
            self.sound_options["iPhone Hillside"] = self.create_iphone_hillside(sample_rate)
            
            # 7. iPhone Playtime (playful tone)
            self.sound_options["iPhone Playtime"] = self.create_iphone_playtime(sample_rate)
            
            # 8. iPhone Sencha (calm, zen-like)
            self.sound_options["iPhone Sencha"] = self.create_iphone_sencha(sample_rate)
            
        except Exception as e:
            print(f"Error creating sounds: {e}")
            # Fallback: set all to None for system beep
            for key in self.sound_options:
                self.sound_options[key] = None
    
    def create_sound(self, sample_rate, duration, frequencies, amplitudes):
        """Create a sound with multiple frequencies"""
        try:
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Mix multiple frequencies
            tone = np.zeros_like(t)
            for freq, amp in zip(frequencies, amplitudes):
                tone += amp * np.sin(2 * np.pi * freq * t)
            
            # Apply fade in/out to avoid clicks
            fade_samples = int(0.1 * sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out
            
            # Normalize and convert to 16-bit integer
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            # Save as temporary WAV file
            temp_filename = f'temp_{frequencies[0]}.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
            
        except Exception as e:
            print(f"Error creating sound: {e}")
            return None
    
    def create_iphone_radar(self, sample_rate):
        """Create iPhone Radar-like sound (classic radar beep)"""
        try:
            duration = 0.8
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Radar: ascending beep with echo
            base_freq = 800
            tone = np.sin(2 * np.pi * base_freq * t)
            
            # Add frequency sweep (ascending)
            sweep = np.linspace(0.8, 1.2, len(t))
            tone *= sweep
            
            # Add echo effect
            echo_delay = int(0.1 * sample_rate)
            echo = np.zeros_like(tone)
            echo[echo_delay:] = tone[:-echo_delay] * 0.3
            
            tone = tone + echo
            
            # Apply fade
            fade_samples = int(0.1 * sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out
            
            # Normalize and convert
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            temp_filename = 'temp_radar.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
        except Exception as e:
            print(f"Error creating iPhone Radar: {e}")
            return None
    
    def create_iphone_beacon(self, sample_rate):
        """Create iPhone Beacon-like sound (gentle beacon)"""
        try:
            duration = 1.2
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Beacon: gentle pulsing tone
            base_freq = 600
            tone = np.sin(2 * np.pi * base_freq * t)
            
            # Add gentle pulse modulation
            pulse_freq = 2  # 2 Hz pulse
            pulse = 0.7 + 0.3 * np.sin(2 * np.pi * pulse_freq * t)
            tone *= pulse
            
            # Add harmonics for warmth
            tone += 0.3 * np.sin(2 * np.pi * base_freq * 1.5 * t)
            tone += 0.2 * np.sin(2 * np.pi * base_freq * 2 * t)
            
            # Apply fade
            fade_samples = int(0.2 * sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out
            
            # Normalize and convert
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            temp_filename = 'temp_beacon.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
        except Exception as e:
            print(f"Error creating iPhone Beacon: {e}")
            return None
    
    def create_iphone_bulletin(self, sample_rate):
        """Create iPhone Bulletin-like sound (news bulletin style)"""
        try:
            duration = 1.0
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Bulletin: attention-grabbing tone
            base_freq = 1000
            tone = np.sin(2 * np.pi * base_freq * t)
            
            # Add sharp attack and decay
            attack_samples = int(0.05 * sample_rate)
            decay_samples = int(0.1 * sample_rate)
            
            attack = np.linspace(0, 1, attack_samples)
            decay = np.linspace(1, 0.3, decay_samples)
            
            tone[:attack_samples] *= attack
            tone[-decay_samples:] *= decay
            
            # Add slight modulation
            mod_freq = 8  # 8 Hz modulation
            modulation = 0.9 + 0.1 * np.sin(2 * np.pi * mod_freq * t)
            tone *= modulation
            
            # Normalize and convert
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            temp_filename = 'temp_bulletin.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
        except Exception as e:
            print(f"Error creating iPhone Bulletin: {e}")
            return None
    
    def create_iphone_signal(self, sample_rate):
        """Create iPhone Signal-like sound (signal tone)"""
        try:
            duration = 0.6
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Signal: clean, electronic tone
            base_freq = 1200
            tone = np.sin(2 * np.pi * base_freq * t)
            
            # Add slight frequency modulation
            fm_freq = 4  # 4 Hz FM
            fm_depth = 50  # Hz
            fm = fm_depth * np.sin(2 * np.pi * fm_freq * t)
            tone = np.sin(2 * np.pi * (base_freq + fm) * t)
            
            # Add harmonics for clarity
            tone += 0.2 * np.sin(2 * np.pi * base_freq * 2 * t)
            
            # Apply fade
            fade_samples = int(0.1 * sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out
            
            # Normalize and convert
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            temp_filename = 'temp_signal.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
        except Exception as e:
            print(f"Error creating iPhone Signal: {e}")
            return None
    
    def create_iphone_hillside(self, sample_rate):
        """Create iPhone Hillside-like sound (nature-inspired)"""
        try:
            duration = 1.5
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Hillside: nature-inspired, gentle
            base_freq = 400
            tone = np.sin(2 * np.pi * base_freq * t)
            
            # Add natural harmonics
            tone += 0.4 * np.sin(2 * np.pi * base_freq * 1.5 * t)
            tone += 0.3 * np.sin(2 * np.pi * base_freq * 2.5 * t)
            tone += 0.2 * np.sin(2 * np.pi * base_freq * 3.5 * t)
            
            # Add gentle vibrato
            vibrato_freq = 6  # 6 Hz vibrato
            vibrato_depth = 20  # Hz
            vibrato = vibrato_depth * np.sin(2 * np.pi * vibrato_freq * t)
            tone = np.sin(2 * np.pi * (base_freq + vibrato) * t)
            
            # Apply long fade
            fade_samples = int(0.3 * sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out
            
            # Normalize and convert
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            temp_filename = 'temp_hillside.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
        except Exception as e:
            print(f"Error creating iPhone Hillside: {e}")
            return None
    
    def create_iphone_playtime(self, sample_rate):
        """Create iPhone Playtime-like sound (playful tone)"""
        try:
            duration = 0.8
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Playtime: playful, bouncy tone
            base_freq = 800
            tone = np.sin(2 * np.pi * base_freq * t)
            
            # Add playful modulation
            mod_freq = 12  # 12 Hz modulation
            modulation = 0.8 + 0.2 * np.sin(2 * np.pi * mod_freq * t)
            tone *= modulation
            
            # Add harmonics for brightness
            tone += 0.3 * np.sin(2 * np.pi * base_freq * 1.25 * t)
            tone += 0.2 * np.sin(2 * np.pi * base_freq * 1.75 * t)
            
            # Add slight pitch bend
            bend = np.linspace(1.0, 1.1, len(t))
            tone = np.sin(2 * np.pi * base_freq * bend * t)
            
            # Apply fade
            fade_samples = int(0.1 * sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out
            
            # Normalize and convert
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            temp_filename = 'temp_playtime.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
        except Exception as e:
            print(f"Error creating iPhone Playtime: {e}")
            return None
    
    def create_iphone_sencha(self, sample_rate):
        """Create iPhone Sencha-like sound (calm, zen-like)"""
        try:
            duration = 2.0
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Sencha: calm, zen-like tone
            base_freq = 300
            tone = np.sin(2 * np.pi * base_freq * t)
            
            # Add very gentle harmonics
            tone += 0.2 * np.sin(2 * np.pi * base_freq * 2 * t)
            tone += 0.1 * np.sin(2 * np.pi * base_freq * 3 * t)
            
            # Add very slow vibrato
            vibrato_freq = 2  # 2 Hz vibrato
            vibrato_depth = 10  # Hz
            vibrato = vibrato_depth * np.sin(2 * np.pi * vibrato_freq * t)
            tone = np.sin(2 * np.pi * (base_freq + vibrato) * t)
            
            # Apply very long fade
            fade_samples = int(0.4 * sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out
            
            # Normalize and convert
            tone = tone / np.max(np.abs(tone)) * 16383
            tone = tone.astype(np.int16)
            
            temp_filename = 'temp_sencha.wav'
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
            
            return pygame.mixer.Sound(temp_filename)
        except Exception as e:
            print(f"Error creating iPhone Sencha: {e}")
            return None
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Focus Alarm", 
            font=('Arial', 24, 'bold'), 
            fg='#ecf0f1', 
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Timer display
        self.time_display = tk.Label(
            main_frame,
            text="00:00:00",
            font=('Arial', 36, 'bold'),
            fg='#3498db',
            bg='#2c3e50'
        )
        self.time_display.pack(pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=300,
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(pady=10)
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Custom.Horizontal.TProgressbar',
            background='#3498db',
            troughcolor='#34495e',
            borderwidth=0,
            lightcolor='#3498db',
            darkcolor='#3498db'
        )
        
        # Time input frame
        input_frame = tk.Frame(main_frame, bg='#2c3e50')
        input_frame.pack(pady=20)
        
        # Hours
        tk.Label(input_frame, text="Hours:", font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50').grid(row=0, column=0, padx=5)
        self.hours_var = tk.StringVar(value="0")
        hours_spinbox = tk.Spinbox(
            input_frame, 
            from_=0, 
            to=24, 
            width=5, 
            textvariable=self.hours_var,
            font=('Arial', 12),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        hours_spinbox.grid(row=0, column=1, padx=5)
        
        # Minutes
        tk.Label(input_frame, text="Minutes:", font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50').grid(row=0, column=2, padx=5)
        self.minutes_var = tk.StringVar(value="25")
        minutes_spinbox = tk.Spinbox(
            input_frame, 
            from_=0, 
            to=59, 
            width=5, 
            textvariable=self.minutes_var,
            font=('Arial', 12),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        minutes_spinbox.grid(row=0, column=3, padx=5)
        
        # Seconds
        tk.Label(input_frame, text="Seconds:", font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50').grid(row=0, column=4, padx=5)
        self.seconds_var = tk.StringVar(value="0")
        seconds_spinbox = tk.Spinbox(
            input_frame, 
            from_=0, 
            to=59, 
            width=5, 
            textvariable=self.seconds_var,
            font=('Arial', 12),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        seconds_spinbox.grid(row=0, column=5, padx=5)
        
        # Sound selection frame
        sound_frame = tk.Frame(main_frame, bg='#2c3e50')
        sound_frame.pack(pady=10, fill=tk.X)
        
        # Sound selection label
        tk.Label(sound_frame, text="Sound:", font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50').pack(anchor=tk.W)
        
        # Audio status indicator
        audio_status_color = '#27ae60' if self.audio_working else '#e74c3c'
        audio_status_text = "Audio: Working" if self.audio_working else "Audio: Not Working"
        self.audio_status_label = tk.Label(
            sound_frame, 
            text=audio_status_text, 
            font=('Arial', 10), 
            fg=audio_status_color, 
            bg='#2c3e50'
        )
        self.audio_status_label.pack(anchor=tk.W)
        
        # Sound dropdown
        self.sound_var = tk.StringVar(value="Default Beep")
        sound_dropdown = ttk.Combobox(
            sound_frame,
            textvariable=self.sound_var,
            values=list(self.sound_options.keys()),
            state="readonly",
            font=('Arial', 12),
            width=20
        )
        sound_dropdown.pack(pady=5, fill=tk.X)
        sound_dropdown.bind('<<ComboboxSelected>>', self.on_sound_change)
        
        # Test sound button
        self.test_sound_button = tk.Button(
            sound_frame,
            text="Test Sound",
            command=self.test_current_sound,
            font=('Arial', 10),
            bg='#f39c12',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.test_sound_button.pack(pady=5)
        
        # Fix Audio button (for .app issues)
        self.fix_audio_button = tk.Button(
            sound_frame,
            text="Fix Audio",
            command=self.reinitialize_audio,
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.fix_audio_button.pack(pady=5)
        
        # Test System Sound button
        self.test_system_button = tk.Button(
            sound_frame,
            text="Test System Sound",
            command=self.test_system_sound,
            font=('Arial', 10),
            bg='#e67e22',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.test_system_button.pack(pady=5)
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="Start Focus Session",
            command=self.start_timer,
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_timer,
            font=('Arial', 14, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to start your focus session",
            font=('Arial', 12),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        self.status_label.pack(pady=10)
        
        # Info frame
        info_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=20)
        
        info_text = """
Focus Alarm Features:
• Set custom timer duration
• Random sound intervals (3-5 minutes)
• 8 iPhone-style alarm sounds
• Test sound feature
• Visual progress indicator
• Clean, distraction-free interface
        """
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#34495e',
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        info_label.pack()
        
    def start_timer(self):
        """Start the focus timer"""
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            
            self.total_time = hours * 3600 + minutes * 60 + seconds
            
            if self.total_time <= 0:
                messagebox.showerror("Error", "Please set a valid time duration")
                return
                
            self.remaining_time = self.total_time
            self.is_running = True
            
            # Update UI
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Focus session in progress...")
            
            # Start timer thread
            self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
            self.timer_thread.start()
            
            # Start sound thread
            self.sound_thread = threading.Thread(target=self.sound_loop, daemon=True)
            self.sound_thread.start()
            
            # Play start sound immediately
            print("Timer started - playing start sound")
            self.play_sound()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for time")
    
    def stop_timer(self):
        """Stop the focus timer"""
        self.is_running = False
        self.remaining_time = 0
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Session stopped")
        self.time_display.config(text="00:00:00")
        self.progress_var.set(0)
    
    def timer_loop(self):
        """Main timer loop"""
        while self.is_running and self.remaining_time > 0:
            # Update display
            hours = self.remaining_time // 3600
            minutes = (self.remaining_time % 3600) // 60
            seconds = self.remaining_time % 60
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Update progress
            progress = ((self.total_time - self.remaining_time) / self.total_time) * 100
            
            # Update UI in main thread
            self.root.after(0, self.update_display, time_str, progress)
            
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.remaining_time <= 0:
            self.root.after(0, self.session_complete)
    
    def sound_loop(self):
        """Sound loop with random intervals"""
        print("Sound loop started - will play sounds every 3-5 minutes")
        
        while self.is_running and self.remaining_time > 0:
            # Random interval between 3-5 minutes (180-300 seconds)
            interval = random.uniform(180, 300)
            print(f"Next sound in {interval/60:.1f} minutes")
            
            # Wait for the interval or until timer stops
            start_time = time.time()
            while self.is_running and self.remaining_time > 0 and (time.time() - start_time) < interval:
                time.sleep(1)
            
            # Play sound if timer is still running
            if self.is_running and self.remaining_time > 0:
                print("Playing interval sound...")
                self.play_sound()
    
    def on_sound_change(self, event=None):
        """Handle sound selection change"""
        self.current_sound = self.sound_var.get()
        print(f"Sound changed to: {self.current_sound}")
    
    def test_current_sound(self):
        """Test the currently selected sound"""
        try:
            # Always use system sounds since pygame isn't working reliably
            self.play_system_sound_bluetooth()
            print(f"Playing system sound for: {self.current_sound}")
        except Exception as e:
            print(f"Error testing sound: {e}")
            print('\a')
    
    def play_sound(self):
        """Play the selected sound"""
        try:
            # Always use system sounds since pygame isn't working reliably
            self.play_system_sound_bluetooth()
        except Exception as e:
            # Final fallback
            print(f"Sound error: {e}")
            print('\a')
    
    def update_display(self, time_str, progress):
        """Update the display in the main thread"""
        self.time_display.config(text=time_str)
        self.progress_var.set(progress)
    
    def session_complete(self):
        """Handle session completion"""
        self.is_running = False
        
        # Play final sound
        for _ in range(3):
            self.play_sound()
            time.sleep(0.5)
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Focus session completed!")
        
        # Show completion message
        messagebox.showinfo("Session Complete", "Great job! Your focus session is complete.")
    
    def on_closing(self):
        """Handle window closing"""
        self.is_running = False
        
        # Clean up temporary sound files
        temp_files = [
            'temp_800.wav', 'temp_radar.wav', 'temp_beacon.wav', 'temp_bulletin.wav',
            'temp_signal.wav', 'temp_hillside.wav', 'temp_playtime.wav', 'temp_sencha.wav'
        ]
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
        
        self.root.destroy()

def main():
    try:
        root = tk.Tk()
        app = FocusAlarm(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        # Show error in a message box if GUI is available
        try:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", f"Failed to start Focus Alarm: {str(e)}")
        except:
            # If GUI is not available, print to console
            print(f"Error starting Focus Alarm: {e}")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
