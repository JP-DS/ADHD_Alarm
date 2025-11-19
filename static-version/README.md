# Focus Alarm - Static Version

A fully static focus timer with random interval alarms. No backend needed!

## ✨ Features

- Custom timer duration (hours, minutes, seconds)
- Random sound intervals (3-5 minutes)
- 8 iPhone-style alarm sounds
- Visual progress indicator
- Works completely offline
- No server required

## 🚀 Deployment Options

### Option 1: Add to Your Next.js Site (jiaran.net/alarm)

1. **Copy files to your Next.js project:**
   ```bash
   cp -r static-version/* /path/to/jiaran.net/public/alarm/
   ```

2. **Access at:** `https://jiaran.net/alarm/`

That's it! Next.js automatically serves files from the `public` folder.

---

### Option 2: Deploy to Vercel as Separate Site

1. **Create a new GitHub repo** (or push to existing)
   ```bash
   cd static-version
   git init
   git add .
   git commit -m "Initial commit: Focus Alarm static site"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repo
   - Deploy (takes 30 seconds)
   - Done! Gets a URL like `alarm.vercel.app`

3. **Add custom domain:**
   - In Vercel project settings → Domains
   - Add `alarm.jiaran.net`
   - Update DNS: `alarm` CNAME → `cname.vercel-dns.com`

---

### Option 3: GitHub Pages (Free)

1. **Push to GitHub:**
   ```bash
   cd static-version
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Repo Settings → Pages
   - Source: main branch / root
   - Save

3. **Access at:** `https://yourusername.github.io/repo-name/`

---

### Option 4: Netlify Drop

1. Go to https://app.netlify.com/drop
2. Drag the `static-version` folder
3. Done! Gets instant URL

---

## 🧪 Test Locally

```bash
cd static-version
python3 -m http.server 8000
# Visit: http://localhost:8000
```

Or just double-click `index.html` - works directly in browser!

---

## 📁 File Structure

```
static-version/
├── index.html       # Main page
├── css/
│   └── style.css   # Styling
└── js/
    └── app.js      # Timer & sound logic (Web Audio API)
```

---

## 🎯 Integration with jiaran.net

### Recommended: Add as `/alarm` route

**In your Next.js project:**

```bash
# Copy to public folder
cp -r static-version/* your-nextjs-project/public/alarm/
```

**Link from your portfolio:**

```jsx
// In your projects section or navigation
<a href="/alarm" target="_blank">Focus Alarm Tool</a>

// Or embed in a page
<iframe src="/alarm" width="100%" height="800px" />
```

**Result:** `https://jiaran.net/alarm/` ✅

---

## 💡 Benefits Over Flask Version

| Feature | Flask (Render) | Static |
|---------|---------------|--------|
| Load time | 30s (sleeping) / 1-2s | <1s always |
| 24/7 active | ❌ Sleeps | ✅ Always |
| Cost | $0-$7/month | **$0 forever** |
| Deploy time | 2-3 min | **10 seconds** |
| Works offline | ❌ | ✅ |
| CDN | ❌ | ✅ Global |

---

## 🔧 Customization

All styles are in `css/style.css` - easily customize:
- Colors
- Fonts
- Layout
- Animations

All logic is in `js/app.js`:
- Sound types
- Timer intervals
- Alert behavior

---

## 🎵 How Sounds Work

Uses **Web Audio API** to generate sounds in the browser:
- No audio files needed
- Works offline
- iPhone-style tones (Radar, Beacon, Signal, etc.)
- Resumes automatically after browser idle

---

## 📝 License

Free to use and modify!

---

Built with ❤️ for focus and productivity

