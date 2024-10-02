import streamlit as st
import random
import time

def generate_actual_speed():
    return round(random.uniform(0.78, 1.28), 2)

def generate_theoretical_speed():
    return round(random.uniform(1.16, 1.23), 2)

def generate_wheel_slip():
    return random.randint(15, 37)

def check_wheel_slip_status(wheel_slip):
    threshold = 20
    if wheel_slip > threshold:
        return "Over Limit", "red"  # Color for 'Over Limit' text
    else:
        return "Safe Limit", "green"  # Color for 'Safe Limit' text

def display_parameters():
    #st.title("Real-time Speed and Slip Parameters Display")
    page_bg_img = '''
    <style>
    body {
    background-image: logo.png;
    background-size: cover;
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f5f5; /* Change background color */
        }
        table {
            font-size: 20px; /* Set font size */
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
            background-color: #a903fc; /* Change table header color */
            color: white; /* Change table header text color */
        }
        .over-limit {
            color: red; /* Change font color for 'Over Limit' */
        }
        .safe-limit {
            color: green; /* Change font color for 'Safe Limit' */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.write("")

    with col2:
        st.image("speed.png")

    with col3:
        st.write("")

    output_placeholder = st.empty()

    while True:
        actual_speed = generate_actual_speed()
        theoretical_speed = generate_theoretical_speed()
        wheel_slip = generate_wheel_slip()
        wheel_slip_status, color = check_wheel_slip_status(wheel_slip)

        output_content = f"""
        <table>
            <tr>
                <th>Parameter</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Actual Speed (m/s)</td>
                <td>{actual_speed}</td>
            </tr>
            <tr>
                <td>Theoretical Speed (m/s)</td>
                <td>{theoretical_speed}</td>
            </tr>
            <tr>
                <td>Wheel Slip (%)</td>
                <td>{wheel_slip}</td>
            </tr>
            <tr>
                <td>Wheel Slip Status</td>
                <td class="{wheel_slip_status.lower().replace(' ', '-')}">{wheel_slip_status}</td>
            </tr>
        </table>
        """

        output_placeholder.markdown(output_content, unsafe_allow_html=True)
        time.sleep(1)  # Display for 3 seconds

        output_placeholder.empty()  # Clear the content for new data
        #time.sleep(1)  # Add a small delay before displaying new data
def show_speednslip_page():
    st.markdown("<h3 style='text-align: center; color: #031cfc;'>Real-time Speed and Slip Parameters Display</h3>", unsafe_allow_html=True)
    display_parameters()