import streamlit as st
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Import values from the gps.py page
from gps import throttle_values, engine_speed_values, implement_depth_values, forward_speed_values, slip_values

# Icon paths for the table
icon_url = {
    "Engine Torque": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQhkTm5C6-djVM3yJ6DZ--Yc3axxHSxT8RHVYB4Dthor-vWVhc4",
    "Fuel Consumption": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqc4p4DyeU5I0AzNnl7w1rYwsQrq3vV4ylviuU9JSy7g63vv0L",
    "Engine Power": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT0tSZjxD2nNXkGho7aCY3RdK-2SKylAUgV_XXxGGvnb3nIqhmq",
    "Specific Fuel Consumption": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXJIQWbLE_0DwM4BmilBbQIFC08CrGHqnKgMZM4Gv6YjuF0DdK",
    "Fuel Consumption per Tilled Area": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSUYRAAJNfkU0TtLoT7qmjouHO46frWiqYOppmIGytCzbORik9",
    "Implement Draft": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfbucYctsmUEAm34Ja4Xxgb1nVtv5comnkGPqqvwJVJAl7L0RY",
    "Drawbar Power": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkoQm9oof_qXb12jIbTZI3U5iI5MRV21ONG9GoW0LI65XZ1svq",
    "Tractive Efficiency": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8mr5HjL2hNmNZzCD63O5KszeL0khnYGNUd09ang3WgtXCUCZm",
}

# Function to calculate additional parameters based on imported values
def calculate_parameters():
    parameters = []

    for i in range(len(throttle_values)):
        # Calculate z and r
        z = 24.49 * throttle_values[i] + 42.483
        r = z - engine_speed_values[i]

        # Engine torque (Nm)
        ent = (
            (r ** 3 * z ** 2) * (8.5558 * pow(10, -13)) +
            (r ** 2 * z ** 2) * (-5.086 * pow(10, -9)) +
            (r * z ** 2) * (3.1619 * pow(10, -7)) +
            (r ** 3 * z) * (-1.909 * pow(10, -8)) +
            (r ** 2 * z) * (1.5683 * pow(10, -5)) +
            (r * z) * (-0.000435357) + 5.93541932
        )

        # Fuel consumption (L/h)
        fcp = (
            (z ** 3 * r ** 2) * (-2.2978 * pow(10, -25)) +
            (z ** 2 * r ** 2) * (-3.0631 * pow(10, -11)) +
            (z ** 3 * r) * (-5.2523 * pow(10, -23)) +
            (z ** 2 * r) * (1.60046 * pow(10, -8)) +
            (z ** 3) * (-5.60937 * pow(10, -21)) + 1.342006549
        )

        # Engine power (hp)
        enp = (2 * 3.14 * engine_speed_values[i] * ent) / (60 * 746)

        # Specific fuel consumption (kg/hp-hr)
        sfc = (fcp * 840) / enp if enp != 0 else 0

        # Fuel consumption per tilled area (L/ha)
        FC = (fcp * 10) / (0.6 * forward_speed_values[i]) if forward_speed_values[i] != 0 else 0

        # Implement draft (kN)
        draft = 0.78 * (652 + 5.1 * forward_speed_values[i] ** 2) * 0.6 * implement_depth_values[i]

        # Drawbar power (dbp)
        dbp = 0.3723 * (draft * forward_speed_values[i])

        # Tractive efficiency (%)
        te = dbp * (100 - slip_values[i]) / (0.9 * enp) if enp != 0 else 0

        # Store calculated values
        parameters.append({
            'engine_torque': ent,
            'fuel_consumption': fcp,
            'engine_power': enp,
            'specific_fuel_consumption': sfc,
            'fuel_consumption_area': FC,
            'implement_draft': draft,
            'drawbar_power': dbp,
            'tractive_efficiency': te
        })

    return parameters

# Main function to display tractor parameters
def display_parameters():
    st.markdown(
        """
        <style>
        /* Set entire app background color to white */
        .main {
            background-color: white;
        }

        /* Set the table font and formatting */
        table {
            font-size: 25px;
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 10px;
        }

        th, td {
            padding: 10px;
            text-align: center;
        }

        th {
            background-color: white;
            color: black;
        }

        /* Change background color of the table to white */
        table, th, td {
            background-color: white;
        }

        h3 {
            text-align: center;
            color: black;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h3>Real-time Tractor Operating Parameters</h3>", unsafe_allow_html=True)

    # Initialize placeholders for output and graph
    output_placeholder = st.empty()
    graph_placeholder = st.empty()

    # Calculate all the parameters
    calculated_parameters = calculate_parameters()

    time_stamps = list(range(len(throttle_values)))  # Using index as timestamps for simplicity

    # Display the table
    table_content = f"""
    <table>
        <tr><th>Parameter</th><th>Value</th></tr>
    """
    for i, params in enumerate(calculated_parameters):
        table_content += f"""
        <tr>
            <td><img src="{icon_url['Engine Torque']}" width="30"> Engine Torque (Nm)</td>
            <td>{params['engine_torque']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Fuel Consumption']}" width="30"> Fuel Consumption (L/h)</td>
            <td>{params['fuel_consumption']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Engine Power']}" width="30"> Engine Power (hp)</td>
            <td>{params['engine_power']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Specific Fuel Consumption']}" width="30"> Specific Fuel Consumption (kg/hp-hr)</td>
            <td>{params['specific_fuel_consumption']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Fuel Consumption per Tilled Area']}" width="30"> Fuel Consumption per Tilled Area (L/ha)</td>
            <td>{params['fuel_consumption_area']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Implement Draft']}" width="30"> Implement Draft (kN)</td>
            <td>{params['implement_draft']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Drawbar Power']}" width="30"> Drawbar Power (kW)</td>
            <td>{params['drawbar_power']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Tractive Efficiency']}" width="30"> Tractive Efficiency (%)</td>
            <td>{params['tractive_efficiency']:.2f}</td>
        </tr>
        """
    table_content += "</table>"

    output_placeholder.markdown(table_content, unsafe_allow_html=True)

    # Plot the real-time data on the right with dots and shaded areas
    fig, ax = plt.subplots(5, 1, figsize=(10, 15), sharex=True)

    ax[0].plot(time_stamps, throttle_values, label="Throttle Setting (%)", color='green', marker='o')
    ax[0].fill_between(time_stamps, throttle_values, color='green', alpha=0.2)

    ax[1].plot(time_stamps, engine_speed_values, label="Engine Speed (rpm)", color='blue', marker='o')
    ax[1].fill_between(time_stamps, engine_speed_values, color='blue', alpha=0.2)

    ax[2].plot(time_stamps, forward_speed_values, label="Actual Speed (km/h)", color='orange', marker='o')
    ax[2].fill_between(time_stamps, forward_speed_values, color='orange', alpha=0.2)

    ax[3].plot(time_stamps, implement_depth_values, label="Implement Depth (cm)", color='purple', marker='o')
    ax[3].fill_between(time_stamps, implement_depth_values, color='purple', alpha=0.2)

    ax[4].plot(time_stamps, slip_values, label="Slip (%)", color='red', marker='o')
    ax[4].fill_between(time_stamps, slip_values, color='red', alpha=0.2)

    for axis in ax:
        axis.legend(loc="upper right")
        axis.grid(True)

    ax[-1].set_xlabel("Time")

    # Display plot
    graph_placeholder.pyplot(fig)

# Call the GPS page to run the app
if __name__ == "__main__":
    display_parameters()
