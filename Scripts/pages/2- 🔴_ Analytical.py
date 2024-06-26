# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from datasist.structdata import detect_outliers

# Constants
DATA_PATH = "../data/Processed/V3Processed.csv"
FIG_DIR = "../report/Figures"

# Read data
df = pd.read_pickle(DATA_PATH)

# Sidebar navigation
st.sidebar.title('Navigation')
page_selection = st.sidebar.radio("Go to", ('Univariate Analysis', 'Bivariate Analysis', 'Multivariate Analysis'))

# Main content based on selection
if page_selection == 'Univariate Analysis':
    st.title('Univariate Analysis')

    # Distribution of Sale Prices
    st.subheader('What is the distribution of sale prices ?')
    fig = px.box(df, y='sale price ($)', title='Distribution of Sale prices')
    st.plotly_chart(fig)
    
    
    # Outliers detection
    otlr_idx = detect_outliers(df , 0 , ['sale price ($)'])
    st.write(f"Number of outliers in Sale Price: {len(otlr_idx)}")
    
    median_price = df['sale price ($)'].median()

    # Replace outliers (greater than 8.5M) with the median
    df['sale price ($)'] = df['sale price ($)'].apply(lambda x: median_price if x > 7500000 else x)
    st.subheader('The distribution of sale prices Aftar Handling')
    fig_handled = px.box(df, y='sale price ($)', title='Distribution of Sale Prices after Handling Outliers')
    st.plotly_chart(fig_handled)
    


    # Distribution of Locality
    st.subheader('What is the distribution of locality ?')
    fig = px.histogram(data_frame=df, x='locality', histfunc='count', text_auto=True ,
                       title='Distribution of Locality')
    fig.update_xaxes(categoryorder='total ascending')
    st.plotly_chart(fig)
    
    # Distribution of year
    st.subheader('What is the distribution of year ?')
    fig = px.histogram(data_frame=df , x = df['year'] ,text_auto=True ,title='Distribution of year')
    st.plotly_chart(fig)
    
    # Distribution of property
    st.subheader('What is the distribution of property ?')
    fig = px.histogram(data_frame=df , x = df['property'].astype(str) , text_auto=True,
                       title='Distribution of property')
    st.plotly_chart(fig)
    
    # Distribution of num_bathrooms
    st.subheader('What is the distribution of Nummber Of Bathrooms ? ?')
    fig = px.histogram(df, x='num_bathrooms', title='Histogram of Number of Bathrooms', text_auto=True).update_xaxes(categoryorder='total ascending')
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig)
    
    # Distribution of residential
    st.subheader('What is the distribution of residential ?')
    fig = px.histogram(df, x='residential', histfunc='count' ,title='Distribution of residential', text_auto=True).update_xaxes(categoryorder='total ascending')
    st.plotly_chart(fig)
    
    
    # Distribution of num_rooms
    st.subheader('What is the distribution of Number Of Rooms')
    fig = px.pie(data_frame=df , names = 'num_rooms' ,title='Distribution of Number Of Rooms', )
    st.plotly_chart(fig)
    
    
    # Distribution of face
    st.subheader('What is the distribution of face ?')
    fig = px.pie(data_frame=df , names = 'face',title='Distribution of face', )
    st.plotly_chart(fig)
    
    
    # Distribution of tax value
    st.subheader('What is the distribution of Tax Value ?')
    fig9= px.box(df, y='tax_value', title='Distribution of Tax Value')
    fig9.update_layout(yaxis_title='tax_value', xaxis_title='')
    st.plotly_chart(fig9)

        
        
    # Distribution of Month Name 
    st.subheader('What is the distribution of Month Name ?')
    fig5 = px.histogram(df, x='month_name', title='Histogram of Month Name', text_auto=True)
    fig5.update_layout(bargap=0.2)
    st.plotly_chart(fig5)


    
    
    

elif page_selection == 'Bivariate Analysis':
    st.title('Bivariate Analysis')
    
    # Correlation heatmap of numerical variables
    st.subheader('Correlation Heatmap')
    fig = px.imshow(df.select_dtypes('number').corr() , text_auto=True)
    st.plotly_chart(fig)



    # Scatter plot of Estimated Value vs Sale Price
    st.subheader('Relationship between Estimated Value and Sale Price')
    fig10 = px.scatter(df, x='estimated value ($)', y='sale price ($)', color='estimated value ($)',
                 title='House prices in the DataFrame', opacity=0.8)
    fig10.update_layout(xaxis_title='Estimated Value', yaxis_title='Sale price')
    st.plotly_chart(fig10)

    
    
    st.markdown("After seeing this plot, I realize there were Estimated Values of $0$, so I eliminated them.")
    df['estimated value ($)'].sort_values(ascending=True)
    df = df.drop(df[df['estimated value ($)'] < 3499].index)
    
    # Calculate the median of EstimatedValue
    median_estimated_value = df['estimated value ($)'].median()

    # Replace outliers (greater than 8.5M) with the median
    df['estimated value ($)'] = df['estimated value ($)'].apply(lambda x: median_estimated_value if x > 8500000 else x)
    st.subheader('Relationship between Estimated Value and Sale Price after handling outliers')

    fig= px.scatter(df, x='estimated value ($)', y='sale price ($)', color='estimated value ($)', title='House prices after Handling Outliers')
    st.plotly_chart(fig)
    

    
    
    
    
    
    
    # Group by 'year' and calculate average sale price and estimated value
    grouped_df = df.groupby('year')[['sale price ($)', 'estimated value ($)']].mean().reset_index()

    # Create the line plot using Plotly
    fig = go.Figure()

    # Add the line for sale price
    fig.add_trace(go.Scatter(x=grouped_df['year'], y=grouped_df['sale price ($)'], mode='lines+markers', name='Sale price ($)', line=dict(color='blue')))

    # Add the line for estimated value
    fig.add_trace(go.Scatter(x=grouped_df['year'], y=grouped_df['estimated value ($)'], mode='lines+markers', name='Estimated Value ($)', line=dict(color='orange')))

    # Update layout
    fig.update_layout(
        title='Relationship between Estimated Value and Sale Price',
        xaxis_title='Year',
        yaxis_title='Value ($)',
        legend_title='Legend'
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)


    # Distribution between number of rooms and sale price
    st.subheader('How does the number of rooms in a property affect its sale price ?')
    fig = px.histogram(data_frame=df , x = df['num_rooms'].astype(str) , y = 'sale price ($)', histfunc='avg' , text_auto=True ,title='Correlation between number of rooms and Sale Price in the DataFrame' )
    st.plotly_chart(fig)
    
    
    # Distribution between Face and sale price 
    st.subheader('Analysis of the Relationship Between Face Features and Sale Prices ?')
    fig = px.histogram(data_frame=df , x ='face' , y = 'sale price ($)' , text_auto=True ,title='Correlation between Face and Sale Price in the DataFrame' )
    st.plotly_chart(fig)
    
    
    # Distribution between Residential and sale price 
    st.subheader('Exploring Sale Prices of Residential Properties ?')
    # Group by 'residential' and calculate average sale price
    avg_sale_price = df.groupby('residential')['sale price ($)'].mean().reset_index()

    # Create histogram using Plotly Express
    fig = px.histogram(df, x='residential', y='sale price ($)',
                    title='Average Sale Price by Residential Type',
                    labels={'residential': 'Residential Type', 'sale price ($)': 'Average Sale Price ($)'},
                    color='residential',text_auto=True,
                    color_discrete_map={'House': 'blue', 'Apartment': 'green'},
                    histfunc='avg',  # Calculate average sale price within each 'residential' category
                    hover_data={'sale price ($)': ':.2f'}  # Display average sale price on hover with formatting
                   )

    # Display the plot in Streamlit
    st.plotly_chart(fig)
    
    
    # Calculate yearly average sale price
    yearly_sale_price = df.groupby('year')['sale price ($)'].mean().reset_index()

    # Create line plot using Plotly Express
    fig = px.line(yearly_sale_price, x='year', y='sale price ($)',
                title='Average Sale Price per Year',
                labels={'year': 'Year', 'sale price ($)': 'Average Sale Price ($)'})

    # Display the plot in Streamlit
    st.subheader('Correlation Between Sale Prices and Transaction Year ?')
    st.plotly_chart(fig)

        
    
    
    
    # Distribution between year and sale price
    st.subheader('Examining the Relationship Between Sale Prices and Year of Transaction ?')
    fig = px.histogram(data_frame=df,x=df['year'].astype(str),y='sale price ($)',title='Relation Between Sale Price and Year',color='year',
                       text_auto=True).update_xaxes(categoryorder='total ascending')
    st.plotly_chart(fig)
    
    
    
    locality_mean = df.groupby('locality')['sale price ($)'].mean().sort_values().reset_index()

    # Create bar plot using Plotly Express
    fig = px.bar(locality_mean, x='locality', y='sale price ($)',
             title='Mean Sale Price in Each Locality',text_auto=True,
             labels={'locality': 'Locality', 'sale price ($)': 'Mean Sale Price ($)'},
             color='sale price ($)',
             color_continuous_scale='Viridis')

    # Display the plot in Streamlit
    st.subheader('Average Sale Price Analysis Across Localities ?')
    st.plotly_chart(fig)

 
    
    # Distribution between face and property
    st.subheader('Analysis of face Across Different property')
    # Group by 'face' and 'property' to get counts
    df_face_property = df.groupby(['face', 'property']).size().reset_index(name='count')

    # Create histogram using Plotly Express
    fig = px.histogram(df_face_property, x='face', y='count', color='property',
                    title='Distribution of Property Types by Face',
                    labels={'face': 'Face', 'count': 'Count', 'property': 'Property Type'},
                    barmode='group',
                    text_auto=True ,
                    )

    # Add comment after the plot
    comment = "This indicates that the face orientation (East, North, South, West) does not significantly impact the type of properties in the dataset."
    st.plotly_chart(fig)
    st.markdown(comment)
    
    
     # Relationship between Locality and Residential Status
    st.subheader('Relationship between Locality and Residential Status')
    fig29 = px.histogram(df, x='locality', color='residential',
                   title='Relationship between Locality and Residential Status',
                   labels={'locality': 'Locality', 'residential': 'Residential Status'},
                   barmode='group')

    st.plotly_chart(fig29)


    
    # Distribution between Average Carpet Area by Locality
    st.title('Relationship between Average Carpet Area by Locality')
    avg_carpet_area = df.groupby('locality')['carpet_area_sq_ft'].mean().reset_index()
    fig18= px.bar(avg_carpet_area, x='locality', y='carpet_area_sq_ft',
                title='Average Carpet Area by Locality',
                labels={'locality': 'Locality', 'carpet_area_sq_ft': 'Average Carpet Area (sq ft)'})
    fig18.update_xaxes(categoryorder='total ascending')
    st.plotly_chart(fig18)
    
    
    
    
    # Average Carpet Area by Residential Type
    st.subheader('Analysis of Carpet Area by Residential Type ?')
    carpet_res_avg = df.groupby('residential')['carpet_area_sq_ft'].mean().sort_values().reset_index()
    fig = px.bar(carpet_res_avg, x='residential', y='carpet_area_sq_ft', 
                 title='Average Carpet Area by Residential Type',
                 labels={'residential': 'Residential Type', 'carpet_area_sq_ft': 'Average Carpet Area (sq ft)'},
                 color='residential' , text_auto=True)
    st.plotly_chart(fig)
    
    
    
    
    
    # Distribution between Property and Facing Residential Status
    st.title('Relationship between Property Type and Residential Status')
    fig= px.histogram(df, x='property', color='residential',
                        title='Relationship between Property Type and Residential Status',
                        labels={'property': 'Property Type', 'residential': 'Residential Status'},
                        barmode='group' , text_auto=True)  # Use grouped bars

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig)
    
    
    # Distribution between Average Tax Value by Residential Category
    st.title('Relationship between Average Tax Value by Residential Category')
    avg_tax_value = df.groupby('residential')['tax_value'].mean().reset_index()
    fig21 = px.bar(avg_tax_value, x='residential', y='tax_value', 
             title='Average Tax Value by Residential Category',
             labels={'residential': 'Residential Category', 'tax_value': 'Average Tax Value ($)'},
             text='tax_value')
    st.plotly_chart(fig21)

  
    # Distribution between Average Tax Value by locality Category
    st.title('Relationship between Average Tax Value by locality Category')
    avg_tax_value = df.groupby('locality')['tax_value'].mean().reset_index()
    fig22 = px.bar(avg_tax_value, x='locality', y='tax_value', 
             title='Average Tax Value by locality Category',
             labels={'locality': 'locality Category', 'tax_value': 'Average Tax Value ($)'},
             text='tax_value')
    st.plotly_chart(fig22)
   


elif page_selection == 'Multivariate Analysis':
    st.title('Multivariate Analysis')


    st.subheader('Correlation between number of rooms and the number of bathrooms together affect the sale price ?')
    fig = px.histogram(df, x='num_rooms', y='sale price ($)', color='num_bathrooms',
                    title='Number of Rooms and Bathrooms vs Sale price',
                    labels={'num_rooms': 'Number of Rooms', 'sale price ($)': 'Sale Price ($)', 'num_bathrooms': 'Number of Bathrooms'},
                    hover_data=['carpet_area_sq_ft'],
                    histfunc='avg',  # Aggregate sale price by average within each bin
                    barmode='group', text_auto=True # Group bars by 'num_bathrooms'
                    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)
    
    
    st.subheader('Correlation between locality affect the sale price considering the carpet area ?')
    # Group by 'locality' and calculate average sale price and carpet area
    avg_values = df.groupby('locality').agg({
        'sale price ($)': 'mean', 
        'carpet_area_sq_ft': 'mean'
    }).reset_index()

    # Melt the DataFrame to convert 'sale price ($)' and 'carpet_area_sq_ft' into a single column
    melted_df = pd.melt(avg_values, id_vars=['locality'], 
                        value_vars=['sale price ($)', 'carpet_area_sq_ft'],
                        var_name='metric', value_name='value')

    # Create a grouped bar plot using Plotly Express
    fig = px.bar(melted_df, 
                x='locality', 
                y='value', 
                color='metric',
                title='Average Sale Price and Carpet Area by Locality',text_auto=True,
                labels={'locality': 'Locality', 'value': 'Value', 'metric': 'Metric'},
                barmode='group',  # Group bars by 'locality'
                )

    # Update y-axis label
    fig.update_yaxes(title_text='Value')

    # Display the plot in Streamlit
    st.plotly_chart(fig)
    
    
    
    st.subheader('Correlation locality and residential status together affect the sale price ?')
    avg_values = df.groupby(['locality', 'residential']).agg({'sale price ($)': 'mean'}).reset_index()
    fig = px.bar(avg_values, x='locality', y='sale price ($)', color='residential', 
                 title='Average Sale Price by Locality and Residential Type',
                 labels={'sale price ($)': 'Average Sale price ($)', 'locality': 'Locality', 'residential': 'Residential Type'},
                 barmode='group',text_auto=True)
    st.plotly_chart(fig)
    
    
    st.subheader('Relationship between Sale Price, Property Type, and Residential Status ?')
    fig27 = px.histogram(df, x='property', y='sale price ($)', color='residential',
                   title='Relationship between Sale Price, Property Type, and Residential Status',
                   labels={'property': 'Property Type', 'sale price ($)': 'Sale Price ($)', 'residential': 'Residential Status'},
                   barmode='group', histfunc='avg')  # Use mean for sale price

    st.plotly_chart(fig27)


    st.subheader('Relationship between Tax Value and Sale Price by Year ?')
    grouped_df = df.groupby('year')[['sale price ($)', 'tax_value']].mean().reset_index()
    fig23= go.Figure()

    # Add the line for sale price
    fig23.add_trace(go.Scatter(x=grouped_df['year'], y=grouped_df['sale price ($)'], mode='lines+markers', name='Sale price ($)', line=dict(color='blue')))

    # Add the line for tax_value
    fig23.add_trace(go.Scatter(x=grouped_df['year'], y=grouped_df['tax_value'], mode='lines+markers', name='tax_value', line=dict(color='orange')))
    fig23.update_layout(
        title='Relationship between tax_value and Sale Price',
        xaxis_title='Year',
        yaxis_title='Value ($)',
        legend_title='Legend'
    )
    
    st.plotly_chart(fig23)


    
    

# Footer
st.sidebar.markdown("---")
st.sidebar.text("Made with ❤️ by Mahmoud Shatia")
