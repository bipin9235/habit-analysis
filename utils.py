import streamlit as st
from datetime import datetime, timedelta
from config import HABITS, HABIT_SELECT_OPTIONS, HABIT_TYPES
import json
import pandas as pd

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

def filter_entries_by_period(entries, period="all"):
    """Filter entries by time period"""
    if period == "all":
        return entries
    
    today = datetime.now().date()
    filtered = []
    
    for entry_date_str, entry_data in entries:
        try:
            entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
            
            if period == "today":
                if entry_date == today:
                    filtered.append((entry_date_str, entry_data))
            elif period == "week":
                days_ago = (today - entry_date).days
                if 0 <= days_ago < 7:
                    filtered.append((entry_date_str, entry_data))
            elif period == "month":
                days_ago = (today - entry_date).days
                if 0 <= days_ago < 30:
                    filtered.append((entry_date_str, entry_data))
            elif period == "year":
                days_ago = (today - entry_date).days
                if 0 <= days_ago < 365:
                    filtered.append((entry_date_str, entry_data))
        except:
            pass
    
    return filtered

def calculate_health_score(entries):
    """
    Calculate overall health score based on habits
    Negative habits: High Sugar Intake, High Scrolling
    Positive habits: Yoga, Running, Meditation, Focus Work, Reading, Learning
    """
    if not entries:
        return {"score": 0, "risk_factors": [], "good_habits": []}
    
    total_entries = len(entries)
    sugar_high_count = 0
    scrolling_high_count = 0
    
    good_habit_counts = {
        "Yoga": 0,
        "Running": 0,
        "Meditation": 0,
        "Focus Work": 0,
        "Reading": 0,
        "Learning/Skillup": 0
    }
    
    for entry_date_str, entry_data_str in entries:
        try:
            entry_data = json.loads(entry_data_str)
            
            # Check negative habits
            if "Sugar Intake" in entry_data:
                if entry_data["Sugar Intake"] == "High":
                    sugar_high_count += 1
            
            if "Scrolling" in entry_data:
                if entry_data["Scrolling"] == "High":
                    scrolling_high_count += 1
            
            # Check positive habits
            for habit in good_habit_counts:
                if habit in entry_data:
                    value = entry_data[habit]
                    if value == True or value == "Yes":
                        good_habit_counts[habit] += 1
        except:
            pass
    
    # Calculate health metrics
    sugar_risk = (sugar_high_count / total_entries * 100) if total_entries > 0 else 0
    scrolling_risk = (scrolling_high_count / total_entries * 100) if total_entries > 0 else 0
    
    good_habits = {h: (c / total_entries * 100) for h, c in good_habit_counts.items()}
    
    # Calculate score (0-100)
    risk_score = (sugar_risk + scrolling_risk) / 2  # Average risk
    
    # Positive habits boost score
    avg_good_habits = sum(good_habits.values()) / len(good_habits) if good_habits else 0
    
    # Final score: 100 - risk + good habits bonus
    score = max(0, min(100, 100 - risk_score + (avg_good_habits * 0.3)))
    
    # Identify risk factors
    risk_factors = []
    if sugar_risk > 50:
        risk_factors.append(f"🍬 High Sugar Intake ({sugar_risk:.0f}% of days)")
    if scrolling_risk > 50:
        risk_factors.append(f"📱 High Scrolling ({scrolling_risk:.0f}% of days)")
    
    # Best habits
    best_habits = sorted(good_habits.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "score": score,
        "risk_factors": risk_factors,
        "sugar_risk": sugar_risk,
        "scrolling_risk": scrolling_risk,
        "good_habits": dict(best_habits)
    }

def get_period_label(period):
    """Get friendly name for period"""
    labels = {
        "today": "Today",
        "week": "This Week",
        "month": "This Month",
        "year": "This Year",
        "all": "All Time"
    }
    return labels.get(period, period)
