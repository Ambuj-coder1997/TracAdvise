import streamlit as st
from gps import show_gps_page
from speednslip import display_parameters
from fc import show_fc_page
from PIL import Image
#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
image = Image.open("logo.png")
st.sidebar.image(image)
st.sidebar.title("An AI-IoT based Tractor Field Performance Monitoring cum Advisory System for Optimum Tillage")
page = st.sidebar.selectbox("Select an option", ("Tractor Operating Parameters", "Tractor Performance Prediction","Tractor Advisory System"))

if page == "Tractor Operating Parameters":
    show_gps_page()
else:
    if page == "Tractor Performance Prediction":
        display_parameters()
    else:
        if page == "Tractor Advisory System":
            show_fc_page()
        

