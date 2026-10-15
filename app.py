import streamlit as st
import os
from datetime import datetime
from database import init_db, get_user_entry, save_entry, get_all_entries
from config import USERS, HABITS, HABIT_TYPES
from utils import display_habits_form, get_today_date

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
                    st.success("✅ Your entry has been saved successfully!", icon="✓")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error saving entry: {str(e)}", icon="✕")
        
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
        
        # Get all entries for user
        all_entries = get_all_entries(selected_user)
        
        if all_entries:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Days Tracked", len(all_entries))
            
            with col2:
                completed_entries = len([e for e in all_entries if e])
                st.metric("Completed Entries", completed_entries)
            
            with col3:
                if all_entries:
                    st.metric("Tracking Rate", f"{(completed_entries/len(all_entries)*100):.1f}%")
            
            with col4:
                st.metric("Last Entry", all_entries[0][0] if all_entries else "N/A")
            
            st.divider()
            
            # Habit completion analysis
            st.subheader("Habit Completion Analysis")
            
            # Prepare data for analysis
            habit_completion = {}
            for habit_name in HABITS:
                completion_count = 0
                for entry in all_entries:
                    if entry and len(entry) > 1:
                        try:
                            entry_data = eval(entry[1])  # Parse JSON string
                            if habit_name in entry_data:
                                if entry_data[habit_name] == True or entry_data[habit_name] == "Yes":
                                    completion_count += 1
                        except:
                            pass
                
                completion_rate = (completion_count / len(all_entries) * 100) if all_entries else 0
                habit_completion[habit_name] = {
                    "completed": completion_count,
                    "total": len(all_entries),
                    "rate": completion_rate
                }
            
            # Display habit completion chart
            col1, col2 = st.columns([2, 1])
            
            with col1:
                chart_data = {h: v["rate"] for h, v in habit_completion.items()}
                st.bar_chart(chart_data)
            
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
            
            # Recent entries
            st.subheader("Recent Entries")
            
            for entry_date, entry_data_str in all_entries[:10]:  # Last 10 entries
                with st.expander(f"📅 {entry_date}"):
                    try:
                        entry_data = eval(entry_data_str)
                        for habit, value in entry_data.items():
                            st.write(f"**{habit}:** {value}")
                    except:
                        st.write("Error parsing entry data")
        else:
            st.info("No entries yet. Start logging your habits from the Daily Entry page!", icon="ℹ️")
