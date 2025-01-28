import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
df = pd.read_csv("flights_important_features.csv")

# Clean up any potential missing values
df = df.dropna()

# Set up the title and layout of the dashboard
st.title("Flight Delay Analysis Dashboard")
st.markdown("""This interactive dashboard allows you to explore flight delays, identify patterns, and get insights to optimize flight schedules.""")

# Sidebar options
st.sidebar.header("Navigation")
section = st.sidebar.selectbox("Choose a section:", [
    "Dataset Overview", "Delay Visualizations", "Optimization Suggestions"
])

if section == "Dataset Overview":
    st.subheader("Dataset Overview")
    if st.checkbox("Show Dataset Info", key="dataset_info"):
        st.write(df.head())
        st.write("Dataset Shape:", df.shape)
        st.write("Missing Values:", df.isnull().sum())

elif section == "Delay Visualizations":
    st.subheader("Visualizations of Flight Delays")

    # Delay distribution
    st.subheader("1. Flight Delay Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Arr_Delay_x'], kde=True, bins=50, ax=ax, color="skyblue")
    ax.set_title("Distribution of Arrival Delays")
    ax.set_xlabel("Arrival Delay (minutes)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    st.markdown("""
    **Insights:**
    - The histogram shows the frequency of arrival delays across different ranges.
    - A significant number of flights are delayed by less than 30 minutes, while longer delays are less frequent.
    - Understanding this distribution helps in identifying common delay durations and may assist in optimizing flight schedules to minimize long delays.
    """)

    # Average delay by day of the week
    st.subheader("2. Average Delay by Day of the Week")
    delay_by_day = df.groupby('Day_Of_Week_x')['Arr_Delay_x'].mean().reset_index()
    fig = px.bar(delay_by_day, x='Day_Of_Week_x', y='Arr_Delay_x', 
                 title="Average Arrival Delay by Day of the Week", 
                 labels={"Day_Of_Week_x": "Day of the Week", "Arr_Delay_x": "Average Delay (minutes)"}, 
                 color="Arr_Delay_x", color_continuous_scale="Blues")
    st.plotly_chart(fig)

    st.markdown("""
    **Insights:**
    - The plot indicates that certain days, such as Mondays and Fridays, may experience higher average delays.
    - Airlines can optimize schedules by adjusting flight times or resources on these high-delay days.
    """)

    # Delays by airport and month
    st.subheader("3. Delays by Airport and Month")
    if st.checkbox("Show Delays by Airport and Month", key="delays_by_airport_period"):
        # Ensure 'FlightDate' is properly formatted and 'AIRPORT' exists in the dataset
        if 'FlightDate' in df.columns and 'AIRPORT' in df.columns:
            try:
                # Convert 'FlightDate' to datetime and extract the month
                df['Month'] = pd.to_datetime(df['FlightDate'], errors='coerce').dt.month
                df = df.dropna(subset=['Month'])
                
                # Group by 'AIRPORT' and 'Month' to calculate the mean arrival delay
                delay_by_airport_period = df.groupby(['AIRPORT', 'Month'])['Arr_Delay_x'].mean().reset_index()
                
                # Plot using Plotly
                fig = px.bar(delay_by_airport_period, x='Month', y='Arr_Delay_x', color='AIRPORT',
                             title="Average Delay by Airport and Month", 
                             labels={"Month": "Month", "Arr_Delay_x": "Average Delay (minutes)"}, 
                             barmode='group')
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error processing 'FlightDate' or 'AIRPORT': {e}")
        else:
            st.warning("'FlightDate' or 'AIRPORT' columns are missing in the dataset. Please ensure the dataset includes these columns.")

    st.markdown("""
    **Insights:**
    - Delays vary depending on both the airport and the month. Some airports experience more delays during certain months due to seasonal weather patterns or operational conditions.
    - Focus on airports with consistently high delays to improve operational efficiency and allocate resources effectively.
    """)

    # Scatter plot of Departure vs Arrival Delays
    st.subheader("4. Departure vs Arrival Delays")
    fig = px.scatter(df, x='Dep_Delay_x', y='Arr_Delay_x', title='Departure Delay vs Arrival Delay',
                     labels={'Dep_Delay_x': 'Departure Delay (minutes)', 'Arr_Delay_x': 'Arrival Delay (minutes)'}
    )
    st.plotly_chart(fig)

    st.markdown("""
    **Insights:**
    - The scatter plot helps identify the correlation between departure and arrival delays. Flights with long departure delays tend to have longer arrival delays.
    - Understanding this relationship can guide operational adjustments to minimize both types of delays and improve on-time performance.
    """)

    # Heatmap: Arrival Delays by Weather Conditions (Wind and Precipitation)
    st.subheader("5. Arrival Delays by Weather Conditions")
    if 'wdir' in df.columns and 'prcp' in df.columns:
        weather_delay = df.groupby(['wdir', 'prcp'])['Arr_Delay_x'].mean().unstack()
        fig = px.imshow(weather_delay, title="Arrival Delays by Weather Conditions (Wind & Precipitation)", 
                        labels=dict(color="Average Delay (minutes)"))
        st.plotly_chart(fig)

        st.markdown("""
        **Insights:**
        - The heatmap provides a view of how weather conditions like wind direction and precipitation affect arrival delays.
        - Flights during heavy precipitation or strong winds tend to experience longer delays.
        - Airlines can use weather forecasts to better anticipate delays and adjust flight schedules accordingly.
        """)

elif section == "Optimization Suggestions":
    st.subheader("Optimization Suggestions")

    st.markdown("### Insights for Optimizing Flight Schedules")
    st.markdown("""
    - **Adjust flight schedules for peak delay days**: Reduce traffic on high-delay days such as Mondays and Fridays.
    - **Leverage weather data**: Optimize flight times to avoid weather patterns causing delays (e.g., high precipitation or unfavorable wind directions).
    - **Review airport-specific delays**: Focus on airports with consistently high delays and allocate resources to mitigate bottlenecks.
    - **Analyze seasonal trends**: Address delays during specific months by adapting schedules to seasonal demand and operational challenges.
    """)

# Download the cleaned dataset
st.sidebar.subheader("Download Cleaned Dataset")
csv = df.to_csv(index=False)
st.sidebar.download_button(label="Download CSV", data=csv, file_name="cleaned_flights.csv", mime="text/csv")

