import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Constants
DATA_PATH = "../data/Processed/V3Explored.csv"
REPLACED_NAME = {
    'carpet_area': 'carpet_area_sq_ft',
    'estimated value': 'estimated value ($)',
    'sale price': 'sale price ($)'
}

# Function to display missing values table
def missing_values_table(df):
    missing = df.isna().sum()
    missing_percent = (missing / len(df)) * 100
    missing_table = pd.concat([missing, missing_percent], axis=1)
    missing_table.columns = ['Missing Values', '% of Total Values']
    missing_table = missing_table[missing_table.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
    return missing_table

# Function to get season based on month
def get_season(month):
    if month in ['March', 'April', 'May']:
        return 'Spring'
    elif month in ['June', 'July', 'August']:
        return 'Summer'
    elif month in ['September', 'October', 'November']:
        return 'Fall'
    else:
        return 'Winter'

# Load the processed data
df = pd.read_pickle(DATA_PATH)

# Streamlit UIw
st.set_page_config(page_title='Real Estate Data Processing', layout='wide')

# Sidebar
st.sidebar.title('Navigation')
page_selection = st.sidebar.radio("Go to", ('Data Overview', 'Missing Values', 'Insights'))

# Main content based on selection
if page_selection == 'Data Overview':
    st.title("Phase 1 : Exploration Of Data Analytics")
    st.write("Before we start exploring the data, let's establish a clear objective to guide our analysis.")

    # Display image
    image_path = "explor.JPG"
    image = Image.open(image_path)
    st.image(image, caption="Real Estate", use_column_width=True)
    # Containers for dataset and visualizations
    dataset_real_estate = st.container()
    statical_real_estate = st.container()
    with dataset_real_estate:
        st.header("All Real Estate Data")
        st.write("Explore the dataset to get all the information about the data we've obtained from Kaggle.")

        # Button to show/hide DataFrame
        show_dataframe = st.button("Show DataFrame of Real Estate")
        if show_dataframe:
            with st.expander("All Information about the Data and Descriptions"):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Sample Data")
                    st.write(df.sample(3))
                with col2:
                    st.subheader("Single Entry Description")
                    st.write(df.sample(1).iloc[0])
    with statical_real_estate:
   # List of questionable categorical columns
        questionable_cat_cols = ["locality", "property", "residential", "face"]

        st.subheader("Unique Values in Questionable Categorical Columns")
        for col in questionable_cat_cols:
            if col in df.columns:
                st.write(f"**Column: {col}**")
                st.write(df[col].unique().tolist())
                st.markdown("---")
            else:
                st.write(f"**Column: {col}**")
                st.write("Column not found in the dataset.")
                st.markdown("---")

        # List of questionable numerical columns
        questionable_num_cols = ['date', 'year', 'estimated value', 'sale price', 'num_rooms', 'num_bathrooms', 'carpet_area', 'property_tax_rate']

        st.subheader("Checking for Missing Values in Questionable Numerical Columns")
        for col in questionable_num_cols:
            if col in df.columns and df[col].isna().any():
                st.write(f"**{col}**: has missing values")
            elif col not in df.columns:
                st.write(f"**{col}**: Column not found in the dataset.")

elif page_selection == 'Missing Values':
    st.title('Dealing with Missing Values')

    # Display missing values table
    st.subheader("Missing Values Summary")
    st.write(missing_values_table(df))

    # Handle missing values in 'locality' and 'property'
    df['locality'].fillna('Unknown', inplace=True)
    df['property'].fillna(df['property'].mode()[0], inplace=True)

    # Show updated missing values summary
    st.subheader("After Handling Missing Values")
    st.write(missing_values_table(df))

elif page_selection == 'Insights':
    st.title('Insights from Data')

    # Example insights
    insight_text = """
    Here are some insights from the processed data:
    - The dataset contains various numerical and categorical columns related to real estate properties.
    - Some columns had missing values which were handled through imputation or removal.
    - Seasonal and age-related features were derived from existing data for deeper analysis.
    """

    st.write(insight_text)

# Footer
st.sidebar.markdown("---")
st.sidebar.text("Made with ❤️ by Mahmoud Shatia")