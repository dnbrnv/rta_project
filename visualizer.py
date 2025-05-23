import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Smart Climate System — Data Visualization")

# Load data from CSV file
df = pd.read_csv("climate_control_log.csv", header=None)
df.columns = ['timestamp', 'T_out', 'RH_out', 'Windspeed', 'predicted', 'recommended', 'action']
df['time'] = pd.to_datetime(df['timestamp'], unit='s')

# Temperature trends over time
st.subheader("Temperature Trends")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['time'], df['T_out'], label='Outdoor Temperature')
ax.plot(df['time'], df['predicted'], label='Predicted Indoor Temperature')
ax.plot(df['time'], df['recommended'], label='Recommended Temperature', linestyle='--')
ax.set_xlabel("Time")
ax.set_ylabel("Temperature (°C)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Action summary (heating/cooling/none)
st.subheader("System Actions")
action_counts = df['action'].value_counts()
st.bar_chart(action_counts)

# Show recent data
st.subheader("Latest Records")
st.dataframe(df.tail(20))