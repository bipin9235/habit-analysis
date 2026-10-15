"""
Sample data initialization script
Run this to populate the database with sample entries for testing
"""

import sqlite3
import json
from datetime import datetime, timedelta
from config import LOCAL_DB_PATH, USERS

def init_sample_data():
    """Initialize database with sample data for testing"""
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    
    # Sample data for the last 30 days
    sample_habits = {
        "Alice": {
            "Yoga": [True, True, False, True, True, True, False, True, True, True,
                     True, False, True, True, True, True, False, True, True, True,
                     True, True, False, True, True, True, True, False, True, True],
            "Running": [True, False, True, False, True, True, False, True, False, True,
                        True, True, False, False, True, True, True, False, True, True,
                        False, True, True, False, True, True, False, True, True, False],
            "Focus Work": [True, True, True, True, True, True, True, True, True, True,
                           True, True, True, True, True, True, True, True, True, True,
                           True, True, True, True, True, True, True, True, True, True],
            "Reading": [True, True, False, True, True, False, True, False, True, True,
                        True, False, True, True, True, False, True, True, False, True,
                        True, True, False, True, True, False, True, True, True, False],
            "Sugar Intake": ["Low", "Low", "High", "Low", "Low", "Low", "High", "Low", "Low", "Low",
                            "Low", "High", "Nil", "Low", "Low", "Low", "High", "Low", "Low", "Low",
                            "Low", "Low", "High", "Nil", "Low", "Low", "Low", "Low", "Low", "High"],
            "Learning Skillup": [True, True, True, False, True, True, False, True, True, True,
                                True, False, True, True, True, False, True, True, True, False,
                                True, True, False, True, True, True, True, True, True, True],
            "Meditation": [True, False, True, True, False, True, True, True, False, True,
                          True, True, False, True, True, True, True, False, True, True,
                          True, False, True, True, True, True, False, True, True, True],
            "Scrolling": ["Low", "High", "High", "Low", "Low", "High", "High", "Low", "High", "Low",
                         "Low", "High", "High", "Low", "Low", "Low", "High", "Low", "High", "Low",
                         "Low", "High", "Low", "None", "Low", "Low", "High", "Low", "Low", "High"],
        },
        "Bob": {
            "Yoga": [False, False, False, True, False, False, True, False, False, True,
                     False, True, False, False, True, False, False, True, False, False,
                     True, False, False, True, False, False, True, False, False, True],
            "Running": [True, True, True, True, True, True, True, True, True, True,
                        True, True, True, True, True, True, True, True, True, True,
                        True, True, True, True, True, True, True, True, True, True],
            "Focus Work": [True, True, True, True, True, True, False, True, True, True,
                           True, True, True, False, True, True, True, True, True, True,
                           True, True, False, True, True, True, True, True, True, True],
            "Reading": [False, False, True, False, False, True, False, False, True, False,
                        False, True, False, False, True, False, False, True, False, False,
                        True, False, False, True, False, False, True, False, False, True],
            "Sugar Intake": ["High", "High", "Nil", "High", "High", "Nil", "High", "High", "Nil", "High",
                            "High", "Nil", "High", "High", "Nil", "High", "High", "Nil", "High", "High",
                            "Nil", "High", "High", "Nil", "High", "High", "Nil", "High", "High", "Nil"],
            "Learning Skillup": [False, True, False, False, True, False, False, True, False, False,
                                True, False, False, True, False, False, True, False, False, True,
                                False, False, True, False, False, True, False, False, True, False],
            "Meditation": [False, False, False, False, False, False, False, False, False, False,
                          False, False, False, False, False, False, False, False, False, False,
                          False, False, False, False, False, False, False, False, False, False],
            "Scrolling": ["High", "High", "High", "High", "High", "High", "High", "High", "High", "High",
                         "High", "High", "High", "High", "High", "High", "High", "High", "High", "High",
                         "High", "High", "High", "High", "High", "High", "High", "High", "High", "High"],
        },
        "Charlie": {
            "Yoga": [True, True, True, True, True, True, True, True, True, True,
                     True, True, True, True, True, True, True, True, True, True,
                     True, True, True, True, True, True, True, True, True, True],
            "Running": [True, True, True, True, True, True, True, True, True, True,
                        True, True, True, True, True, True, True, True, True, True,
                        True, True, True, True, True, True, True, True, True, True],
            "Focus Work": [True, True, True, True, True, True, True, True, True, True,
                           True, True, True, True, True, True, True, True, True, True,
                           True, True, True, True, True, True, True, True, True, True],
            "Reading": [True, True, True, True, True, True, True, True, True, True,
                        True, True, True, True, True, True, True, True, True, True,
                        True, True, True, True, True, True, True, True, True, True],
            "Sugar Intake": ["Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil",
                            "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil",
                            "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil", "Nil"],
            "Learning Skillup": [True, True, True, True, True, True, True, True, True, True,
                                True, True, True, True, True, True, True, True, True, True,
                                True, True, True, True, True, True, True, True, True, True],
            "Meditation": [True, True, True, True, True, True, True, True, True, True,
                          True, True, True, True, True, True, True, True, True, True,
                          True, True, True, True, True, True, True, True, True, True],
            "Scrolling": ["None", "None", "None", "None", "None", "None", "None", "None", "None", "None",
                         "None", "None", "None", "None", "None", "None", "None", "None", "None", "None",
                         "None", "None", "None", "None", "None", "None", "None", "None", "None", "None"],
        }
    }
    
    # Insert sample data
    today = datetime.now().date()
    
    for username in USERS:
        if username in sample_habits:
            habits_data = sample_habits[username]
            
            for day_offset in range(30):
                entry_date = (today - timedelta(days=day_offset)).strftime("%Y-%m-%d")
                
                # Build habits entry
                entry_habits = {}
                for habit_name, values in habits_data.items():
                    if day_offset < len(values):
                        entry_habits[habit_name] = values[day_offset]
                
                habits_json = json.dumps(entry_habits)
                
                try:
                    cursor.execute('''
                        INSERT INTO habit_entries (username, entry_date, habits_data)
                        VALUES (?, ?, ?)
                    ''', (username, entry_date, habits_json))
                except sqlite3.IntegrityError:
                    # Entry already exists, update it
                    cursor.execute('''
                        UPDATE habit_entries
                        SET habits_data = ?
                        WHERE username = ? AND entry_date = ?
                    ''', (habits_json, username, entry_date))
    
    conn.commit()
    conn.close()
    
    print("✅ Sample data initialized successfully!")
    print(f"   - Added data for {len(USERS)} users")
    print(f"   - 30 days of habit tracking per user")
    print(f"   - Database: {LOCAL_DB_PATH}")

if __name__ == "__main__":
    init_sample_data()
