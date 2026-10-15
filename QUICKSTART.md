# Quick Start Guide 🚀

Get your habit tracker running in **5 minutes**!

## Option 1: Start Immediately (Local - No Configuration)

Perfect for testing and development!

### Windows
```powershell
# 1. Navigate to project folder
cd habit-analysis

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Load sample data (optional)
python init_sample_data.py

# 6. Run the app
streamlit run app.py
```

### macOS / Linux
```bash
# 1. Navigate to project folder
cd habit-analysis

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Load sample data (optional)
python init_sample_data.py

# 6. Run the app
streamlit run app.py
```

✨ **Your app is now running at:** `http://localhost:8501`

## Testing the App

### Predefined Users
- **Alice** - Perfect tracker
- **Bob** - Inconsistent tracker
- **Charlie** - Super focused

### What to try:
1. Select a username
2. Check/uncheck habits for today
3. Click "Submit Today's Entry"
4. Go to "📊 Analysis" to see charts
5. Try updating today's entry again (it updates!)

## Option 2: Deploy to Streamlit Cloud (Free Hosting)

### Prerequisites
- GitHub account
- GitHub repository with this code

### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Habit tracker app"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Select `app.py`
   - Click "Deploy"

3. **Share Your Link**
   - Your app gets a public URL!
   - Share with others

## Using Cloudflare D1 (Optional)

For persistent cloud database:

1. Create Cloudflare account (free at cloudflare.com)
2. Create D1 database
3. Copy your credentials:
   - Account ID
   - Database ID  
   - API Token
4. Create `.env` file:
   ```
   CLOUDFLARE_API_TOKEN=your_token
   CLOUDFLARE_ACCOUNT_ID=your_account_id
   D1_DATABASE_ID=your_database_id
   ```
5. Run schema SQL in Cloudflare dashboard:
   ```sql
   CREATE TABLE IF NOT EXISTS habit_entries (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT NOT NULL,
       entry_date TEXT NOT NULL,
       habits_data TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       UNIQUE(username, entry_date)
   );
   ```

## Customize Your Habits

Edit `config.py`:

```python
USERS = ["Your Name", "Friend 1", "Friend 2"]

HABITS = {
    "Sleep 8 Hours": "boolean",  # Yes/No
    "Water Intake": "select",     # Multiple choice
}

HABIT_SELECT_OPTIONS = {
    "Water Intake": ["Not Enough", "Good", "Excellent"],
}

HABIT_TYPES = {
    "health": ["Sleep 8 Hours", "Water Intake"],
}
```

Then restart the app: `streamlit run app.py`

## Troubleshooting

### Port 8501 already in use?
```bash
streamlit run app.py --server.port 8502
```

### Virtual environment issues?
```bash
# Deactivate
deactivate

# Delete old environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Create fresh one and repeat steps above
```

### Import errors?
```bash
# Make sure environment is activated, then:
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. ✅ Test locally
2. ✅ Customize habits
3. ✅ Deploy to Streamlit Cloud
4. ✅ Share with friends/family
5. ✅ Track daily!

## Questions?

See full documentation in:
- `README.md` - Complete guide
- `DEPLOYMENT.md` - Deployment details
- Comments in `config.py` - Customize app

---

**Happy Tracking!** 🎯📊
