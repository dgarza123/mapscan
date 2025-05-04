import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# -------------------------------
# 🚨 Embedded Sample Data
# -------------------------------
data = [
    {"URL": "https://recorder.maricopa.gov", "Domain": "recorder.maricopa.gov", "IP": "104.18.36.57", "Hosting Org": "CLOUDFLARENET", "ASN": "13335", "Country": "None", "Type": "Recorder", "Latitude": 37.751, "Longitude": -97.822, "Jurisdiction Flag": "⚠️ Non-US"},
    {"URL": "https://tulsigabbard.com", "Domain": "tulsigabbard.com", "IP": "104.21.64.1", "Hosting Org": "CLOUDFLARENET", "ASN": "13335", "Country": "None", "Type": "Public Figure", "Latitude": 37.751, "Longitude": -97.822, "Jurisdiction Flag": "⚠️ Non-US"},
    {"URL": "https://arapahoe.co.publicsearch.us/", "Domain": "arapahoe.co.publicsearch.us", "IP": "35.247.2.99", "Hosting Org": "GOOGLE-CLOUD", "ASN": "396982", "Country": "None", "Type": "Recorder", "Latitude": 37.751, "Longitude": -97.822, "Jurisdiction Flag": "⚠️ Non-US"},
    {"URL": "http://jimspss1.courts.state.hi.us:8080", "Domain": "jimspss1.courts.state.hi.us", "IP": "162.221.245.181", "Hosting Org": "STATE-OF-HAWAII", "ASN": "62712", "Country": "None", "Type": "Court", "Latitude": 21.307, "Longitude": -157.858, "Jurisdiction Flag": "⚠️ Non-US"},
    {"URL": "https://bocdataext.hi.wcicloud.com", "Domain": "bocdataext.hi.wcicloud.com", "IP": "20.47.116.33", "Hosting Org": "MSFT", "ASN": "8069", "Country": "None", "Type": "Recorder", "Latitude": 47.6097, "Longitude": -122.3331, "Jurisdiction Flag": "⚠️ Non-US"},
    {"URL": "https://loandepot.com", "Domain": "loandepot.com", "IP": "104.18.24.94", "Hosting Org": "CLOUDFLARENET", "ASN": "13335", "Country": "None", "Type": "Mortgage", "Latitude": 33.7175, "Longitude": -117.8311, "Jurisdiction Flag": "⚠️ Non-US"},
]

df = pd.DataFrame(data)

# -------------------------------
# 🌍 Create Map
# -------------------------------
st.title("🌐 Hosting Jurisdiction Map")
st.markdown("Shows domains of courts, recorders, and mortgage companies with hosting geolocation and flags for ⚠️ non-U.S. jurisdiction.")

map_center = [37.5, -98.0]
m = folium.Map(location=map_center, zoom_start=4)
marker_cluster = MarkerCluster().add_to(m)

# 🎨 Marker color by category
def get_marker_color(category):
    return {
        "Court": "purple",
        "Recorder": "red",
        "Mortgage": "blue",
        "Public Figure": "orange"
    }.get(category, "gray")

for _, row in df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(f"""<b>{row['Domain']}</b><br>
            Type: {row['Type']}<br>
            IP: {row['IP']}<br>
            Host: {row['Hosting Org']}<br>
            ASN: {row['ASN']}<br>
            {row['Jurisdiction Flag']}""", max_width=250),
        icon=folium.Icon(color=get_marker_color(row["Type"]))
    ).add_to(marker_cluster)

st_folium(m, width=800, height=600)

# 📁 Optional download
csv = df.to_csv(index=False)
st.download_button("⬇️ Download Data as CSV", csv, "hosting_map_data.csv", "text/csv")
