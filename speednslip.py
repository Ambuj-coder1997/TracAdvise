import streamlit as st
import random
import time
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

# Function to generate values and calculate parameters
def calculate_parameters():
    throttle = generate_throttle_values()
    engine_speed = generate_engine_speed_values()
    forward_speed = generate_forward_speed_values()
    implement_depth = generate_implement_depth_values()
    gear_ratio = random.choice(gear_ratios)

    slip = calculate_slip(engine_speed, forward_speed, gear_ratio)

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

    return {
        'engine_torque': ent,
        'fuel_consumption': fcp,
        'engine_power': enp,
        'specific_fuel_consumption': sfc,
        'fuel_consumption_area': FC,
        'implement_draft': draft,
        'drawbar_power': dbp,
        'tractive_efficiency': te,
        'throttle': throttle,
        'engine_speed': engine_speed,
        'forward_speed': forward_speed,
        'implement_depth': implement_depth,
        'slip': slip
    }

# Main function to display tractor parameters
def display_parameters():
    st.markdown("<h1>Real-time Tractor Performance Prediction</h1>", unsafe_allow_html=True)

    # Initialize placeholders for output and graph
    output_placeholder = st.empty()
    graph_placeholder = st.empty()

    # Initialize lists to store data for plotting
    throttle_values = []
    engine_speed_values = []
    forward_speed_values = []
    implement_depth_values = []
    slip_values = []
    engine_torque_values = []
    fuel_consumption_values = []
    engine_power_values = []
    specific_fuel_consumption_values = []
    fuel_consumption_area_values = []
    implement_draft_values = []
    drawbar_power_values = []
    tractive_efficiency_values = []
    time_stamps = []

    # Icon URLs for each parameter
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

    # Infinite loop for continuous data generation
    while True:
        time_stamp = len(time_stamps)  # Using the list length as a time index

        # Calculate new parameters
        params = calculate_parameters()

        # Append new values to lists
        throttle_values.append(params['throttle'])
        engine_speed_values.append(params['engine_speed'])
        forward_speed_values.append(params['forward_speed'])
        implement_depth_values.append(params['implement_depth'])
        slip_values.append(params['slip'])
        engine_torque_values.append(params['engine_torque'])
        fuel_consumption_values.append(params['fuel_consumption'])
        engine_power_values.append(params['engine_power'])
        specific_fuel_consumption_values.append(params['specific_fuel_consumption'])
        fuel_consumption_area_values.append(params['fuel_consumption_area'])
        implement_draft_values.append(params['implement_draft'])
        drawbar_power_values.append(params['drawbar_power'])
        tractive_efficiency_values.append(params['tractive_efficiency'])
        time_stamps.append(time_stamp)

        # Table content
        table_content = """
        <table>
            <tr><th>Parameter</th><th>Value</th></tr>
        """
        table_content += f"""
        <tr><td><img src="{icon_url['Engine Torque']}" width="24"/> Engine Torque (Nm)</td><td>{params['engine_torque']:.2f}</td></tr>
        <tr><td><img src="{icon_url['Fuel Consumption']}" width="24"/> Fuel Consumption (L/h)</td><td>{params['fuel_consumption']:.2f}</td></tr>
        <tr><td><img src="{icon_url['Engine Power']}" width="24"/> Engine Power (hp)</td><td>{params['engine_power']:.2f}</td></tr>
        <tr><td><img src="{icon_url['Specific Fuel Consumption']}" width="24"/> Specific Fuel Consumption (kg/hp-hr)</td><td>{params['specific_fuel_consumption']:.2f}</td></tr>
        <tr><td><img src="{icon_url['Fuel Consumption per Tilled Area']}" width="24"/> Fuel Consumption per Tilled Area (L/ha)</td><td>{params['fuel_consumption_area']:.2f}</td></tr>
        <tr><td><img src="{icon_url['Implement Draft']}" width="24"/> Implement Draft (kN)</td><td>{params['implement_draft']:.2f}</td></tr>
        <tr><td><img src="{icon_url['Drawbar Power']}" width="24"/> Drawbar Power (hp)</td><td>{params['drawbar_power']:.2f}</td></tr>
        <tr><td><img src="{icon_url['Tractive Efficiency']}" width="24"/> Tractive Efficiency (%)</td><td>{params['tractive_efficiency']:.2f}</td></tr>
        """
        table_content += "</table>"

        # Display table
        output_placeholder.markdown(table_content, unsafe_allow_html=True)

        # Plot data
        fig, ax = plt.subplots()
        ax.plot(time_stamps, engine_torque_values, label="Engine Torque (Nm)")
        ax.plot(time_stamps, fuel_consumption_values, label="Fuel Consumption (L/h)")
        ax.plot(time_stamps, engine_power_values, label="Engine Power (hp)")
        ax.plot(time_stamps, specific_fuel_consumption_values, label="Specific Fuel Consumption (kg/hp-hr)")
        ax.plot(time_stamps, fuel_consumption_area_values, label="Fuel Consumption per Tilled Area (L/ha)")
        ax.plot(time_stamps, implement_draft_values, label="Implement Draft (kN)")
        ax.plot(time_stamps, drawbar_power_values, label="Drawbar Power (hp)")
        ax.plot(time_stamps, tractive_efficiency_values, label="Tractive Efficiency (%)")

        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("Real-time Tractor Performance Parameters")
        ax.legend()

        # Display graph
        graph_placeholder.pyplot(fig)

        # Pause for a short time to simulate real-time behavior
        time.sleep(3)

if __name__ == "__main__":
    display_parameters()
