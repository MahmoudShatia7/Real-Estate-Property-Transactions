# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import pandas as pd 
import os 
# Configure the page layout and appearance
st.set_page_config(
    page_title= "Real Estate Property Transactions",
    page_icon= '🪴',
    layout="wide")
# Add logo to the sidebar
#st.sidebar.image("logo.webp")
st.sidebar.success("Made with ❤️ / \n Created by Mahmoud Shatia")
# Create container
header = st.container()
with header :
    # Set the page title and subheader
    st.title(" 🏠 Real Estate Property Transactions ")
    st.subheader("About My Project")
    # Provide a brief description of the project
    st.write("it’s Mid Project for Data Science Diploma i build a Python Script to various analytical purposes such as market analysis, predictive modeling, and decision-making in the real estate industry. Then we extract the data from kaggle and then load this data into a Python Pandas DataFrame and analyze this data. Finally, we build simple visualization from this data using the Python Seaborn and ploty library.")
    # Display an image
    image = st.image("y.webp")
