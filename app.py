import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from database import init_db, get_user_entry, save_entry, get_all_entries
from config import USERS, HABITS, HABIT_TYPES
from utils import (
    display_habits_form, 
    get_today_date,
    filter_entries_by_period,
    calculate_health_score,
    get_period_label
)

# Page configuration
st.set_page_config(
    page_title="Habit Tracker & Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .success {
        color: #31a354;
    }
    .warning {
        color: #ff9500;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
init_db()

# Sidebar
st.sidebar.title("🎯 Habit Tracker")
page = st.sidebar.radio("Navigate", ["📝 Daily Entry", "📊 Analysis"])

# Main content
if page == "📝 Daily Entry":
    st.title("📝 Daily Habit Entry")
    
    # User selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_user = st.selectbox(
            "Select your username:",
            USERS,
            key="user_select"
        )
    
    with col2:
        st.metric("Today's Date", get_today_date())
    
    st.divider()
    
    if selected_user:
        # Get today's entry if exists
        today_entry = get_user_entry(selected_user, get_today_date())
        
        if today_entry:
            st.info("✏️ You already have an entry for today. Update it below and submit to modify.", icon="ℹ️")
        
        # Display habit form
        st.subheader(f"Your Habits for {get_today_date()}")
        
        habits_data = display_habits_form(selected_user, today_entry)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("✅ Submit Today's Entry", use_container_width=True, type="primary"):
                try:
                    save_entry(selected_user, get_today_date(), habits_data)
                    st.success("✅ Your entry has been saved successfully!", icon="✅")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error saving entry: {str(e)}", icon="❌")
        
        with col2:
            if st.button("🔄 Reset Form", use_container_width=True):
                st.rerun()

elif page == "📊 Analysis":
    st.title("📊 Habit Analysis Dashboard")
    
    # User selection for analysis
    selected_user = st.selectbox(
        "Select user for analysis:",
        USERS,
        key="user_analysis"
    )
    
    if selected_user:
        st.divider()
        
        # Time period selector
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            period = st.selectbox(
                "📅 Select Time Period:",
                ["today", "week", "month", "year", "all"],
                format_func=get_period_label,
                key="period_select"
            )
        
        # Get all entries and filter by period
        all_entries = get_all_entries(selected_user)
        period_entries = filter_entries_by_period(all_entries, period)
        
        if period_entries:
            # Calculate and display health score
            health = calculate_health_score(period_entries)
            
            # Health score card
            with col2:
                # Color based on score
                if health["score"] >= 70:
                    color = "🟢"
                    status = "Excellent"
                elif health["score"] >= 50:
                    color = "🟡"
                    status = "Good"
                else:
                    color = "🔴"
                    status = "Needs Improvement"
                
                st.metric(f"Health Score {color}", f"{health['score']:.0f}/100", status)
            
            # Display risk factors
            with col3:
                if health["risk_factors"]:
                    st.warning("⚠️ **Risk Factors:**\n" + "\n".join(health["risk_factors"]))
                else:
                    st.success("✅ **No Risk Factors Detected!**")
            
            st.divider()
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Days Tracked", len(period_entries))
            
            with col2:
                st.metric("Sugar Risk", f"{health['sugar_risk']:.0f}%")
            
            with col3:
                st.metric("Scrolling Risk", f"{health['scrolling_risk']:.0f}%")
            
            with col4:
                if health["good_habits"]:
                    best_habit = max(health["good_habits"].items(), key=lambda x: x[1])
                    st.metric("Best Habit", best_habit[0], f"{best_habit[1]:.0f}%")
            
            st.divider()
            
            # Habit completion analysis
            st.subheader("Habit Completion Analysis")
            
            # Prepare data for analysis
            habit_completion = {}
            for habit_name in HABITS:
                completion_count = 0
                for entry in period_entries:
                    if entry and len(entry) > 1:
                        try:
                            # Use json.loads instead of eval (safer and more reliable)
                            entry_data = json.loads(entry[1])
                            
                            if habit_name in entry_data:
                                value = entry_data[habit_name]
                                
                                # For boolean habits: count if True
                                if HABITS[habit_name] == "boolean":
                                    if value == True or value == "Yes":
                                        completion_count += 1
                                # For select habits: count any selection (not None/empty)
                                elif HABITS[habit_name] == "select":
                                    if value and value != "" and value != "None":
                                        completion_count += 1
                        except Exception as e:
                            pass
                
                completion_rate = (completion_count / len(period_entries) * 100) if period_entries else 0
                habit_completion[habit_name] = {
                    "completed": completion_count,
                    "total": len(period_entries),
                    "rate": completion_rate
                }
            
            # Display habit completion chart
            col1, col2 = st.columns([2, 1])
            
            with col1:
                chart_data = {h: v["rate"] for h, v in habit_completion.items()}
                if chart_data:
                    # Convert to DataFrame for better compatibility
                    df = pd.DataFrame(list(chart_data.items()), columns=["Habit", "Rate"])
                    st.bar_chart(df.set_index("Habit"))
                else:
                    st.info("No habit data available for this period")
            
            with col2:
                st.write("**Completion Rates:**")
                for habit, data in habit_completion.items():
                    rate = data["rate"]
                    if rate >= 70:
                        status = "🟢 Excellent"
                    elif rate >= 50:
                        status = "🟡 Good"
                    else:
                        status = "🔴 Needs Work"
                    st.write(f"**{habit}**: {rate:.0f}% {status}")
            
            st.divider()
            
            # Risk Factors Detailed Analysis
            st.subheader("⚠️ Risk Factor Analysis")
            
            risk_col1, risk_col2 = st.columns(2)
            
            with risk_col1:
                st.write("**🍬 Sugar Intake Levels**")
                sugar_levels = {"Nil": 0, "Low": 0, "High": 0}
                for entry in period_entries:
                    if entry and len(entry) > 1:
                        try:
                            entry_data = json.loads(entry[1])
                            if "Sugar Intake" in entry_data:
                                level = entry_data["Sugar Intake"]
                                if level in sugar_levels:
                                    sugar_levels[level] += 1
                        except:
                            pass
                
                # Create visualization
                if sum(sugar_levels.values()) > 0:
                    df_sugar = pd.DataFrame(list(sugar_levels.items()), columns=["Level", "Days"])
                    st.bar_chart(df_sugar.set_index("Level"))
                    high_pct = (sugar_levels["High"] / sum(sugar_levels.values()) * 100) if sum(sugar_levels.values()) > 0 else 0
                    if high_pct > 50:
                        st.error(f"⛔ High sugar intake detected ({high_pct:.0f}% of days)")
                    elif high_pct > 25:
                        st.warning(f"⚠️ Moderate sugar intake ({high_pct:.0f}% of days)")
                    else:
                        st.success(f"✅ Good sugar control ({high_pct:.0f}% of days)")
                else:
                    st.info("No sugar intake data recorded")
            
            with risk_col2:
                st.write("**📱 Scrolling Levels**")
                scrolling_levels = {"None": 0, "Low": 0, "High": 0}
                for entry in period_entries:
                    if entry and len(entry) > 1:
                        try:
                            entry_data = json.loads(entry[1])
                            if "Scrolling" in entry_data:
                                level = entry_data["Scrolling"]
                                if level in scrolling_levels:
                                    scrolling_levels[level] += 1
                        except:
                            pass
                
                # Create visualization
                if sum(scrolling_levels.values()) > 0:
                    df_scrolling = pd.DataFrame(list(scrolling_levels.items()), columns=["Level", "Days"])
                    st.bar_chart(df_scrolling.set_index("Level"))
                    high_pct = (scrolling_levels["High"] / sum(scrolling_levels.values()) * 100) if sum(scrolling_levels.values()) > 0 else 0
                    if high_pct > 50:
                        st.error(f"⛔ High scrolling detected ({high_pct:.0f}% of days)")
                    elif high_pct > 25:
                        st.warning(f"⚠️ Moderate scrolling ({high_pct:.0f}% of days)")
                    else:
                        st.success(f"✅ Good scrolling control ({high_pct:.0f}% of days)")
                else:
                    st.info("No scrolling data recorded")
            
            st.divider()
            
            # Recent entries
            st.subheader("Recent Entries")
            
            for entry_date, entry_data_str in period_entries[:10]:  # Last 10 entries in period
                with st.expander(f"📅 {entry_date}"):
                    try:
                        entry_data = json.loads(entry_data_str)
                        for habit, value in entry_data.items():
                            st.write(f"**{habit}:** {value}")
                    except:
                        st.write("Error parsing entry data")
            
            st.divider()
            
            # # Debug section
            # with st.expander("🔍 Debug: View Raw Data"):
            #     st.write(f"**Entries for {get_period_label(period)} (raw JSON):**")
            #     for entry_date, entry_data_str in period_entries[:5]:  # Show last 5
            #         st.code(f"Date: {entry_date}\nData: {entry_data_str}", language="json")
        else:
            st.info(f"No entries for {get_period_label(period)}. Start logging your habits from the Daily Entry page!", icon="ℹ️")
