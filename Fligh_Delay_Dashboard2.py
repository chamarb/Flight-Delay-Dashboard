import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
df = pd.read_csv("flights_important_features.csv")

# Clean up any potential missing values
df = df.dropna()

# Set up the title of the dashboard
st.title("Flight Delay Analysis Dashboard")

# Display basic dataset information
if st.checkbox("Show Dataset Info", key="dataset_info"):
    st.write(df.head())
    st.write("Dataset Shape:", df.shape)
    st.write("Missing Values:", df.isnull().sum())

# Option to view a distribution of delays
st.subheader("Flight Delay Distribution")
if st.checkbox("Show Delay Distribution Plot", key="delay_distribution"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Arr_Delay_x'], kde=True, bins=50, ax=ax)
    ax.set_title("Distribution of Arrival Delays")
    ax.set_xlabel("Arrival Delay (minutes)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    st.write("**Insight**: Most flight delays seem to be relatively short, with a significant peak around the 0-30 minute range.")

# Bar plot of delays by day of the week
st.subheader("Average Delay by Day of the Week")
if st.checkbox("Show Average Delay by Day of the Week", key="delay_by_day"):
    delay_by_day = df.groupby('Day_Of_Week_x')['Arr_Delay_x'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Day_Of_Week_x', y='Arr_Delay_x', data=delay_by_day, ax=ax, palette="coolwarm")
    ax.set_title("Average Arrival Delay by Day of the Week")
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Average Arrival Delay (minutes)")
    st.pyplot(fig)
    st.write("**Insight**: Mondays and Fridays seem to have higher delays, possibly due to the weekend rush or logistical challenges.")

# Check if the 'Flight_Duration_x' column exists before proceeding
if 'Flight_Duration_x' in df.columns:
    # Create 'Time_of_Day' column based on flight duration
    df['Time_of_Day'] = pd.cut(df['Flight_Duration_x'], 
                               bins=[0, 60, 120, 180, 240], 
                               labels=['Short', 'Medium', 'Long', 'Very Long'])
else:
    st.warning("'Flight_Duration_x' column not found in the dataset. Please check the dataset.")

# Now the bar plot for delays by time of day should work
if st.checkbox("Show Average Delay by Time of Day", key="delay_by_time"):
    if 'Time_of_Day' in df.columns:  # Only proceed if 'Time_of_Day' exists
        delay_by_time = df.groupby('Time_of_Day')['Arr_Delay_x'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Time_of_Day', y='Arr_Delay_x', data=delay_by_time, ax=ax, palette="coolwarm")
        ax.set_title("Average Arrival Delay by Time of Day", fontsize=14)
        ax.set_xlabel("Time of Day", fontsize=12)
        ax.set_ylabel("Average Arrival Delay (minutes)", fontsize=12)
        st.pyplot(fig)
        st.write("**Insight**: Flights during the 'Very Long' duration segment tend to have higher delays, potentially due to complex scheduling or extended transit times.")
    else:
        st.warning("'Time_of_Day' column not found after transformation.")

# Interactive scatter plot of Departure vs Arrival Delays
st.subheader("Departure vs Arrival Delays")
if st.checkbox("Show Departure vs Arrival Delays", key="dep_vs_arr"):
    fig = px.scatter(df, x='Dep_Delay_x', y='Arr_Delay_x', title='Departure Delay vs Arrival Delay',
                     labels={'Dep_Delay_x': 'Departure Delay (minutes)', 'Arr_Delay_x': 'Arrival Delay (minutes)'})
    st.plotly_chart(fig)
    st.write("**Insight**: There seems to be a positive correlation between departure and arrival delays, indicating that delayed departures often lead to delayed arrivals.")

# Heatmap of arrival delays by weather conditions (wind direction and precipitation)
st.subheader("Arrival Delays by Weather Conditions")
if st.checkbox("Show Arrival Delays by Weather Conditions", key="weather_delays"):
    weather_delay = df.groupby(['wdir', 'prcp'])['Arr_Delay_x'].mean().unstack()
    fig = px.imshow(weather_delay, title="Arrival Delays by Weather Conditions (Wind & Precipitation)")
    st.plotly_chart(fig)
    st.write("**Insight**: Certain wind directions and precipitation levels seem to have a significant impact on arrival delays, with some weather patterns leading to higher delays.")

# Display the option to download the cleaned dataset
st.subheader("Download Cleaned Dataset")
csv = df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name="cleaned_flights.csv", mime="text/csv")

