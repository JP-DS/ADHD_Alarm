# Focus Alarm App

A local alarm application designed to help you maintain focus during work or study sessions. The app features a countdown timer with random sound intervals to keep you alert and engaged.

## Features

- **Customizable Timer**: Set any duration from seconds to hours
- **Random Sound Intervals**: Sounds play at random intervals between 3-5 minutes (uniformly distributed)
- **8 iPhone-style Sounds**: Choose from 8 built-in sound options including beeps, chimes, bells, and gongs
- **Visual Progress**: Real-time countdown display with progress bar
- **Clean Interface**: Modern, distraction-free UI
- **Session Management**: Start, stop, and track your focus sessions

## Quick Start

### Web Version (Recommended for Public Website)

**Run locally:**
```bash
pip install flask
python app.py
```
Then open `http://localhost:5000` in your browser.

**Deploy to production:**
- Deploy to any platform that supports Flask (Heroku, Railway, Render, etc.)
- Or use static hosting (Netlify, Vercel) by serving the `static` and `templates` folders

### Standalone App (macOS)

**For macOS users:**
1. Download the `Focus Alarm` executable from the `dist` folder
2. Double-click to run (no installation required)
3. If you get a security warning, go to System Preferences > Security & Privacy and click "Open Anyway"

## Installation (Development)

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Desktop Application**:
   ```bash
   python focus_alarm.py
   ```

3. **Run the Web Application**:
   ```bash
   python app.py
   ```
   Then open `http://localhost:5000` in your browser.

## Usage

1. **Set Timer Duration**:
   - Use the spinboxes to set hours, minutes, and seconds
   - Default is set to 25 minutes (Pomodoro technique)

2. **Choose Your Sound**:
   - Use the dropdown menu to select from 8 built-in sound options:
     - Default Beep
     - iPhone Radar
     - iPhone Beacon
     - iPhone Bulletin
     - iPhone Signal
     - iPhone Hillside
     - iPhone Playtime
     - iPhone Sencha
   - Click "Test Sound" to preview your selection

3. **Start Focus Session**:
   - Click "Start Focus Session" to begin
   - The timer will count down and sounds will play at random intervals

4. **Monitor Progress**:
   - Watch the countdown timer and progress bar
   - Status updates show current session state

5. **Stop or Complete**:
   - Click "Stop" to end the session early
   - When the timer reaches zero, you'll hear 3 beeps and see a completion message

## How It Works

- **Timer**: Counts down from your set duration in real-time
- **Random Sounds**: Every 3-5 minutes (randomly distributed), your chosen sound will play
- **Threading**: Uses separate threads for timer and sound management to prevent UI freezing
- **Sound Generation**: Creates iPhone-style alarm sounds using mathematical algorithms

## System Requirements

- **Standalone App**: macOS 10.13 or later (no Python required)
- **Development**: Python 3.7 or higher, macOS, Windows, or Linux
- Audio output capability

## Troubleshooting

- **No Sound**: The app will fall back to system beep if pygame audio fails
- **UI Issues**: Make sure you have tkinter installed (usually comes with Python)
- **Dependencies**: Run `pip install -r requirements.txt` if you encounter import errors
- **Security Warning**: On macOS, you may need to allow the app in Security & Privacy settings

## Customization

You can modify the sound intervals by changing the values in the `sound_loop()` method:
```python
# Random interval between 3-5 minutes (180-300 seconds)
interval = random.uniform(180, 300)
```

## Web Deployment

### Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: python app.py
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Deploy to Railway/Render

1. Connect your repository
2. Set start command: `python app.py`
3. Deploy automatically

### Deploy as Static Site (Netlify/Vercel)

The web app can also be served as a static site. You'll need to modify `app.js` to remove Flask template syntax and serve files directly.

## Building the Standalone App

To create your own executable:
```bash
pip install pyinstaller
pyinstaller focus_alarm.spec
```

The executable will be created in the `dist` folder.

## License

This project is open source and available under the MIT License.
