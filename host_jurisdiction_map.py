import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Extended dataset with subdomains from publicsearch.us and kofile.com
# Note: Coordinates are approximated for visualization purposes

full_data = [
    {"Domain": "govos.com", "Category": "recorder", "IP": "141.193.213.20", "Org": "WPENG", "ASN": "209242", "Flag": "⚠️ Non-US", "Lat": 32.7767, "Lon": -96.7970},
    {"Domain": "publicsearch.us", "Category": "recorder", "IP": "35.247.2.99", "Org": "GOOGLE-CLOUD", "ASN": "396982", "Flag": "⚠️ Non-US", "Lat": 40.7128, "Lon": -74.0060},
    {"Domain": "tylertech.com", "Category": "recorder", "IP": "3.82.237.29", "Org": "AMAZON-IAD", "ASN": "14618", "Flag": "⚠️ Non-US", "Lat": 38.9072, "Lon": -77.0369},
    {"Domain": "kofile.com", "Category": "recorder", "IP": "104.196.199.136", "Org": "GOOGLE-CLOUD", "ASN": "396982", "Flag": "⚠️ Non-US", "Lat": 30.2672, "Lon": -97.7431},
    {"Domain": "fnf.com", "Category": "mortgage", "IP": "172.200.144.121", "Org": "UK-MICROSOFT-20000324", "ASN": "8075", "Flag": "⚠️ Non-US", "Lat": 51.509865, "Lon": -0.118092},

    # Example subdomains added
    {"Domain": "bexartx.search.kofile.com", "Category": "recorder", "IP": "104.42.21.90", "Org": "KOFILE", "ASN": "???", "Flag": "⚠️ Non-US", "Lat": 29.4241, "Lon": -98.4936},  # San Antonio
    {"Domain": "freestonetx.search.kofile.com", "Category": "recorder", "IP": "104.42.21.90", "Org": "KOFILE", "ASN": "???", "Flag": "⚠️ Non-US", "Lat": 31.7246, "Lon": -96.1653},  # Freestone TX
    {"Domain": "clerk.boulder.co.publicsearch.us", "Category": "recorder", "IP": "34.83.72.72", "Org": "GOOGLE-CLOUD", "ASN": "396982", "Flag": "⚠️ Non-US", "Lat": 40.015, "Lon": -105.2705},
    {"Domain": "admin.kennebec.me.publicsearch.us", "Category": "recorder", "IP": "34.83.72.72", "Org": "GOOGLE-CLOUD", "ASN": "396982", "Flag": "⚠️ Non-US", "Lat": 44.4334, "Lon": -69.7179},
    {"Domain": "admin.franklin.oh.publicsearch.us", "Category": "recorder", "IP": "34.83.72.72", "Org": "GOOGLE-CLOUD", "ASN": "396982", "Flag": "⚠️ Non-US", "Lat": 39.9612, "Lon": -82.9988},
]

category_colors = {
    "recorder": "blue",
    "mortgage": "red",
    "court": "green",
    "public figure": "orange",
    "pdf software": "purple"
}

st.title("⚖️ Website Hosting Location Map")
st.markdown("This map displays recorder, court, and mortgage-related sites and their server hosting locations.")

# Create Folium map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

for entry in full_data:
    folium.CircleMarker(
        location=[entry["Lat"], entry["Lon"]],
        radius=6,
        color=category_colors.get(entry["Category"], "gray"),
        fill=True,
        fill_opacity=0.7,
        popup=f"{entry['Domain']}<br>Org: {entry['Org']}<br>ASN: {entry['ASN']}<br>Flag: {entry['Flag']}",
    ).add_to(m)

# Add map legend manually using HTML
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 180px; height: 150px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;">
     &nbsp;<b>Legend</b><br>
     &nbsp;<span style='color:blue'>&#11044;</span> Recorder<br>
     &nbsp;<span style='color:red'>&#11044;</span> Mortgage<br>
     &nbsp;<span style='color:green'>&#11044;</span> Court<br>
     &nbsp;<span style='color:orange'>&#11044;</span> Public Figure<br>
     &nbsp;<span style='color:purple'>&#11044;</span> PDF Software
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

folium_static(m)
