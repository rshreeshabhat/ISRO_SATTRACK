import os
import requests
import streamlit as st
import pandas as pd
import pydeck as pdk
from dotenv import load_dotenv

# Load environment variables (because API keys shouldn't be hard-coded)
load_dotenv()
API_KEY = os.getenv("N2YO_API_KEY")

# Streamlit app title
st.title("ISRO Satellite Tracker")

# Satellite data (ID mappings for selected ISRO satellites)
satellites = {
    "Cartosat-2A": 32783, "Cartosat-2B": 36839, "Cartosat-2C": 41599,
    "Cartosat-2D": 42063, "Cartosat-2E": 42747, "Cartosat-2F": 43111,
    "INSAT-3A": 27714, "INSAT-3C": 27298, "INSAT-4A": 28911, "INSAT-4B": 30793,
    "INSAT-4CR": 32050, "GSAT-6A": 43241, "GSAT-7": 39234, "GSAT-10": 38778,
    "GSAT-12": 37746, "GSAT-16": 40332, "GSAT-18": 41793, "RISAT-1": 38337,
    "RISAT-2": 34807, "IRNSS-1A": 39199, "IRNSS-1B": 39635, "IRNSS-1C": 40269,
    "IRNSS-1D": 40547, "IRNSS-1E": 41384, "IRNSS-1F": 41469, "IRNSS-1G": 41589,
    "Chandrayaan-2 Orbiter": 44426
}

# Satellite colors to distinguish between satellites
satellite_colors = {
    "Cartosat-2A": [255, 0, 0],"Cartosat-2B": [0, 255, 0],"Cartosat-2C": [0, 0, 255],"Cartosat-2D": [255, 255, 0],
    "Cartosat-2E": [255, 0, 255],"Cartosat-2F": [0, 255, 255],"INSAT-3A": [255, 165, 0],"INSAT-3C": [128, 0, 128],
    "INSAT-4A": [0, 128, 128],"INSAT-4B": [128, 128, 0],"INSAT-4CR": [0, 0, 128],"GSAT-6A": [192, 192, 192],
    "GSAT-7": [128, 128, 128],"GSAT-10": [0, 255, 127],"GSAT-12": [255, 20, 147],"GSAT-16": [123, 104, 238],
    "GSAT-18": [65, 105, 225],"RISAT-1": [106, 90, 205],"RISAT-2": [220, 20, 60],"IRNSS-1A": [255, 99, 71],
    "IRNSS-1B": [32, 178, 170],"IRNSS-1C": [107, 142, 35],"IRNSS-1D": [255, 215, 0], "IRNSS-1E": [154, 205, 50],
    "IRNSS-1F": [255, 140, 0],"IRNSS-1G": [233, 150, 122],"Chandrayaan-2 Orbiter": [72, 61, 139]  
}

# Satellite selection section
st.subheader("Select Satellites to Display on the Map:")

# Create a grid of checkboxes for satellite selection
cols = st.columns(4)  # Display checkboxes in 4 columns
selected_satellites = {}
for idx, sat_name in enumerate(satellites.keys()):
    if cols[idx % 4].checkbox(sat_name, value=True):
        selected_satellites[sat_name] = satellites[sat_name]

# Fetch data from the API with error handling
def fetch_satellite_data(satellite_ids):
    satellite_data = []
    for sat_name, sat_id in satellite_ids.items():
        try:
            url = f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/41.702/-76.014/0/2/&apiKey={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()  # Handle HTTP errors
            data = response.json()

            if 'positions' in data:
                position = data['positions'][0]
                satellite_data.append({
                    'name': sat_name,
                    'latitude': position.get('satlatitude', 'N/A'),
                    'longitude': position.get('satlongitude', 'N/A'),
                    'color': satellite_colors[sat_name]
                })
            else:
                st.write(f"⚠️ Unable to fetch data for {sat_name}. Please try again later.")
        except requests.exceptions.RequestException as e:
            st.write(f"⚠️ Unable to fetch data for {sat_name}. Please try again later.")
    return satellite_data

# Fetch data for selected satellites
satellite_data = fetch_satellite_data(selected_satellites)

# Plot the map if data is available
if satellite_data:
    df = pd.DataFrame(satellite_data)
    
    # Create a scatterplot layer for pydeck
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[longitude, latitude]',
        get_fill_color='color', 
        get_radius=50000,
        pickable=True  # Allows clicking on satellite markers for details
    )

    # Define the map view state (initial position and zoom level)
    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=3,
        pitch=0
    )

    # Render the map using pydeck
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}"}))
else:
    st.write("No data available.")  # Display a message if no data is fetched
