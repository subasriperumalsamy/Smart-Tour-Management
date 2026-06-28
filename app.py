import streamlit as st

st.set_page_config(page_title="Smart Tour", layout="wide")

st.sidebar.title("🌍 SmartTour")
page = st.sidebar.radio("Navigate", [
    "Dashboard",
    "Explore Places",
    "Analytics Hub",
    "Smart Itinerary"
])

if page == "Dashboard":
    st.switch_page("pages/dashboard.py")

elif page == "Explore Places":
    st.switch_page("pages/explore.py")

elif page == "Analytics Hub":
    st.switch_page("pages/analytics.py")

elif page == "Smart Itinerary":
    st.switch_page("pages/itinerary.py")