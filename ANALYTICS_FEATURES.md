# Advanced Analytics Features

## New Features Added

### 1. Time Period Filtering 📅
Select analysis period:
- **Today**: Only today's entry
- **This Week**: Last 7 days
- **This Month**: Last 30 days
- **This Year**: Last 365 days
- **All Time**: All entries

All metrics update based on selected period.

---

### 2. Health Score 🏥
Automatic health score calculation (0-100):

**Score Formula:**
```
Score = 100 - Risk% + (Good Habits Bonus × 0.3)
```

**Risk Factors:**
- 🍬 **High Sugar Intake**: Days with "High" sugar ≥ 50%
- 📱 **High Scrolling**: Days with "High" scrolling ≥ 50%

**Score Interpretation:**
- 🟢 **70+**: Excellent health
- 🟡 **50-69**: Good health
- 🔴 **Below 50**: Needs improvement

---

### 3. Risk Indicators ⚠️

**Sugar Intake Analysis:**
- Visual bar chart showing Nil/Low/High distribution
- Percentage of high sugar days
- Color-coded alerts:
  - ⛔ Red: >50% high sugar days
  - ⚠️ Orange: 25-50% high sugar days
  - ✅ Green: <25% high sugar days

**Scrolling Analysis:**
- Visual bar chart showing None/Low/High distribution
- Percentage of high scrolling days
- Color-coded alerts:
  - ⛔ Red: >50% high scrolling days
  - ⚠️ Orange: 25-50% high scrolling days
  - ✅ Green: <25% high scrolling days

---

### 4. Metrics Dashboard 📊

**Top Row** (Time Period Selector):
- 📅 Time period picker
- 🏥 Health score with color indicator
- ⚠️ Risk factor warnings

**Metrics Row**:
- Days Tracked (in period)
- Sugar Risk % (high sugar days)
- Scrolling Risk % (high scrolling days)
- Best Habit (most consistent habit)

---

### 5. Drill-Down View 🔍

**By Time Period:**
All data automatically recalculates:
```
Select "This Week" → See only last 7 days data
Select "This Month" → See only last 30 days data
Select "All Time" → See all data combined
```

**Visualizations Update:**
- Habit completion rates
- Sugar intake distribution
- Scrolling distribution
- Recent entries list
- All metrics and scores

---

## How to Use

### Daily Tracking
1. Go to "📝 Daily Entry"
2. Select your username
3. Log your habits
4. Click "✅ Submit Today's Entry"

### Analyze Performance
1. Go to "📊 Analysis Dashboard"
2. Select username
3. **Choose time period** (Today/Week/Month/Year/All)
4. Review:
   - Health Score
   - Risk factors
   - Sugar intake levels
   - Scrolling levels
   - Best habits
   - Habit completion rates

### Interpret Risk Levels
- **Sugar Intake**:
  - 🟢 Nil: Best (keep it up!)
  - 🟡 Low: Good (acceptable)
  - 🔴 High: Avoid (bad for health)

- **Scrolling**:
  - 🟢 None: Best (no screen time)
  - 🟡 Low: Good (limited use)
  - 🔴 High: Excessive (reduce it)

---

## Example Analysis

**Scenario**: User logged habits for 30 days

### Overall (All Time):
- Health Score: 65/100 (Good)
- Risk Factors:
  - 🍬 High Sugar Intake (45% of days)
  - 📱 High Scrolling (60% of days)

### This Week Drill-Down:
- Health Score: 72/100 (Excellent!)
- Sugar Risk: 20% (Improved!)
- Scrolling Risk: 40% (Getting better)

**Insight**: User is improving this week. Keep up the good work!

---

## Configuration

The health score calculation can be tuned in `utils.py`:

```python
def calculate_health_score(entries):
    # Adjust thresholds:
    sugar_risk_threshold = 50  # % of high sugar days
    scrolling_risk_threshold = 50  # % of high scrolling days
    good_habit_bonus = 0.3  # Multiplier for good habits
```

---

## Features by Time Period

### Today
- Single day's entry
- Useful for daily review
- Shows exactly what you did today

### This Week
- 7-day rolling window
- Great for habits development
- See weekly patterns

### This Month
- 30-day window
- Good for monthly goals
- Spot trends

### This Year
- 365-day window
- Full year review
- Long-term progress

### All Time
- Complete history
- Overall performance
- Career statistics

---

## Tips for Best Results

✅ **Do**:
- Log habits consistently
- Review weekly for trends
- Set goals for next period
- Track "bad" habits to reduce them

❌ **Don't**:
- Skip days (affects accuracy)
- Be too strict on yourself
- Ignore risk warnings
- Only focus on one metric

---

## Future Enhancements

- 📈 Trend analysis (improving/declining)
- 🎯 Goal setting per habit
- 🏆 Achievement badges
- 📧 Weekly email reports
- 📱 Mobile app
- 🤖 AI recommendations
- 👥 Social challenges

---
