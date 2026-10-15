# Streamlit Cloud Deployment Guide

## Quick Deploy to Streamlit Cloud

### Option 1: Direct Deployment (Recommended)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Habit Tracker app"
   git remote add origin https://github.com/YOUR_USERNAME/habit-analysis.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Click "New app"
   - Choose "GitHub" and select your repository
   - Select branch: `main`
   - Select file: `app.py`
   - Click "Deploy"

3. **Add Secrets (if using Cloudflare D1)**
   - Click "Settings" → "Secrets"
   - Paste your secrets:
   ```
   CLOUDFLARE_API_TOKEN = "your_token"
   CLOUDFLARE_ACCOUNT_ID = "your_account_id"  
   D1_DATABASE_ID = "your_database_id"
   ```
   - Save and refresh

### Option 2: Using Streamlit CLI

```bash
# Install Streamlit CLI
pip install streamlit

# Create a local account
streamlit login

# Deploy
streamlit deploy \
  --hello=false \
  --project=habit-analysis
```

## Running Locally

```bash
# Activate environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Environment Variables for Deployment

Create `.streamlit/secrets.toml` for local development:
```toml
CLOUDFLARE_API_TOKEN = "your_api_token"
CLOUDFLARE_ACCOUNT_ID = "your_account_id"
D1_DATABASE_ID = "your_database_id"
```

On Streamlit Cloud, add these through the Secrets manager in app settings.

## Database Options

### Option A: Local SQLite (Works immediately)
- No configuration needed
- Data stored in `habit_tracker.db` (local to runner)
- Perfect for development

### Option B: Cloudflare D1 (Recommended for production)
- Cloud database, persistent across deployments
- Data accessible from anywhere
- Free tier available

## Monitoring & Logs

View app logs on Streamlit Cloud:
1. Click your deployed app
2. Select "Manage app"
3. Check "Logs" tab

## Sharing Your App

After deployment, Streamlit generates a public URL like:
```
https://your-username-habit-analysis-xxxxx.streamlit.app
```

Share this link with users to access the habit tracker!

## Troubleshooting Deployment

### App crashes on startup
- Check "Logs" for error messages
- Verify all imports are in `requirements.txt`
- Test locally first: `streamlit run app.py`

### Database connection fails
- Verify Cloudflare credentials in secrets
- Check API token hasn't expired
- Ensure D1 table exists

### Secrets not loading
- Use `.streamlit/secrets.toml` format
- Do NOT commit secrets to GitHub
- Secrets are per-app in Streamlit Cloud

## Cost

Streamlit Community Cloud (Free tier):
- ✅ Unlimited apps
- ✅ Unlimited viewers
- ✅ 1 GB of storage per app
- ✅ 3 apps per GitHub account (paid plans available)

Cloudflare D1 (Free tier):
- ✅ Unlimited read queries
- ✅ 100,000 write queries per day
- ✅ Plenty for daily habit tracking!
