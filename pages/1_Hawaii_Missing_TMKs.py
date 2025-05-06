import streamlit as st
import pandas as pd
import pydeck as pdk
import gdown
import os

# === Page setup ===
st.set_page_config(layout="wide", page_title="Hawaii Land Change Tracker")
st.title("📍 Map 1: Hawaii Missing TMKs (2020 → 2023 → 2024)")
st.markdown("""
This interactive map shows land parcels (TMKs) that disappeared or reappeared across three datasets:

- 🟥 **Disappeared after 2020**  
- 🟧 **Disappeared after 2023**  
- 🟩 **Reappeared in 2024**
""")

# === Google Drive file IDs ===
FILE_IDS = {
    "2020": "1Vz-oVGyUq5bS2mUHwDihrMfbLS0R3gvh",
    "2023": "1hmcideaS-t8MFFs5lzDHWuFQf5BrLyik",
    "2024": "1cQtEvFIJPb9Tu0PC4bblZ5uDtwTFsCTR"
}

@st.cache_data
def load_csv(file_id):
    path = f"/tmp/{file_id}.csv"
    if not os.path.exists(path):
        gdown.download(f"https://drive.google.com/uc?id={file_id}", path, quiet=False)
    return pd.read_csv(path)

try:
    df_2020 = load_csv(FILE_IDS["2020"])
    df_2023 = load_csv(FILE_IDS["2023"])
    df_2024 = load_csv(FILE_IDS["2024"])
except Exception as e:
    st.error(f"❌ Failed to load CSVs from Google Drive: {e}")
    st.stop()

if df_2020.empty or df_2023.empty or df_2024.empty:
    st.error("❌ One of the datasets is empty or unreadable.")
    st.stop()

# === Safe column detection ===
def detect_column(df, keywords):
    for col in df.columns:
        if isinstance(col, str):
            lower_col = col.lower()
            for kw in keywords:
                if kw in lower_col:
                    return col
    return None

tmk_col = detect_column(df_2020, ["tmk"])
lat_col = detect_column(df_2020, ["lat", "latitude", "y"])
lon_col = detect_column(df_2020, ["lon", "lng", "longitude", "x"])

missing = []
if not tmk_col: missing.append("TMK")
if not lat_col: missing.append("Latitude")
if not lon_col: missing.append("Longitude")

if missing:
    st.error(f"❌ Missing columns: {', '.join(missing)}")
    st.stop()

# === Compare TMKs ===
set_2020 = set(df_2020[tmk_col])
set_2023 = set(df_2023[tmk_col])
set_2024 = set(df_2024[tmk_col])

gone_after_2020 = set_2020 - set_2023 - set_2024
gone_after_2023 = set_2023 - set_2024
reappeared_2024 = (set_2020 - set_2023) & set_2024

def tag_changes(df, ids, label):
    sub = df[df[tmk_col].isin(ids)].copy()
    sub["change"] = label
    return sub[[tmk_col, lat_col, lon_col, "change"]]

df_map = pd.concat([
    tag_changes(df_2020, gone_after_2020, "Disappeared after 2020"),
    tag_changes(df_2023, gone_after_2023, "Disappeared after 2023"),
    tag_changes(df_2024, reappeared_2024, "Reappeared in 2024")
])

# === Summary ===
st.markdown(f"""
### 📊 Summary
- 🟥 Disappeared after 2020: **{len(gone_after_2020):,}**
- 🟧 Disappeared after 2023: **{len(gone_after_2023):,}**
- 🟩 Reappeared in 2024: **{len(reappeared_2024):,}**
""")

# === Map rendering ===
color_map = {
    "Disappeared after 2020": [255, 0, 0, 150],
    "Disappeared after 2023": [255, 140, 0, 150],
    "Reappeared in 2024": [0, 200, 0, 150],
}

layers = [
    pdk.Layer(
        "ScatterplotLayer",
        data=df_map[df_map["change"] == label],
        get_position=f"[{lon_col}, {lat_col}]",
        get_radius=30,
        get_fill_color=color,
        pickable=True,
    )
    for label, color in color_map.items()
]

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state=pdk.ViewState(latitude=21.5, longitude=-157.8, zoom=8.5),
    layers=layers,
    tooltip={"text": "{change}"}
))

st.download_button("⬇️ Download CSV", df_map.to_csv(index=False), "missing_tmks_2020_2024.csv")
