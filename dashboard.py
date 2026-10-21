import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 People Counting Dashboard")

log_file = "people_log.csv"
try:
    df = pd.read_csv(log_file, names=["Timestamp", "People Count"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])  
    st.dataframe(df)
except FileNotFoundError:
    st.error("No data found. Run the people counter first.")
    df = pd.DataFrame(columns=["Timestamp", "People Count"])

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("today"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

if not df.empty:
    st.write("### People Count Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(df["Timestamp"], df["People Count"], marker="o", linestyle="-", color="b")
    plt.xlabel("Time")
    plt.ylabel("People Count")
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)
else:
    st.warning("No data available for the selected period.")


