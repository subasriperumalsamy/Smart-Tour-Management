import streamlit as st
import pandas as pd

st.title("Tourism Analytics Dashboard")

df = pd.read_csv("TN_tourism.csv")

# ---------------- District ----------------
st.subheader("Places per District")
district_counts = df["District"].value_counts().reset_index()
district_counts.columns = ["District", "Count"]
st.bar_chart(district_counts.set_index("District"))

# ---------------- Category ----------------
st.subheader("Places by Category")
category_counts = df["Category"].value_counts().reset_index()
category_counts.columns = ["Category", "Count"]
st.bar_chart(category_counts.set_index("Category"))

# ---------------- Weather ----------------
st.subheader("Weather Distribution")
weather_counts = df["Weather"].value_counts().reset_index()
weather_counts.columns = ["Weather", "Count"]
st.bar_chart(weather_counts.set_index("Weather"))