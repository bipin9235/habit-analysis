import streamlit as st
from datetime import datetime
from config import HABITS, HABIT_SELECT_OPTIONS, HABIT_TYPES
import json

def get_today_date():
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")

def display_habits_form(username, today_entry=None):
    """Display the habit entry form and return the habits data"""
    habits_data = {}
    
    # Parse existing data if available
    existing_habits = {}
    if today_entry and "habits" in today_entry:
        existing_habits = today_entry["habits"]
    
    # Organize habits by category
    for category, habit_list in HABIT_TYPES.items():
        if category == "physical":
            st.subheader("💪 Physical Habits")
        elif category == "mental":
            st.subheader("🧠 Mental Habits")
        elif category == "intake":
            st.subheader("🍽️ Intake Tracking")
        elif category == "digital":
            st.subheader("📱 Digital Habits")
        
        cols = st.columns(len(habit_list))
        
        for idx, habit in enumerate(habit_list):
            with cols[idx]:
                if HABITS[habit] == "boolean":
                    # Yes/No toggle
                    default_value = existing_habits.get(habit, False)
                    habits_data[habit] = st.checkbox(
                        f"✓ {habit}",
                        value=default_value,
                        key=f"{username}_{habit}"
                    )
                    
                elif HABITS[habit] == "select":
                    # Dropdown selection
                    options = HABIT_SELECT_OPTIONS.get(habit, [])
                    default_value = existing_habits.get(habit, options[0] if options else None)
                    habits_data[habit] = st.selectbox(
                        habit,
                        options,
                        index=options.index(default_value) if default_value in options else 0,
                        key=f"{username}_{habit}"
                    )
        
        st.divider()
    
    return habits_data

def format_habit_display(habit_value):
    """Format habit value for display"""
    if isinstance(habit_value, bool):
        return "✅ Yes" if habit_value else "❌ No"
    else:
        return str(habit_value)

def calculate_streak(entries, habit_name):
    """Calculate the streak for a specific habit"""
    streak = 0
    for entry_date, entry_data_str in entries:
        try:
            entry_data = json.loads(entry_data_str)
            if habit_name in entry_data:
                value = entry_data[habit_name]
                if value == True or value == "Yes":
                    streak += 1
                else:
                    break
        except:
            break
    return streak

def get_habit_statistics(entries, habit_name):
    """Get statistics for a specific habit"""
    completed = 0
    total = len(entries)
    
    for entry_date, entry_data_str in entries:
        try:
            entry_data = json.loads(entry_data_str)
            if habit_name in entry_data:
                value = entry_data[habit_name]
                if value == True or value == "Yes":
                    completed += 1
        except:
            pass
    
    percentage = (completed / total * 100) if total > 0 else 0
    return {
        "completed": completed,
        "total": total,
        "percentage": percentage,
        "remaining": total - completed
    }
