import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Tourism AI",
    page_icon="🌍",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("TN_tourism.csv")

# ---------------- DATA CLEANING ----------------

# Remove ₹ and commas if present
df["Budget"] = (
    df["Budget"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["Budget"] = pd.to_numeric(
    df["Budget"],
    errors="coerce"
)

df["Rating"] = pd.to_numeric(
    df["Rating"],
    errors="coerce"
)

# Remove rows with missing values
df = df.dropna(subset=["Budget", "Rating"])

# ---------------- SIDEBAR ----------------

st.sidebar.title("🌍 Smart Tourism AI")

source = st.sidebar.text_input(
    "Source Location",
    "Palani"
)

destination = st.sidebar.selectbox(
    "Destination District",
    sorted(df["District"].dropna().unique())
)

budget = st.sidebar.slider(
    "Budget (₹)",
    1000,
    20000,
    5000
)

days = st.sidebar.slider(
    "Duration (Days)",
    1,
    10,
    3
)

# ---------------- FILTER ----------------

filtered = df[
    (df["District"] == destination)
    &
    (df["Budget"] <= budget)
]

filtered = filtered.sort_values(
    by="Rating",
    ascending=False
)

# ---------------- HEADER ----------------

st.markdown("""
<div style="
background:linear-gradient(135deg,#0A4D68,#F4B400);
padding:25px;
border-radius:20px;
color:white;
text-align:center;">
<h1>🌍 Smart Tourism AI Dashboard</h1>
<h3>Plan Smarter • Travel Better</h3>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- METRICS ----------------

c1,c2,c3,c4 = st.columns(4)

c1.metric("📍 Source", source)
c2.metric("🎯 Destination", destination)
c3.metric("💰 Budget", f"₹{budget}")
c4.metric("📅 Duration", f"{days} Days")

# ---------------- AI SCORE ----------------

st.markdown("## 🤖 AI Trip Score")

score = min(100, int((budget / 10000) * 100))

st.progress(score)

st.success(f"Trip Suitability Score: {score}%")

# ---------------- RECOMMENDATIONS ----------------
st.markdown("## 🔥 Recommended Places")

if filtered.empty:

    st.warning("No tourist places found for this budget.")

else:

    places_per_page = 9

    if "page" not in st.session_state:
        st.session_state.page = 0

    start = st.session_state.page * places_per_page
    end = start + places_per_page

    page_data = filtered.iloc[start:end]

    cols = st.columns(3)

    for i, (_, row) in enumerate(page_data.iterrows()):

        with cols[i % 3]:
            st.markdown(f"""
            <div style="
            background: linear-gradient(135deg,#0A4D68,#0F6E8C);
            padding:20px;
            border-radius:20px;
            border-top:5px solid #F4B400;
            box-shadow:0px 6px 18px rgba(0,0,0,0.15);
            margin-bottom:20px;
            color:white;
            min-height:280px;
            ">

           <h3>🌍 {row['Place_Name']}</h3>

           <hr style="border:1px solid rgba(255,255,255,0.3);">

           <p>⭐ Rating: <b>{row['Rating']}</b></p>

           <p>🏷 Category: <b>{row['Category']}</b></p>

           <p>💰 Budget: <b>₹{int(row['Budget'])}</b></p>

           <p>☁ Weather: <b>{row['Weather']}</b></p>

           <p>🏨 Stay: <b>{row['Accommodation_Name']}</b></p>

           <p>📅 Best Month: <b>{row['Best_Month']}</b></p>

           </div>
           """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅ Previous"):
            if st.session_state.page > 0:
                st.session_state.page -= 1
                st.rerun()

    with col2:
        total_pages = (len(filtered) - 1) // places_per_page + 1
        st.markdown(
            f"<center><b>Page {st.session_state.page + 1} of {total_pages}</b></center>",
            unsafe_allow_html=True
        )

    with col3:
        if st.button("Next ➡"):
            if end < len(filtered):
                st.session_state.page += 1
                st.rerun()

# ---------------- INSIGHTS ----------------

if not filtered.empty:

    best = filtered.iloc[0]

    st.markdown("## 🧠 AI Travel Insights")

    st.info(f"""
✔ Best Place : {best['Place_Name']}

✔ Best Month : {best['Best_Month']}

✔ Accommodation : {best['Accommodation_Name']}

✔ Weather : {best['Weather']}

✔ Route : {best['Best_Route']}
""")

# ---------------- ITINERARY ----------------

st.markdown("## 📅 Suggested Itinerary")

tab1, tab2, tab3 = st.tabs([
    "Day 1",
    "Day 2",
    "Day 3"
])

places = filtered["Place_Name"].tolist()

with tab1:
    for p in places[:2]:
        st.success(p)

with tab2:
    for p in places[2:4]:
        st.success(p)

with tab3:
    for p in places[4:6]:
        st.success(p)

# ---------------- ANALYTICS ----------------

st.markdown("## 📊 Quick Analytics")

a1,a2,a3,a4 = st.columns(4)

a1.metric("Places", len(filtered))

a2.metric(
    "Avg Rating",
    round(filtered["Rating"].mean(), 2)
    if not filtered.empty else 0
)

a3.metric(
    "Categories",
    filtered["Category"].nunique()
    if not filtered.empty else 0
)

a4.metric(
    "Hotels",
    filtered["Accommodation_Name"].nunique()
    if not filtered.empty else 0
)

# ---------------- TABLE ----------------

st.markdown("## 🏞 Matching Places")

if not filtered.empty:

    st.dataframe(
        filtered[
            [
                "Place_Name",
                "Category",
                "Rating",
                "Budget",
                "Weather",
                "Best_Month"
            ]
        ],
        use_container_width=True
    )
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
geolocator = Nominatim(user_agent="tourism_app")

def get_coords(place):
    try:
        location = geolocator.geocode(place)
        if location:
            return [location.latitude, location.longitude]
    except:
        return None

    return None
source = st.sidebar.text_input(
    "Source Location",
    "Palani",
    key="source_input"
)

destination = st.sidebar.selectbox(
    "Destination District",
    sorted(df["District"].unique()),
    key="destination_select"
)

budget = st.sidebar.slider(
    "Budget (₹)",
    1000,
    20000,
    5000,
    key="budget_slider"
)

days = st.sidebar.slider(
    "Duration (Days)",
    1,
    10,
    3,
    key="days_slider"
)


st.markdown("## 🗺 Route Map")

source_coords = get_coords(source)
dest_coords = get_coords(destination)

if source_coords and dest_coords:

    center_lat = (
        source_coords[0] + dest_coords[0]
    ) / 2

    center_lon = (
        source_coords[1] + dest_coords[1]
    ) / 2

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8
    )

    folium.Marker(
        source_coords,
        popup=f"Source: {source}",
        tooltip=source,
    ).add_to(m)

    folium.Marker(
        dest_coords,
        popup=f"Destination: {destination}",
        tooltip=destination,
    ).add_to(m)

    folium.PolyLine(
        [source_coords, dest_coords],
        weight=5
    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=500
    )

else:
    st.warning(
        "Unable to locate source or destination."
    )