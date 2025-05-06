import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="💰 Missing Parcel Map")

# --- Title Banner ---
st.markdown("""
    <div style="background-color:#111827;padding:20px 30px;border-radius:10px;margin-bottom:20px">
        <h2 style="color:white;margin:0">💰 HAWAIʻI LAND DISAPPEARANCE MAP</h2>
        <p style="color:#d1d5db;margin:0;font-size:18px">
        $128,000,000,000 in Missing Parcel Value · 2020–2024
        </p>
        <p style="color:#9ca3af;margin:0;font-size:15px">Source: Forensic Audit of TMK Shapefiles · WCI Obfuscation Index v5.4</p>
    </div>
""", unsafe_allow_html=True)

# --- Load CSV from Google Drive ---
CSV_FILE_ID = "1eEFL1uyAr16SLGBE7KaZZj_hjiuXkpzt"  # Replace with your file ID
csv_url = f"https://drive.google.com/uc?export=download&id={CSV_FILE_ID}"
df = pd.read_csv(csv_url)

# --- Clean Columns ---
df.columns = df.columns.str.strip()
df = df.dropna(subset=['Latitude', 'Longitude'])

# --- Build Folium Map ---
m = folium.Map(location=[21.3, -157.85], zoom_start=12, control_scale=True, tiles="OpenStreetMap")

# --- Add Parcel Markers ---
for _, row in df.iterrows():
    popup = f"""
    <b>Grantor:</b> {row['Grantor']}<br>
    <b>Grantee:</b> {row['Grantee']}<br>
    <b>Amount:</b> {row['Amount']}<br>
    <b>Date:</b> {row['Date']}<br>
    <b>Bank:</b> {row['Bank']}<br>
    <b>Country:</b> {row['Country']}<br>
    <b>WCI Escrow:</b> {row['WCI Escrow Number']}<br>
    <b>WCI Certificate:</b> {row['WCI Certificate Number']}<br>
    <b>Doc:</b> <a href="{row['Link']}" target="_blank">{row['Document']}</a>
    """
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6,
        color='blue',
        fill=True,
        fill_opacity=0.9,
        popup=folium.Popup(popup, max_width=350)
    ).add_to(m)

# --- DLNR Marker ---
folium.CircleMarker(
    location=[21.310440, -157.871794],
    radius=12,
    color='red',
    fill=True,
    fill_opacity=0.9,
    tooltip="New Location of DLNR"
).add_to(m)

# --- Display Map ---
st.markdown("### 🗺️ Map of Missing Government Parcels")
st.markdown(f"**Total Transactions Mapped:** {len(df)}")
st_folium(m, width=1200, height=700)

# --- Download Button ---
st.markdown(f"""
    <div style='position: fixed; bottom: 20px; right: 20px;'>
        <a href="{csv_url}" download="transactions.csv">
            <button style='padding:10px 20px; font-size:16px;'>⬇ Download CSV</button>
        </a>
    </div>
""", unsafe_allow_html=True)
