import os
from dotenv import load_dotenv

load_dotenv()

# Users for the application (demo setup with 3 users)
USERS = ["Bipin", "Ragini"]

# Define all available habits with their types
HABITS = {
    "Yoga": "boolean",           # Yes/No
    "Running": "boolean",        # Yes/No
    "Focus Work": "boolean",     # Yes/No
    "Reading": "boolean",        # Yes/No
    "Sugar Intake": "select",    # Low, High, Nil
    "Learning/Skillup": "boolean",  # Yes/No
    "Meditation": "boolean",     # Yes/No
    "Scrolling": "select",       # None, Low, High
}

# Habit categories for organization
HABIT_TYPES = {
    "physical": ["Yoga", "Running", "Meditation"],
    "mental": ["Focus Work", "Learning/Skillup", "Reading"],
    "intake": ["Sugar Intake"],
    "digital": ["Scrolling"],
}

# Select options for habits with selections
HABIT_SELECT_OPTIONS = {
    "Sugar Intake": ["Nil", "Low", "High"],
    "Scrolling": ["None", "Low", "High"],
}

# Database configuration
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
D1_DATABASE_ID = os.getenv("D1_DATABASE_ID")

# For local testing/development
USE_LOCAL_DB = not all([CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, D1_DATABASE_ID])
LOCAL_DB_PATH = "habit_tracker.db"
