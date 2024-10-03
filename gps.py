import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sample data for the table and map (replace this with actual data)
data = {
    'Parameter': ['Gear Ratio', 'Engine Speed (rpm)', 'Throttle Setting (%)', 'Implement Depth (cm)',
                  'Actual Speed (km/h)', 'Slip (%)', 'Latitude (N)', 'Longitude (E)'],
    'Value': ['L1', 1490, 51, 27.72, 4.34, -54.60, 22.312841038797888, 87.33148608163823]
}

# Convert the data to a pandas DataFrame for table display
df = pd.DataFrame(data)

# Sample GPS coordinates (replace with real GPS data)
gps_coordinates = pd.DataFrame({
    'lat': [22.312841038797888],
    'lon': [87.33148608163823]
})

# Create two columns: table + map on the left, plot on the right
col1, col2 = st.columns(2)

# Column 1: Table and GPS Map
with col1:
    # Display the header for the table
    st.header("Real-time Tractor Operating Parameters")
    
    # Display the table
    st.table(df)

    # Display the GPS map (replace this with real GPS data in use)
    st.map(gps_coordinates)

# Column 2: Real-time Plot with dynamic dots and shaded area
with col2:
    st.header("Real-time Data Variation")
    
    # Simulate real-time data for the plot (replace with actual real-time data)
    x = np.linspace(0, 10, 100)  # Example x-axis (time or similar)
    y = np.sin(x)  # Example y-axis (replace with tractor parameter data)

    # Create the plot
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(x, y, label='Parameter Variation', color='blue')

    # Mark the current point with a red dot
    current_value_index = -1  # Use the latest point in the data, or dynamically calculate the index
    ax.plot(x[current_value_index], y[current_value_index], 'ro', label='Current Value')

    # Shade the area under the curve
    ax.fill_between(x, y, color="lightblue", alpha=0.5)

    # Label the axes
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    
    # Add a legend
    ax.legend()

    # Display the plot
    st.pyplot(fig)
