# 🎯 Habit Tracker & Analysis

A modern Streamlit app for tracking daily habits and analyzing your progress over time. Track habits like yoga, running, reading, meditation, and more. Store data in a Cloudflare D1 SQLite database or local SQLite for development.

## Features

✨ **Easy Daily Entry**
- Quick checkbox-based habit logging
- Select from dropdown options for multi-value habits (Sugar Intake, Scrolling)
- Update existing entries anytime

📊 **Analysis Dashboard**
- View completion rates for each habit
- Track streaks and progress over time
- Visual charts and statistics
- Recent entry history

👥 **Multi-User Support**
- Each user has their own habit log
- Isolated data per user
- Perfect for families or groups

☁️ **Cloud & Local Storage**
- Cloudflare D1 SQLite database for cloud storage
- Local SQLite fallback for development
- Automatic data persistence

## Habits Included

### 💪 Physical Habits
- Yoga (Yes/No)
- Running (Yes/No)
- Meditation (Yes/No)

### 🧠 Mental Habits
- Focus Work (Yes/No)
- Learning Skillup (Yes/No)
- Reading (Yes/No)

### 🍽️ Intake Tracking
- Sugar Intake (Nil/Low/High)

### 📱 Digital Habits
- Scrolling (None/Low/High)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Local Development Setup

1. **Clone or download the project**
   ```bash
   cd habit-analysis
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

### Using Local SQLite (Default)

By default, the app uses a local SQLite database (`habit_tracker.db`). This works immediately without any configuration. Perfect for testing!

### Cloudflare D1 Setup (Optional - for cloud deployment)

If you want to use Cloudflare D1:

1. **Create a Cloudflare account** at https://dash.cloudflare.com

2. **Create a D1 database**
   - Go to Workers & Pages > D1
   - Create a new database
   - Note your: `Account ID`, `Database ID`

3. **Create a Cloudflare API token**
   - Account → API Tokens
   - Create token with D1 permissions
   - Copy the token

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your Cloudflare credentials:
   ```
   CLOUDFLARE_API_TOKEN=your_token
   CLOUDFLARE_ACCOUNT_ID=your_account_id
   D1_DATABASE_ID=your_database_id
   ```

5. **Create D1 schema**
   Run this SQL query in your D1 dashboard:
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

## How to Use

### Daily Entry
1. Open the app
2. Click on **"📝 Daily Entry"** in the sidebar
3. Select your username
4. Check/select your habits for today
5. Click **"✅ Submit Today's Entry"**
6. To update an existing entry, just resubmit!

### Analysis Dashboard
1. Click on **"📊 Analysis"** in the sidebar
2. Select a user
3. View completion rates, charts, and recent entries
4. Track your progress over time

## Deployment to Streamlit Cloud (Free)

### Step 1: Push to GitHub

1. Create a GitHub repository
2. Add this project to it
3. Make sure `.env` and `habit_tracker.db` are in `.gitignore`

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and `app.py`
5. If using Cloudflare D1, add secrets in **Settings**:
   - Click "Advanced settings"
   - Add to `.streamlit/secrets.toml`:
   ```
   CLOUDFLARE_API_TOKEN = "your_token"
   CLOUDFLARE_ACCOUNT_ID = "your_account_id"
   D1_DATABASE_ID = "your_database_id"
   ```

Your app will be live! Share the URL with others.

### Step 3: Update Secrets on Streamlit Cloud

If deploying to Streamlit Cloud and using Cloudflare D1:

1. In your GitHub repo, create `.streamlit/secrets.toml` locally (don't commit it!)
2. On Streamlit Cloud app settings, click "Secrets"
3. Paste your environment variables there

## File Structure

```
habit-analysis/
├── app.py                  # Main Streamlit app
├── config.py              # Habit & user configuration
├── database.py            # Database operations (local & D1)
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── README.md              # This file
```

## Adding More Users

Edit `config.py` and update the `USERS` list:

```python
USERS = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
```

## Adding More Habits

Edit `config.py` and add to the `HABITS` dictionary:

```python
HABITS = {
    "Your Habit": "boolean",  # or "select"
    "Multi-value Habit": "select",
}
```

Then add to `HABIT_TYPES` for categorization:

```python
HABIT_TYPES = {
    "physical": ["Yoga", "Running", "Your Habit"],
    ...
}
```

If it's a select type, add options:

```python
HABIT_SELECT_OPTIONS = {
    "Multi-value Habit": ["Option1", "Option2", "Option3"],
}
```

## Troubleshooting

### "ModuleNotFoundError" when running
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

### Database errors
- Ensure `habit_tracker.db` has read/write permissions
- Check that `.env` file has correct Cloudflare credentials (if using D1)

### Cloudflare D1 connection issues
- Verify your API token is valid
- Check Account ID and Database ID are correct
- Ensure D1 table schema exists
- Review Cloudflare API response in logs

### Secrets not loading on Streamlit Cloud
- Don't commit `.env` file (should be in `.gitignore`)
- Use `.streamlit/secrets.toml` on Streamlit Cloud instead
- Reload the app after updating secrets

## Future Enhancements

- 📧 Email reminders
- 📈 Advanced analytics and trends
- 🎯 Goal setting
- 🏆 Achievements & badges
- 📱 Mobile app
- 📊 Export to CSV/PDF
- 👥 Social features (friend streaks, challenges)

## License

MIT License - Feel free to use and modify!

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review logs in VS Code's terminal
3. Verify all environment variables are set correctly
4. Check Cloudflare dashboard if using D1

---

Happy tracking! 🚀