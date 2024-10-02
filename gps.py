import streamlit as st
import random
import time
from datetime import datetime
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

# Function to display the graphs
def plot_graph(time_stamps, values, label, color, future_values=None, future_time_stamps=None):
    fig, ax = plt.subplots()
    ax.plot(time_stamps, values, label=label, color=color, marker='o')  # Dot on latest value
    ax.fill_between(time_stamps, values, color=color, alpha=0.2)  # Shaded region
    
    if future_values and future_time_stamps:
        ax.plot(future_time_stamps, future_values, label=f'Future {label}', linestyle='--', color='gray')
    
    ax.set_title(label)
    ax.grid(True)
    return fig

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
            width: 100%;
            margin-bottom: 10px;
            margin-left: auto;
            margin-right: auto;
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

    # Heading with font and style changes
    st.markdown("<h1 style='text-align: center; color: DarkGreen; font-family: Arial; font-size: 36px;'>Real-time Tractor Operating Parameters</h1>", unsafe_allow_html=True)

    # Dropdown for gear selection
    gear_options = {"L1": 160, "L2": 120, "L3": 80, "L4": 40, "H1": 30}
    gear = st.selectbox('Select the operating gear:', list(gear_options.keys()))
    x = gear_options[gear]

    # Initializing placeholders for output, graphs, and map
    output_placeholder = st.empty()
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

    start_time = datetime.now()

    # Create the map once and reuse it
    m = folium.Map(location=[current_lat, current_long], zoom_start=15)
    marker = folium.Marker(location=[current_lat, current_long])
    marker.add_to(m)
    
    # Placeholder for the map within the table
    map_placeholder.markdown("<div id='mapid'></div>", unsafe_allow_html=True)
    folium_static(m, width=400, height=300)

    while True:
        current_time = (datetime.now() - start_time).total_seconds()

        # Generate the parameters
        engine_speed = generate_engine_speed()
        throttle_setting = generate_throttle_setting()
        implement_depth = generate_implement_depth()
        actual_speed = generate_actual_forward_speed()

        # Calculate Vt and slip
        Vt = engine_speed / x
        slip = 100 * (1 - (actual_speed / Vt))

        # Append data to the lists
        time_stamps.append(current_time)
        engine_speed_values.append(engine_speed)
        throttle_values.append(throttle_setting)
        implement_depth_values.append(implement_depth)
        forward_speed_values.append(actual_speed)
        slip_values.append(slip)

        # Predict future values (dummy prediction for demonstration)
        future_time_stamps = [current_time + i for i in range(1, 6)]
        future_values = [v * (1 + random.uniform(-0.05, 0.05)) for v in engine_speed_values[-5:]]

        # Update GPS coordinates dynamically without refreshing the map
        current_lat = generate_latitude(current_lat)
        current_long = generate_longitude(current_long)
        coordinates_list.append({
            'latitude': current_lat,
            'longitude': current_long,
            'timestamp': datetime.now(),
            'speed': actual_speed
        })

        # Update the marker's position
        marker.location = [current_lat, current_long]

        # Icons for each parameter (replace with actual image paths)
        engine_icon = 'engine_icon.jpg'
        throttle_icon = 'throttle_icon.jpg'
        depth_icon = 'depth_icon.jpg'
        speed_icon = 'speed_icon.jpg'
        slip_icon = 'slip_icon.jpg'
        gps_icon = 'gps_icon.jpg'

        # Create the plots inside the table
        engine_fig = plot_graph(time_stamps, engine_speed_values, "Engine Speed (rpm)", 'blue', future_values, future_time_stamps)
        throttle_fig = plot_graph(time_stamps, throttle_values, "Throttle Setting (%)", 'green')
        depth_fig = plot_graph(time_stamps, implement_depth_values, "Implement Depth (cm)", 'purple')
        speed_fig = plot_graph(time_stamps, forward_speed_values, "Actual Speed (km/h)", 'orange')
        slip_fig = plot_graph(time_stamps, slip_values, "Slip (%)", 'red')

        # Display the parameter table with icons and plots
        st.markdown("""
        <table>
            <tr>
                <th>Parameter</th>
                <th>Icon</th>
                <th>Value</th>
                <th>Variation Plot</th>
            </tr>
            <tr>
                <td>Engine Speed (rpm)</td>
                <td><img src='{}' width='50'></td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Throttle Setting (%)</td>
                <td><img src='{}' width='50'></td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Implement Depth (cm)</td>
                <td><img src='{}' width='50'></td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Actual Speed (km/h)</td>
                <td><img src='{}' width='50'></td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Slip (%)</td>
                <td><img src='{}' width='50'></td>
                <td>{:.2f}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>GPS Coordinates</td>
                <td><img src='{}' width='50'></td>
                <td>Lat: {}, Long: {}</td>
                <td rowspan="2"><div id='mapid'></div></td>
            </tr>
        </table>
        """.format(
            engine_icon, engine_speed, st.pyplot(engine_fig),
            throttle_icon, throttle_setting, st.pyplot(throttle_fig),
            depth_icon, implement_depth, st.pyplot(depth_fig),
            speed_icon, actual_speed, st.pyplot(speed_fig),
            slip_icon, slip, st.pyplot(slip_fig),
            gps_icon, current_lat, current_long
        ), unsafe_allow_html=True
        )

        # Sleep to simulate real-time updates
        time.sleep(3)

# Call the GPS page to run the app
if __name__ == "__main__":
    display_parameters()
