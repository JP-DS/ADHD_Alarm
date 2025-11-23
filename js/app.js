class FocusAlarm {
    constructor() {
        this.isRunning = false;
        this.remainingTime = 0;
        this.totalTime = 0;
        this.timerInterval = null;
        this.soundInterval = null;
        this.audioContext = null;
        this.currentSound = 'Default Beep';
        this.startTime = null;  // Track actual start time
        this.endTime = null;    // Track when timer should end
        this.nextSoundTime = null; // Track next sound time
        
        this.initializeAudio();
        this.setupEventListeners();
    }
    
    initializeAudio() {
        try {
            // Create AudioContext for Web Audio API
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.updateAudioStatus('Audio: Ready', true);
        } catch (e) {
            console.error('Audio initialization failed:', e);
            this.updateAudioStatus('Audio: Not Available', false);
        }
    }
    
    updateAudioStatus(text, isWorking) {
        const statusEl = document.getElementById('audioStatus');
        statusEl.textContent = text;
        statusEl.className = isWorking ? 'audio-status' : 'audio-status error';
    }
    
    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.startTimer());
        document.getElementById('stopBtn').addEventListener('click', () => this.stopTimer());
        document.getElementById('testSoundBtn').addEventListener('click', () => this.testSound());
        document.getElementById('soundSelect').addEventListener('change', (e) => {
            this.currentSound = e.target.value;
        });
    }
    
    startTimer() {
        console.log('Start timer clicked');
        const hours = parseInt(document.getElementById('hours').value) || 0;
        const minutes = parseInt(document.getElementById('minutes').value) || 0;
        
        console.log('Hours:', hours, 'Minutes:', minutes);
        
        this.totalTime = hours * 3600 + minutes * 60;
        
        console.log('Total time:', this.totalTime);
        
        if (this.totalTime <= 0) {
            alert('Please set a valid time duration');
            return;
        }
        
        // Use real timestamps instead of counting
        this.startTime = Date.now();
        this.endTime = this.startTime + (this.totalTime * 1000);
        this.isRunning = true;
        
        // Update UI
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        document.getElementById('status').textContent = 'Focus session in progress...';
        
        // Add 'running' class for minimalist view
        document.querySelector('.card').classList.add('running');
        
        // Start timer with real time tracking
        this.timerInterval = setInterval(() => this.updateTimer(), 1000);
        
        // Start sound loop with real time tracking
        this.startSoundLoop();
        
        // Play start sound immediately
        this.playSound();
    }
    
    stopTimer() {
        this.isRunning = false;
        this.startTime = null;
        this.endTime = null;
        this.nextSoundTime = null;
        
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        
        if (this.soundInterval) {
            clearInterval(this.soundInterval);
            this.soundInterval = null;
        }
        
        // Update UI
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        document.getElementById('status').textContent = 'Session stopped';
        document.getElementById('timerDisplay').textContent = '00:00:00';
        document.getElementById('progressBar').style.width = '0%';
        
        // Remove 'running' class to show controls again
        document.querySelector('.card').classList.remove('running');
    }
    
    updateTimer() {
        if (!this.isRunning) {
            return;
        }
        
        // Calculate remaining time based on real timestamps
        const now = Date.now();
        const remainingMs = this.endTime - now;
        
        if (remainingMs <= 0) {
            this.sessionComplete();
            return;
        }
        
        // Convert to hours, minutes, seconds
        const remainingSeconds = Math.ceil(remainingMs / 1000);
        const hours = Math.floor(remainingSeconds / 3600);
        const minutes = Math.floor((remainingSeconds % 3600) / 60);
        const seconds = remainingSeconds % 60;
        
        const timeStr = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        document.getElementById('timerDisplay').textContent = timeStr;
        
        // Calculate progress based on real time elapsed
        const elapsed = now - this.startTime;
        const progress = (elapsed / (this.totalTime * 1000)) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
    }
    
    startSoundLoop() {
        // Schedule next sound with random interval (3-5 minutes)
        const scheduleNextSound = () => {
            if (!this.isRunning) return;
            
            // Random interval between 3-5 minutes (180-300 seconds)
            const interval = (Math.random() * (300 - 180) + 180) * 1000; // in milliseconds
            this.nextSoundTime = Date.now() + interval;
        };
        
        // Initial sound schedule
        scheduleNextSound();
        
        // Check every second if it's time to play sound (based on real time)
        this.soundInterval = setInterval(() => {
            if (!this.isRunning) return;
            
            const now = Date.now();
            if (this.nextSoundTime && now >= this.nextSoundTime) {
                this.playSound();
                scheduleNextSound(); // Schedule next sound
            }
        }, 1000);
    }
    
    testSound() {
        this.playSound();
    }
    
    async playSound() {
        if (!this.audioContext) {
            // Try to resume audio context (browsers require user interaction)
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        
        // Resume audio context if suspended (required by some browsers)
        // MUST await this or sounds won't play after inactivity
        if (this.audioContext.state === 'suspended') {
            try {
                await this.audioContext.resume();
                this.updateAudioStatus('Audio: Active', true);
            } catch (e) {
                console.error('Failed to resume audio context:', e);
                this.updateAudioStatus('Audio: Suspended', false);
                return;
            }
        }
        
        try {
            const soundFunction = this.getSoundFunction(this.currentSound);
            soundFunction();
        } catch (e) {
            console.error('Error playing sound:', e);
        }
    }
    
    getSoundFunction(soundName) {
        const sounds = {
            'Default Beep': () => this.createDefaultBeep(),
            'Quick Bell': () => this.createQuickBell(),
            'Gentle Ping': () => this.createGentlePing(),
            'Water Drop': () => this.createWaterDrop(),
            'Wind Chime': () => this.createWindChime(),
            'Marimba': () => this.createMarimba(),
            'Calm Ding': () => this.createCalmDing()
        };
        
        return sounds[soundName] || sounds['Default Beep'];
    }
    
    // Default Beep - Original sound from old version
    createDefaultBeep() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        const now = this.audioContext.currentTime;
        const duration = 0.5;
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.3, now + 0.1);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    // Quick Bell - High-pitched, crispy, clean metallic bell tap
    createQuickBell() {
        const now = this.audioContext.currentTime;
        const duration = 0.22; // Even shorter for cleaner sound
        
        // High-pitched metal bell with bright harmonics for crispy, clean sound
        const frequencies = [
            { freq: 1760, gain: 0.28 },  // A6 - high fundamental
            { freq: 2640, gain: 0.20 },  // 1.5x harmonic (brightness)
            { freq: 3520, gain: 0.14 },  // 2x harmonic (crisp high end)
            { freq: 5280, gain: 0.08 }   // 3x harmonic (ultra-crisp shimmer)
        ];
        
        frequencies.forEach(({ freq, gain }) => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.value = freq;
            oscillator.type = 'sine'; // Pure tones for clean metallic quality
            
            // Ultra-sharp attack for maximum crispness
            gainNode.gain.setValueAtTime(0, now);
            gainNode.gain.linearRampToValueAtTime(gain, now + 0.003); // Instant crisp attack
            gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration);
            
            oscillator.start(now);
            oscillator.stop(now + duration);
        });
    }
    
    // Gentle Ping - Soft notification sound
    createGentlePing() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = 880; // A5 note
        oscillator.type = 'sine';
        
        const now = this.audioContext.currentTime;
        const duration = 0.3;
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.15, now + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    // Water Drop - Natural water droplet sound
    createWaterDrop() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        
        const now = this.audioContext.currentTime;
        const duration = 0.4;
        
        // Frequency drops quickly like water
        oscillator.frequency.setValueAtTime(800, now);
        oscillator.frequency.exponentialRampToValueAtTime(400, now + duration);
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.2, now + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    // Wind Chime - Multiple gentle tones
    createWindChime() {
        const notes = [659, 784, 880, 1047]; // E5, G5, A5, C6
        const now = this.audioContext.currentTime;
        
        notes.forEach((freq, i) => {
            const delay = i * 0.08;
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.value = freq;
            oscillator.type = 'triangle';
            
            const startTime = now + delay;
            const duration = 1.2;
            
            gainNode.gain.setValueAtTime(0, startTime);
            gainNode.gain.linearRampToValueAtTime(0.12, startTime + 0.05);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);
            
            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        });
    }
    
    // Marimba - Warm wooden tone
    createMarimba() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = 440; // A4 note
        oscillator.type = 'triangle';
        
        const now = this.audioContext.currentTime;
        const duration = 0.8;
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.25, now + 0.02);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    // Calm Ding - Subtle reminder
    createCalmDing() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = 698; // F5 note
        oscillator.type = 'sine';
        
        const now = this.audioContext.currentTime;
        const duration = 0.6;
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.18, now + 0.03);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    sessionComplete() {
        this.isRunning = false;
        
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        
        // Play completion sound 3 times
        let count = 0;
        const playCompletion = () => {
            if (count < 3) {
                this.playSound();
                count++;
                setTimeout(playCompletion, 500);
            }
        };
        playCompletion();
        
        // Update UI
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        document.getElementById('status').textContent = 'Focus session completed!';
        
        // Remove 'running' class to show controls again
        document.querySelector('.card').classList.remove('running');
        
        setTimeout(() => {
            alert('Great job! Your focus session is complete.');
        }, 2000);
    }
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', () => {
    new FocusAlarm();
});


