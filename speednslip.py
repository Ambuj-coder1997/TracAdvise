import streamlit as st
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Random generation functions for tractor parameters
def generate_throttle_values():
    return random.randint(45, 85)

def generate_engine_speed_values():
    return random.randint(1200, 1800)

def generate_implement_depth_values():
    return round(random.uniform(5, 45), 2)

def generate_forward_speed_values():
    return round(random.uniform(0.8, 4.5), 2)

# Function to calculate slip percentage
def calculate_slip(engine_speed, forward_speed, gear_ratio):
    Vt = engine_speed / gear_ratio  # Calculate theoretical speed
    slip = 100 * (1 - (forward_speed / Vt))  # Calculate slip percentage
    return round(slip, 2)

# Gear ratios (as per the provided list)
gear_ratios = [160, 120, 80, 40, 30]

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

# Function to generate values and calculate parameters
def calculate_parameters():
    throttle_values = []
    engine_speed_values = []
    forward_speed_values = []
    implement_depth_values = []
    slip_values = []
    
    parameters = []

    for _ in range(10):
        throttle = generate_throttle_values()
        engine_speed = generate_engine_speed_values()
        forward_speed = generate_forward_speed_values()
        implement_depth = generate_implement_depth_values()
        gear_ratio = random.choice(gear_ratios)

        slip = calculate_slip(engine_speed, forward_speed, gear_ratio)

        # Append generated values for graphing
        throttle_values.append(throttle)
        engine_speed_values.append(engine_speed)
        forward_speed_values.append(forward_speed)
        implement_depth_values.append(implement_depth)
        slip_values.append(slip)

        # Calculate engine torque (Nm)
        z = 24.49 * throttle + 42.483
        r = z - engine_speed

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
        enp = (2 * 3.14 * engine_speed * ent) / (60 * 746)

        # Specific fuel consumption (kg/hp-hr)
        sfc = (fcp * 840) / enp if enp != 0 else 0

        # Fuel consumption per tilled area (L/ha)
        FC = (fcp * 10) / (0.6 * forward_speed) if forward_speed != 0 else 0

        # Implement draft (kN)
        draft = 0.78 * (652 + 5.1 * forward_speed ** 2) * 0.6 * implement_depth

        # Drawbar power (hp)
        dbp = 0.3723 * (draft * forward_speed)

        # Tractive efficiency (%)
        te = dbp * (100 - slip) / (0.9 * enp) if enp != 0 else 0

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

    return parameters, throttle_values, engine_speed_values, forward_speed_values, implement_depth_values, slip_values

# Main function to display tractor parameters
def display_parameters():
    st.markdown(
        """
        <style>
        .main {
            background-color: white;
        }
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

    st.markdown("<h1>Real-time Tractor Performance Prediction</h1>", unsafe_allow_html=True)

    # Initialize placeholders for output and graph
    output_placeholder = st.empty()
    graph_placeholder = st.empty()

    # Calculate all the parameters
    calculated_parameters, throttle_values, engine_speed_values, forward_speed_values, implement_depth_values, slip_values = calculate_parameters()

    time_stamps = list(range(len(throttle_values)))

    # Display the table
    table_content = f"""
    <table>
        <tr><th>Parameter</th><th>Value</th></tr>
    """
    for i, params in enumerate(calculated_parameters):
        table_content += f"""
        <tr>
            <td><img src="{icon_url['Engine Torque']}" width="50"> Engine Torque (Nm)</td>
            <td>{params['engine_torque']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Fuel Consumption']}" width="50"> Fuel Consumption (L/h)</td>
            <td>{params['fuel_consumption']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Engine Power']}" width="50"> Engine Power (hp)</td>
            <td>{params['engine_power']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Specific Fuel Consumption']}" width="50"> Specific Fuel Consumption (kg/hp-hr)</td>
            <td>{params['specific_fuel_consumption']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Fuel Consumption per Tilled Area']}" width="50"> Fuel Consumption per Tilled Area (L/ha)</td>
            <td>{params['fuel_consumption_area']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Implement Draft']}" width="50"> Implement Draft (kN)</td>
            <td>{params['implement_draft']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Drawbar Power']}" width="50"> Drawbar Power (hp)</td>
            <td>{params['drawbar_power']:.2f}</td>
        </tr>
        <tr>
            <td><img src="{icon_url['Tractive Efficiency']}" width="50"> Tractive Efficiency (%)</td>
            <td>{params['tractive_efficiency']:.2f}</td>
        </tr>
        """
    table_content += "</table>"

    output_placeholder.markdown(table_content, unsafe_allow_html=True)

    # Extract parameters for plotting
    engine_torque = [params['engine_torque'] for params in calculated_parameters]
    fuel_consumption = [params['fuel_consumption'] for params in calculated_parameters]
    engine_power = [params['engine_power'] for params in calculated_parameters]
    specific_fuel_consumption = [params['specific_fuel_consumption'] for params in calculated_parameters]
    fuel_consumption_area = [params['fuel_consumption_area'] for params in calculated_parameters]
    implement_draft = [params['implement_draft'] for params in calculated_parameters]
    drawbar_power = [params['drawbar_power'] for params in calculated_parameters]
    tractive_efficiency = [params['tractive_efficiency'] for params in calculated_parameters]

    # Plot the real-time data on the right with dots and shaded areas
    fig, ax = plt.subplots(8, 1, figsize=(10, 15), sharex=True)

    ax[0].plot(time_stamps, engine_torque, label="Engine Torque (Nm)", color='green', marker='o')
    ax[0].fill_between(time_stamps, engine_torque, color='green', alpha=0.2)

    ax[1].plot(time_stamps, fuel_consumption, label="Fuel consumption (L/h)", color='blue', marker='o')
    ax[1].fill_between(time_stamps, fuel_consumption, color='blue', alpha=0.2)

    ax[2].plot(time_stamps, engine_power, label="Engine power (hp)", color='orange', marker='o')
    ax[2].fill_between(time_stamps, engine_power, color='orange', alpha=0.2)

    ax[3].plot(time_stamps, specific_fuel_consumption, label="Specific fuel consumption (kg/hp-hr)", color='purple', marker='o')
    ax[3].fill_between(time_stamps, specific_fuel_consumption, color='purple', alpha=0.2)

    ax[4].plot(time_stamps, fuel_consumption_area, label="Fuel consumption per tilled area (L/ha)", color='red', marker='o')
    ax[4].fill_between(time_stamps, fuel_consumption_area, color='red', alpha=0.2)

    ax[5].plot(time_stamps, implement_draft, label="Implement draft (kN)", color='pink', marker='o')
    ax[5].fill_between(time_stamps, implement_draft, color='pink', alpha=0.2)

    ax[6].plot(time_stamps, drawbar_power, label="Drawbar power (hp)", color='orange', marker='o')
    ax[6].fill_between(time_stamps, drawbar_power, color='orange', alpha=0.2)

    ax[7].plot(time_stamps, tractive_efficiency, label="Tractive efficiency (%)", color='blue', marker='o')
    ax[7].fill_between(time_stamps, tractive_efficiency, color='blue', alpha=0.2)

    for axis in ax:
        axis.legend(loc="upper right")
        axis.grid(True)

    ax[-1].set_xlabel("Time")

    # Display plot
    graph_placeholder.pyplot(fig)


# Call the display function
if __name__ == "__main__":
    display_parameters()
