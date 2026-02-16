# How to Export YouTube Cookies for yt-dlp

YouTube is blocking automated downloads. You need to export cookies from your browser.

## Method 1: Browser Extension (Easiest - Recommended)

### For Chrome/Edge:
1. Install extension: **"Get cookies.txt LOCALLY"**
   - Chrome: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
   - Edge: Search for same extension in Edge Add-ons

2. Steps:
   - Open Chrome/Edge
   - Go to **youtube.com** and make sure you're logged in
   - Click the extension icon (cookie icon in toolbar)
   - Click **"Export"** button
   - Save as **`cookies.txt`** in the same folder as `102303862.py`
   - Run your script again

### For Firefox:
1. Install extension: **"cookies.txt"**
   - Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/

2. Steps:
   - Open Firefox
   - Go to **youtube.com** and log in
   - Click the extension icon
   - Click **"Export"**
   - Save as **`cookies.txt`** in the same folder as `102303862.py`

## Method 2: Using yt-dlp Command Line

1. Open Command Prompt/Terminal
2. Navigate to your script folder:
   ```bash
   cd "C:\Users\HP\OneDrive\Desktop\UCS654\Assignment7"
   ```
3. Run this command (replace `firefox` with `chrome` or `edge` if needed):
   ```bash
   yt-dlp --cookies-from-browser firefox --print-to-file url "https://www.youtube.com" cookies.txt
   ```
4. The script will automatically use `cookies.txt` if it exists

## Method 3: Manual Cookie Export (Advanced)

If extensions don't work, you can manually export:

1. Open browser Developer Tools (F12)
2. Go to Application/Storage tab → Cookies → youtube.com
3. Copy all cookies and save in Netscape format as `cookies.txt`

## After Exporting Cookies

1. Make sure `cookies.txt` is in the same folder as `102303862.py`
2. Run your script:
   ```bash
   python 102303862.py "Sharry Maan" 11 21 102303862-output.mp3
   ```
3. The script will automatically detect and use the cookie file

## Notes

- Cookies expire after some time - you may need to re-export periodically
- Make sure you're logged into YouTube when exporting cookies
- The cookie file should be named exactly `cookies.txt`
- Keep cookies.txt private - it contains your login session

## Troubleshooting

- **"Cookie file not found"**: Make sure cookies.txt is in the same folder as the script
- **"Invalid cookie format"**: Try exporting again with the extension
- **Still getting bot errors**: Wait 10-15 minutes and try again, or export fresh cookies
