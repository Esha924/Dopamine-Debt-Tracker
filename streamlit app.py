import streamlit as st
import datetime
import os
import pandas as pd  # Streamlit-friendly for CSV, beginner simple

# Same functions as CLI version
@st.cache_data
def calculate_score(distraction, productive, sleep):
    """Calculate Dopamine Debt Score."""
    score = (distraction * 1.5) - (productive * 1.2)
    if sleep < 6:
        score += 15
    return score

def get_status(score):
    """Get status from score."""
    if score < 0:
        return "Balanced Day 🟢"
    elif score <= 30:
        return "Overstimulated Day 🟡"
    else:
        return "High Dopamine Debt 🔴"

def log_data(distraction, productive, sleep, score):
    """Log to CSV (same as CLI)."""
    filename = "dopamine_log.csv"
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("Date,Distraction,Productive,Sleep,Score\n")
    
    with open(filename, 'a') as f:
        f.write(f"{today},{distraction},{productive},{sleep},{score:.2f}\n")

def get_last_entries():
    """Get last 3 entries."""
    filename = "dopamine_log.csv"
    if not os.path.exists(filename):
        return pd.DataFrame()
    
    df = pd.read_csv(filename)
    return df.tail(3)

# Streamlit UI - simple and clean
st.title("🧠 Dopamine Debt Tracker")
st.markdown("Track your daily distractions vs productivity!")

# Sidebar inputs (sliders for easy use)
st.sidebar.header("Enter Today's Data")
distraction = st.sidebar.slider("Distraction time (minutes)", 0.0, 300.0, 30.0)
productive = st.sidebar.slider("Productive time (minutes)", 0.0, 600.0, 60.0)
sleep = st.sidebar.slider("Sleep hours", 0.0, 12.0, 7.0)

# Calculate if inputs changed
score = calculate_score(distraction, productive, sleep)
status = get_status(score)

# Main display
col1, col2 = st.columns(2)
with col1:
    st.metric("Dopamine Debt Score", f"{score:.2f}")
with col2:
    st.metric("Status", status)

if score > 30:
    st.error("🚨 Take a break! Go for a walk or meditate.")

# Log button
if st.button("📝 Log Today's Data", type="primary"):
    log_data(distraction, productive, sleep, score)
    st.success("Data logged! Refresh page or rerun to see updates.")
    st.rerun()

# Last 3 entries
st.subheader("📊 Last 3 Entries")
df = get_last_entries()
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No data yet. Log your first entry!")

# Footer
st.markdown("---")
st.caption("Built with Streamlit. Beginner-friendly code!")
