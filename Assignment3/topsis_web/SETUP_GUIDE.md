# TOPSIS Web Service - Complete Setup Guide

## Part III: Web Service for TOPSIS

This guide will help you create and deploy a web service for TOPSIS analysis with email functionality.

---

## What You'll Build

A web application with:
- File upload interface
- Input fields for weights, impacts, and email
- TOPSIS calculation backend
- Email delivery of results
- Input validation

---

## Project Structure

```
topsis_web/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── sample_data.csv         # Test data
├── templates/
│   └── index.html         # Web form interface
├── static/
│   └── css/
│       └── style.css      # Styling
├── uploads/               # Temporary file storage (created automatically)
└── results/               # Result files (created automatically)
```

---

## Step 1: Install Python and Dependencies

### Install Python (if not already installed)
Download from: https://www.python.org/downloads/

### Install Flask
```bash
cd topsis_web
pip install -r requirements.txt
```

Or manually:
```bash
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
```

---

## Step 2: Configure Email Settings

Open `app.py` and update these lines (around line 28-31):

```python
# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"      # YOUR EMAIL HERE
SENDER_PASSWORD = "your-app-password"       # YOUR APP PASSWORD HERE
```

### Getting Gmail App Password:

1. Go to your Google Account: https://myaccount.google.com/
2. Click "Security" in the left menu
3. Enable "2-Step Verification" (if not already enabled)
4. Search for "App passwords"
5. Select app: "Mail"
6. Select device: "Other" (enter "TOPSIS App")
7. Click "Generate"
8. Copy the 16-character password
9. Paste it in `app.py` as `SENDER_PASSWORD`

**Important**: Use App Password, NOT your regular Gmail password!

---

## Step 3: Run the Web Service Locally

### Start the server:
```bash
cd topsis_web
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
```

### Access the web interface:
Open your browser and go to:
```
http://localhost:5000
```

---

## Step 4: Test the Application

### Test Data:
- **File**: Use `sample_data.csv` (provided)
- **Weights**: `1,1,1,1,1`
- **Impacts**: `+,+,-,+,+`
- **Email**: Your actual email address

### Steps:
1. Click "Browse File" and select `sample_data.csv`
2. Enter weights: `1,1,1,1,1`
3. Enter impacts: `+,+,-,+,+`
4. Enter your email address
5. Click "Submit"
6. Check your email for results!

---

## Step 5: Deploy to the Web (Production)

### Option A: Deploy to Heroku (Free/Paid)

#### 1. Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

#### 2. Create additional files:

**Procfile** (no extension):
```
web: python app.py
```

**runtime.txt**:
```
python-3.11.0
```

#### 3. Deploy:
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-topsis-app

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku master

# Open app
heroku open
```

Your app will be live at: `https://your-topsis-app.herokuapp.com`

---

### Option B: Deploy to PythonAnywhere (Free)

#### 1. Create account:
Go to: https://www.pythonanywhere.com/

#### 2. Upload files:
- Go to "Files" tab
- Create folder: `topsis_web`
- Upload all your files

#### 3. Create web app:
- Go to "Web" tab
- Click "Add a new web app"
- Choose "Flask"
- Python version: 3.10
- Set path to your `app.py`

#### 4. Configure:
- Set working directory to `/home/yourusername/topsis_web`
- Reload web app

Your app will be live at: `https://yourusername.pythonanywhere.com`

---

### Option C: Deploy to Render (Free)

#### 1. Create account:
Go to: https://render.com/

#### 2. Create new Web Service:
- Connect your GitHub repository
- Select `topsis_web` folder
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`

Your app will be live at: `https://your-app.onrender.com`

---

## Step 6: Input Validation (Already Implemented)

The app validates:
- File format (must be CSV)
- Number of weights = number of impacts
- Impacts are only '+' or '-'
- Weights are numeric
- Email format is valid
- CSV has at least 3 columns
- All data values are numeric

---

## Troubleshooting

### Issue: Email not sending

**Solution 1**: Check Gmail App Password
- Make sure you're using App Password, not regular password
- App Password should be 16 characters without spaces

**Solution 2**: Enable Less Secure Apps (if App Password doesn't work)
- Go to: https://myaccount.google.com/lesssecureapps
- Turn ON "Allow less secure apps"

**Solution 3**: Use different email provider
Update `app.py` with your SMTP settings:
```python
# For Outlook
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587

# For Yahoo
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
```

---

### Issue: ModuleNotFoundError: No module named 'flask'

**Solution**:
```bash
pip install Flask
```

---

### Issue: Port already in use

**Solution**: Change port in `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000
```

---

### Issue: File upload fails

**Solution**: Check file size (max 16MB by default)
Increase in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

---

## Features Implemented

- [x] File upload interface
- [x] Weights input field
- [x] Impacts input field
- [x] Email input field
- [x] TOPSIS calculation
- [x] Email delivery of results
- [x] Input validation
- [x] Error messages
- [x] Success notifications
- [x] Responsive design
- [x] Professional UI

---

## Testing Checklist

- [ ] Upload valid CSV file
- [ ] Enter correct weights and impacts
- [ ] Receive email with results
- [ ] Test with wrong number of weights
- [ ] Test with invalid impacts
- [ ] Test with invalid email format
- [ ] Test with non-CSV file
- [ ] Test with non-numeric data

---

## Assignment Submission

Include in your submission:
1. Screenshots of the web interface
2. Screenshot of email received
3. Screenshot of result file
4. Source code (app.py, templates, static)
5. Link to deployed application (if deployed)
6. README explaining setup

---

## Security Notes

**For production deployment:**
1. Never commit passwords to Git
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Add rate limiting
5. Implement user authentication (if needed)
6. Validate file uploads thoroughly
7. Set secure secret key

---

## Next Steps

1. Test locally
2. Configure email
3. Deploy to web
4. Share link with users
5. Monitor for errors

---

Good luck with your web service! 
