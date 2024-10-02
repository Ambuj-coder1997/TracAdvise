import streamlit as st
import random
import time

def generate_main_flow_rate():
    return round(random.uniform(1.08, 1.24), 2)

def generate_overflow_flow_rate():
    return round(random.uniform(0.98, 1.17), 2)

def generate_mainflow_fuel_quantity():
    return random.randint(0, 500)

def generate_overflow_fuel_quantity():
    return random.randint(0, 350)

def generate_total_fuel_consumption():
    return round(random.uniform(0.12, 0.21), 2)

def display_parameters():
    #st.title("Real-time Fuel Parameters Display")
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f5f5; /* Change background color */
        }
        table {
            font-size: 24px; /* Set font size */
            border-collapse: collapse;
            width: 50%;
            margin-bottom: 20px;
            margin-left: auto;
            margin-right: auto;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #401604; /* Change table header color */
            color: white; /* Change table header text color */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.write("")

    with col2:
        st.image("fc.png")

    with col3:
        st.write("")

    output_placeholder = st.empty()

    while True:
        main_flow_rate = generate_main_flow_rate()
        overflow_flow_rate = generate_overflow_flow_rate()
        mainflow_fuel_quantity = generate_mainflow_fuel_quantity()
        overflow_fuel_quantity = generate_overflow_fuel_quantity()
        total_fuel_consumption = generate_total_fuel_consumption()

        output_content = f"""
        <table>
            <tr>
                <th>Parameter</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Main Flow Line Flow Rate (L/min) </td>
                <td>{main_flow_rate}</td>
            </tr>
            <tr>
                <td>Overflow Line Flow Rate (L/min)</td>
                <td>{overflow_flow_rate}</td>
            </tr>
            <tr>
                <td>Mainflow Line Fuel Quantity (mL)</td>
                <td>{mainflow_fuel_quantity}</td>
            </tr>
            <tr>
                <td>Overflow Line Fuel Quantity (mL)</td>
                <td>{overflow_fuel_quantity}</td>
            </tr>
            <tr>
                <td>Total Fuel Consumption (l/min)</td>
                <td>{total_fuel_consumption}</td>
            </tr>
        </table>
        """

        output_placeholder.markdown(output_content, unsafe_allow_html=True)
        time.sleep(1)  # Display for 3 seconds

        output_placeholder.empty()  # Clear the content for new data
        #time.sleep(1)  # Add a small delay before displaying new data
def show_fc_page():
    st.markdown("<h3 style='text-align: center; color: #4d3b02;'>Real-time Fuel Consumption Parameters Display</h3>", unsafe_allow_html=True)
    display_parameters()