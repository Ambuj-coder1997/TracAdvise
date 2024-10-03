import streamlit as st
import random
import time
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

# Function to generate parameters within given ranges
def generate_engine_speed():
    return random.randint(1200, 1800)

def generate_throttle_setting():
    return random.randint(45, 85)

def generate_implement_depth():
    return random.uniform(5, 45)

def generate_actual_forward_speed():
    return round(random.uniform(0.8, 4.5), 2)

def generate_heading():
    return round(random.uniform(0, 360), 2)

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
            background-color: white;
        }
        table {
            font-size: 20px;
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 10px;
        }
        th, td {
            padding: 10px;
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

    st.markdown("<h3 style='text-align: center; color: DarkGreen;'>Real-time Tractor Operating Parameters</h3>", unsafe_allow_html=True)

    # Dropdown for gear selection
    gear_options = {"L1": 160, "L2": 120, "L3": 80, "L4": 40, "H1": 30}
    gear = st.selectbox('Select the operating gear:', list(gear_options.keys()))
    x = gear_options[gear]

    # Initializing placeholders for output and map
    output_placeholder = st.empty()
    graph_placeholder = st.empty()
    map_placeholder = st.empty()

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
    heading_values = []

    start_time = datetime.now()

    while True:
        current_time = (datetime.now() - start_time).total_seconds()

        # Generate the parameters
        engine_speed = generate_engine_speed()
        throttle_setting = generate_throttle_setting()
        implement_depth = generate_implement_depth()
        actual_speed = generate_actual_forward_speed()
        heading = generate_heading()

        # Calculate Vt and slip
        Vt = engine_speed / x
        slip = 100 * (1 - ((actual_speed) / (Vt * 3.14 * 1.6 * (60 / 1000))))

        # Append data to the lists
        time_stamps.append(current_time)
        engine_speed_values.append(engine_speed)
        throttle_values.append(throttle_setting)
        implement_depth_values.append(implement_depth)
        forward_speed_values.append(actual_speed)
        slip_values.append(slip)
        heading_values.append(heading)

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

        # Split the layout into two columns
        col1, col2 = st.columns([1, 3])  # Left column is smaller than right column

        with col1:
            # Display the updated parameters in a table
            output_content = f"""
            <table>
                <tr><th>Parameter</th><th>Value</th></tr>
                <tr>
                    <td><img src='gear_icon.jpg' width='30' height='30'> Gear Ratio</td>
                    <td>{gear}</td>
                </tr>
                <tr>
                    <td><img src='engine_icon.jpg' width='30' height='30'> Engine Speed (rpm)</td>
                    <td>{engine_speed}</td>
                </tr>
                <tr>
                    <td><img src='throttle_icon.jpg' width='30' height='30'> Throttle Setting (%)</td>
                    <td>{throttle_setting}</td>
                </tr>
                <tr>
                    <td><img src='depth_icon.jpg' width='30' height='30'> Implement Depth (cm)</td>
                    <td>{implement_depth}</td>
                </tr>
                <tr>
                    <td><img src='speed_icon.jpg' width='30' height='30'> Actual Speed (km/h)</td>
                    <td>{actual_speed}</td>
                </tr>
                <tr>
                    <td><img src='slip_icon.jpg' width='30' height='30'> Slip (%)</td>
                    <td>{slip:.2f}</td>
                </tr>
                <tr>
                    <td><img src='heading_icon.jpg' width='30' height='30'> Heading (°)</td>
                    <td>{heading}</td>
                </tr>
                <tr>
                    <td><img src='gps_icon.jpg' width='30' height='30'> Latitude (N)</td>
                    <td>{current_lat}</td>
                </tr>
                <tr>
                    <td><img src='gps_icon.jpg' width='30' height='30'> Longitude (E)</td>
                    <td>{current_long}</td>
                </tr>
            </table>
            """
            output_placeholder.markdown(output_content, unsafe_allow_html=True)

        with col2:
            # Plot the real-time data on the right
            fig, ax = plt.subplots(5, 1, figsize=(10, 15), sharex=True)

            ax[0].plot(time_stamps, engine_speed_values, label="Engine Speed (rpm)", color='blue')
            ax[1].plot(time_stamps, throttle_values, label="Throttle Setting (%)", color='green')
            ax[2].plot(time_stamps, implement_depth_values, label="Implement Depth (cm)", color='purple')
            ax[3].plot(time_stamps, forward_speed_values, label="Actual Speed (km/h)", color='orange')
            ax[4].plot(time_stamps, slip_values, label="Slip (%)", color='red')

            for i, axis in enumerate(ax):
                axis.legend(loc="upper right")
                axis.grid(True)
            
            ax[-1].set_xlabel("Time (s)")

            with graph_placeholder:
                st.pyplot(fig)

        # Create and display satellite map below the graph
        m = folium.Map(location=[current_lat, current_long], zoom_start=15, tiles="Satellite", attr='© OpenStreetMap contributors')
        for coord in coordinates_list:
            folium.Marker(
                location=[coord['latitude'], coord['longitude']],
                popup=f"Lat: {coord['latitude']}, Long: {coord['longitude']}, Speed: {coord['speed']} km/h"
            ).add_to(m)
        with map_placeholder:
            folium_static(m, width=700, height=400)

        time.sleep(3)  # Refresh rate of 3 seconds

def show_gps_page():
    display_parameters()

# Call the GPS page to run the app
if __name__ == "__main__":
    show_gps_page()
