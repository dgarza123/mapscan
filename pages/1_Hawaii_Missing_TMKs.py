# 1_Hawaii_Missing_TMKs.py (CSV version)

import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Hawaii Land Change Tracker")

st.title("📍 Map 1: Hawaii Missing TMKs (2020 → 2023 → 2024)")
st.markdown("""
This interactive map shows land parcels (TMKs) that disappeared or reappeared across three datasets:
- 🟥 Disappeared after 2020
- 🟧 Disappeared after 2023
- 🟩 Reappeared in 2024
""")

# === Google Drive File IDs ===
FILE_IDS = {
    "2020": "YOUR_2020_FILE_ID",
    "2023": "YOUR_2023_FILE_ID",
    "2024": "YOUR_2024_FILE_ID"
}

# === Load CSVs from Google Drive using raw download links ===
@st.cache_data
def load_csv_from_drive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    df = pd.read_csv(url)
    return df

df_2020 = load_csv_from_drive(FILE_IDS["2020"])
df_2023 = load_csv_from_drive(FILE_IDS["2023"])
df_2024 = load_csv_from_drive(FILE_IDS["2024"])

# === Column detection ===
tmk_col = next(col for col in df_2020.columns if "tmk" in col.lower())
lat_col = next(col for col in df_2020.columns if "lat" in col.lower())
lon_col = next(col for col in df_2020.columns if "lon" in col.lower())

# === Set logic ===
set_2020 = set(df_2020[tmk_col])
set_2023 = set(df_2023[tmk_col])
set_2024 = set(df_2024[tmk_col])

gone_after_2020 = set_2020 - set_2023 - set_2024
gone_after_2023 = set_2023 - set_2024
reappeared_2024 = (set_2020 - set_2023) & set_2024

# === Extract and label ===
def extract(df, ids, label):
    sub = df[df[tmk_col].isin(ids)].copy()
    sub["change"] = label
    return sub[[tmk_col, lat_col, lon_col, "change"]]

df_all = pd.concat([
    extract(df_2020, gone_after_2020, "Disappeared after 2020"),
    extract(df_2023, gone_after_2023, "Disappeared after 2023"),
    extract(df_2024, reappeared_2024, "Reappeared in 2024")
])

# === Map summary ===
st.markdown(f"""
### 📊 Summary
- 🟥 Disappeared after 2020: **{len(gone_after_2020):,}**
- 🟧 Disappeared after 2023: **{len(gone_after_2023):,}**
- 🟩 Reappeared in 2024: **{len(reappeared_2024):,}**
""")

# === Color map ===
color_map = {
    "Disappeared after 2020": [255, 0, 0, 150],
    "Disappeared after 2023": [255, 140, 0, 150],
    "Reappeared in 2024": [0, 200, 0, 150],
}

layers = [
    pdk.Layer(
        "ScatterplotLayer",
        data=df_all[df_all["change"] == label],
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

# === Export CSV ===
st.download_button("⬇️ Download CSV", df_all.to_csv(index=False), "missing_tmks.csv")
