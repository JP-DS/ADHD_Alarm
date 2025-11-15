class FocusAlarm {
    constructor() {
        this.isRunning = false;
        this.remainingTime = 0;
        this.totalTime = 0;
        this.timerInterval = null;
        this.soundInterval = null;
        this.audioContext = null;
        this.currentSound = 'Default Beep';
        
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
        const hours = parseInt(document.getElementById('hours').value) || 0;
        const minutes = parseInt(document.getElementById('minutes').value) || 0;
        const seconds = parseInt(document.getElementById('seconds').value) || 0;
        
        this.totalTime = hours * 3600 + minutes * 60 + seconds;
        
        if (this.totalTime <= 0) {
            alert('Please set a valid time duration');
            return;
        }
        
        this.remainingTime = this.totalTime;
        this.isRunning = true;
        
        // Update UI
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        document.getElementById('status').textContent = 'Focus session in progress...';
        
        // Start timer
        this.timerInterval = setInterval(() => this.updateTimer(), 1000);
        
        // Start sound loop
        this.startSoundLoop();
        
        // Play start sound immediately
        this.playSound();
    }
    
    stopTimer() {
        this.isRunning = false;
        this.remainingTime = 0;
        
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
    }
    
    updateTimer() {
        if (!this.isRunning || this.remainingTime <= 0) {
            this.sessionComplete();
            return;
        }
        
        const hours = Math.floor(this.remainingTime / 3600);
        const minutes = Math.floor((this.remainingTime % 3600) / 60);
        const seconds = this.remainingTime % 60;
        
        const timeStr = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        document.getElementById('timerDisplay').textContent = timeStr;
        
        const progress = ((this.totalTime - this.remainingTime) / this.totalTime) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
        
        this.remainingTime--;
    }
    
    startSoundLoop() {
        // Play sound at random intervals (3-5 minutes)
        const playNextSound = () => {
            if (!this.isRunning) return;
            
            // Random interval between 3-5 minutes (180-300 seconds)
            const interval = Math.random() * (300 - 180) + 180;
            
            setTimeout(() => {
                if (this.isRunning && this.remainingTime > 0) {
                    this.playSound();
                    playNextSound(); // Schedule next sound
                }
            }, interval * 1000);
        };
        
        playNextSound();
    }
    
    testSound() {
        this.playSound();
    }
    
    playSound() {
        if (!this.audioContext) {
            // Try to resume audio context (browsers require user interaction)
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        
        // Resume audio context if suspended (required by some browsers)
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
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
            'Default Beep': () => this.createBeep(800, 0.5),
            'iPhone Radar': () => this.createRadar(),
            'iPhone Beacon': () => this.createBeacon(),
            'iPhone Bulletin': () => this.createBulletin(),
            'iPhone Signal': () => this.createSignal(),
            'iPhone Hillside': () => this.createHillside(),
            'iPhone Playtime': () => this.createPlaytime(),
            'iPhone Sencha': () => this.createSencha()
        };
        
        return sounds[soundName] || sounds['Default Beep'];
    }
    
    createBeep(frequency, duration) {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = 'sine';
        
        const now = this.audioContext.currentTime;
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.3, now + 0.1);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    createRadar() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        
        const now = this.audioContext.currentTime;
        const duration = 0.8;
        
        // Frequency sweep (ascending)
        oscillator.frequency.setValueAtTime(800, now);
        oscillator.frequency.exponentialRampToValueAtTime(1200, now + duration);
        
        // Gain envelope with echo effect
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.3, now + 0.1);
        gainNode.gain.linearRampToValueAtTime(0.2, now + 0.4);
        gainNode.gain.linearRampToValueAtTime(0.1, now + 0.6);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    createBeacon() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        const lfo = this.audioContext.createOscillator();
        const lfoGain = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        lfo.connect(lfoGain);
        lfoGain.connect(gainNode.gain);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 600;
        lfo.type = 'sine';
        lfo.frequency.value = 2; // 2 Hz pulse
        lfoGain.gain.value = 0.3;
        
        const now = this.audioContext.currentTime;
        const duration = 1.2;
        
        gainNode.gain.setValueAtTime(0.4, now);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        lfo.start(now);
        oscillator.stop(now + duration);
        lfo.stop(now + duration);
    }
    
    createBulletin() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 1000;
        
        const now = this.audioContext.currentTime;
        const duration = 1.0;
        
        // Sharp attack and decay
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.4, now + 0.05);
        gainNode.gain.linearRampToValueAtTime(0.3, now + 0.2);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }
    
    createSignal() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        const lfo = this.audioContext.createOscillator();
        const lfoGain = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        lfo.connect(lfoGain);
        lfoGain.connect(oscillator.frequency);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 1200;
        lfo.type = 'sine';
        lfo.frequency.value = 4; // 4 Hz FM
        lfoGain.gain.value = 50; // FM depth
        
        const now = this.audioContext.currentTime;
        const duration = 0.6;
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.3, now + 0.1);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        lfo.start(now);
        oscillator.stop(now + duration);
        lfo.stop(now + duration);
    }
    
    createHillside() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        const lfo = this.audioContext.createOscillator();
        const lfoGain = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        lfo.connect(lfoGain);
        lfoGain.connect(oscillator.frequency);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 400;
        lfo.type = 'sine';
        lfo.frequency.value = 6; // 6 Hz vibrato
        lfoGain.gain.value = 20; // Vibrato depth
        
        const now = this.audioContext.currentTime;
        const duration = 1.5;
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.3, now + 0.3);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        lfo.start(now);
        oscillator.stop(now + duration);
        lfo.stop(now + duration);
    }
    
    createPlaytime() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        const lfo = this.audioContext.createOscillator();
        const lfoGain = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        lfo.connect(lfoGain);
        lfoGain.connect(gainNode.gain);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 800;
        lfo.type = 'sine';
        lfo.frequency.value = 12; // 12 Hz modulation
        lfoGain.gain.value = 0.2;
        
        const now = this.audioContext.currentTime;
        const duration = 0.8;
        
        gainNode.gain.setValueAtTime(0.3, now);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        lfo.start(now);
        oscillator.stop(now + duration);
        lfo.stop(now + duration);
    }
    
    createSencha() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        const lfo = this.audioContext.createOscillator();
        const lfoGain = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        lfo.connect(lfoGain);
        lfoGain.connect(oscillator.frequency);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 300;
        lfo.type = 'sine';
        lfo.frequency.value = 2; // 2 Hz vibrato
        lfoGain.gain.value = 10; // Vibrato depth
        
        const now = this.audioContext.currentTime;
        const duration = 2.0;
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.25, now + 0.4);
        gainNode.gain.linearRampToValueAtTime(0, now + duration);
        
        oscillator.start(now);
        lfo.start(now);
        oscillator.stop(now + duration);
        lfo.stop(now + duration);
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
        
        setTimeout(() => {
            alert('Great job! Your focus session is complete.');
        }, 2000);
    }
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', () => {
    new FocusAlarm();
});


