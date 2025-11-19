# Focus Alarm ⏰

A minimalist focus timer with random interval alarms to help you stay on task. Perfect for ADHD, Pomodoro technique, or any focused work session.

## ✨ Features

- **Custom Timer**: Set hours, minutes, and seconds
- **Random Sound Intervals**: Alerts play every 3-5 minutes (uniformly distributed)
- **8 iPhone-Style Sounds**: Radar, Beacon, Signal, and more
- **Visual Progress**: Clean progress bar and countdown display
- **Always Active**: Works in background tabs and when screen dims
- **No Backend Required**: Runs 100% in your browser using Web Audio API

## 🚀 Live Demo

Visit: [Your Render URL]

## 🎯 How It Works

1. Set your focus session duration
2. Choose your preferred alert sound
3. Click "Start Focus Session"
4. Stay focused! Random alarms will remind you to check in every 3-5 minutes
5. Complete your session with a celebration sound

## 🛠️ Technology

- **Pure HTML/CSS/JavaScript** - No frameworks needed
- **Web Audio API** - Generates sounds in real-time
- **Real-time tracking** - Uses timestamps for accurate timing even in background
- **Static hosting** - Deployed on Render (or any static host)

## 📱 Works Everywhere

- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)
- ✅ Background tabs (timer continues accurately)
- ✅ Dimmed screens (sounds still play)
- ✅ Offline capable (after first load)

## 🔧 Local Development

```bash
# Clone the repo
git clone https://github.com/JP-DS/ADHD_Alarm.git
cd ADHD_Alarm

# Open directly in browser
open index.html

# Or use a local server
python3 -m http.server 8000
# Visit: http://localhost:8000
```

## 📦 Deployment

### Render (Current)
Already deployed! Just push changes to main branch.

### Vercel
```bash
vercel --prod
```

### Netlify
```bash
netlify deploy --prod
```

### GitHub Pages
Push to `gh-pages` branch or enable in repo settings.

## 🎨 Customization

- **Sounds**: Edit sound functions in `js/app.js`
- **Styling**: Modify colors/fonts in `css/style.css`
- **Intervals**: Change min/max duration in `startSoundLoop()` function

## 📝 License

Free to use and modify!

---

Built with ❤️ for focus and productivity
