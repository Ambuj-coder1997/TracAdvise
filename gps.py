import streamlit as st
import random
import time
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import numpy as np

# Function to generate parameters within given ranges
def generate_engine_speed():
    return random.randint(1200, 1800)

def generate_throttle_setting():
    return random.randint(45, 85)

def generate_implement_depth():
    return random.uniform(5, 45)

def generate_actual_forward_speed():
    return round(random.uniform(0.8, 4.5), 2)

# Generate latitude and longitude
def generate_latitude(current_lat):
    return current_lat + random.uniform(-0.0001, 0.0001)

def generate_longitude(current_long):
    return current_long + random.uniform(-0.0001, 0.0001)

# Main function to display tractor parameters
def display_parameters():
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f5f5;
        }
        table {
            font-size: 20px;
            border-collapse: collapse;
            width: 50%;
            margin-bottom: 10px;
            margin-left: auto;
            margin-right: auto;
        }
        th, td {
            padding: 0px;
            text-align: center;
        }
        th {
            background-color: #009688;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Heading with font and style changes
    st.markdown("<h1 style='text-align: center; color: DarkGreen; font-family: Arial; font-size: 36px;'>Real-time Tractor Operating Parameters</h1>", unsafe_allow_html=True)

    # Dropdown for gear selection
    gear_options = {"L1": 160, "L2": 120, "L3": 80, "L4": 40, "H1": 30}
    gear = st.selectbox('Select the operating gear:', list(gear_options.keys()))
    x = gear_options[gear]

    # Initializing placeholders for output, graphs, and map
    output_placeholder = st.empty()

    current_lat = 22.31278
    current_long = 87.33152
    coordinates_list = []

    # Variables to store time for graphing
    time_stamps = []
    engine_speed_values = []
    throttle_values = []
    implement_depth_values = []
    forward_speed_values = []
    slip_values = []

    start_time = datetime.now()

    while True:
        current_time = (datetime.now() - start_time).total_seconds()

        # Generate the parameters
        engine_speed = generate_engine_speed()
        throttle_setting = generate_throttle_setting()
        implement_depth = generate_implement_depth()
        actual_speed = generate_actual_forward_speed()

        # Calculate Vt and slip
        Vt = engine_speed / x
        slip = 100 * (1 - ((actual_speed)/(Vt*3.14*1.6*(60/1000)))

        # Append data to the lists
        time_stamps.append(current_time)
        engine_speed_values.append(engine_speed)
        throttle_values.append(throttle_setting)
        implement_depth_values.append(implement_depth)
        forward_speed_values.append(actual_speed)
        slip_values.append(slip)

        # Update GPS coordinates
        current_lat = generate_latitude(current_lat)
        current_long = generate_longitude(current_long)
        coordinates_list.append({
            'latitude': current_lat,
            'longitude': current_long,
            'timestamp': datetime.now(),
            'speed': actual_speed
        })

        # Remove coordinates older than 10 seconds
        coordinates_list = [
            coord for coord in coordinates_list
            if coord['timestamp'] > datetime.now() - timedelta(seconds=10)
        ]

        # Generate real-time graphs for each parameter
        fig, ax = plt.subplots(5, 1, figsize=(10, 15), sharex=True)

        for i, (values, label, color) in enumerate(zip(
                [engine_speed_values, throttle_values, implement_depth_values, forward_speed_values, slip_values],
                ["Engine Speed (rpm)", "Throttle Setting (%)", "Implement Depth (cm)", "Actual Speed (km/h)", "Slip (%)"],
                ['blue', 'green', 'purple', 'orange', 'red']
        )):
            ax[i].plot(time_stamps, values, label=label, color=color, marker='o')  # Dot on latest value
            ax[i].fill_between(time_stamps, values, color=color, alpha=0.2)  # Shading
            ax[i].legend(loc="upper right")
            ax[i].grid(True)

        ax[-1].set_xlabel("Time (s)")
        st.pyplot(fig)

        # Prepare the HTML table with plots and map
        output_content = f"""
        <table>
            <tr><th>Parameter</th><th>Value</th><th>Variation Plot</th></tr>
            <tr>
                <td>Gear Ratio</td>
                <td>{gear}</td>
                <td rowspan="6"><img src='variation_graph.png' width='400' height='300'></td>
            </tr>
            <tr>
                <td>Engine Speed (rpm)</td>
                <td>{engine_speed}</td>
            </tr>
            <tr>
                <td>Throttle Setting (%)</td>
                <td>{throttle_setting}</td>
            </tr>
            <tr>
                <td>Implement Depth (cm)</td>
                <td>{implement_depth}</td>
            </tr>
            <tr>
                <td>Actual Speed (km/h)</td>
                <td>{actual_speed}</td>
            </tr>
            <tr>
                <td>Slip (%)</td>
                <td>{slip:.2f}</td>
            </tr>
            <tr>
                <td>GPS Coordinates</td>
                <td>Lat: {current_lat}, Long: {current_long}</td>
                <td rowspan="2"><img src='map.png' width='400' height='300'></td>
            </tr>
        </table>
        """
        output_placeholder.markdown(output_content, unsafe_allow_html=True)

        # Create and display map
        m = folium.Map(location=[current_lat, current_long], zoom_start=15)
        for coord in coordinates_list:
            folium.Marker(
                location=[coord['latitude'], coord['longitude']],
                popup=f"Lat: {coord['latitude']}, Long: {coord['longitude']}, Speed: {coord['speed']} km/h"
            ).add_to(m)
        folium_static(m, width=700, height=500)

        time.sleep(3)  # Refresh rate of 3 seconds

def show_gps_page():
    display_parameters()

# Call the GPS page to run the app
if __name__ == "__main__":
    show_gps_page()
