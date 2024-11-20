import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Function
def create_monthly_trends(df):
    df['month'] = pd.Categorical(
        df['month'],
        categories=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        ordered=True
    )
    monthly_trends = df.groupby([
        'year', 
        'month'
    ], observed=True)['count'].sum().unstack()

    return monthly_trends

def create_season_trends(df):
    df['weathersit'] = pd.Categorical(
        df['weathersit'],
        categories=["Clear", "Mist", "Light Rain/Snow", "Heavy Rain/Snow"],
        ordered=True
    )
    df['season'] = pd.Categorical(
        df['season'],
        categories=["Spring", "Summer", "Fall", "Winter"],
        ordered=True
    )
    season_trends = df.groupby([
        'season',
        'weathersit'
    ], observed=True)['count'].mean().unstack()
    
    return season_trends

def create_user_type_patterns(df):
    df['weekday'] = pd.Categorical(
        df['weekday'],
        categories=["Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"
        ],
        ordered=True
    )
    user_type_patterns = df.groupby([
        'weekday',
        'workingday'
    ], observed=True)[['casual', 'registered']].mean().reset_index()
    
    return user_type_patterns

def create_hourly_patterns(df):
    hourly_patterns = df.groupby([
        'hour',
        'workingday'
    ], observed=True)['count'].mean().unstack()
    
    return hourly_patterns

def create_weather_user(df):
    df['weathersit'] = pd.Categorical(
        df['weathersit'],
        categories=["Clear", "Mist", "Light Rain/Snow", "Heavy Rain/Snow"],
        ordered=True
    )
    weather_user = df.groupby('weathersit', observed=True)[[
        'casual',
        'registered'
    ]].mean()
    
    return weather_user

def create_env_categories(df):
    df['temp_category'] = pd.Categorical(
        df['temp_category'],
        categories=["Very Cold", "Cold", "Comfortable", "Hot"],
        ordered=True
    )
    df['atemp_category'] = pd.Categorical(
        df['atemp_category'],
        categories=["Very Cold", "Cold", "Comfortable", "Hot"],
        ordered=True
    )
    df['humidity_category'] = pd.Categorical(
        df['humidity_category'],
        categories=["Dry", "Moderate", "Humid", "Very Humid"],
        ordered=True
    )
    df['windspeed_category'] = pd.Categorical(
        df['windspeed_category'],
        categories=["Calm", "Breezy", "Windy", "Very Windy"],
        ordered=True
    )
    temp_categories = df.groupby('temp_category', observed=True)['count'].mean().reset_index()
    atemp_categories = df.groupby('atemp_category', observed=True)['count'].mean().reset_index()
    humidity_categories = df.groupby('humidity_category', observed=True)['count'].mean().reset_index()
    windspeed_categories = df.groupby('windspeed_category', observed=True)['count'].mean().reset_index()
    
    return temp_categories, atemp_categories, humidity_categories, windspeed_categories

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    # Daily dataset
    day_df = pd.read_csv('https://raw.githubusercontent.com/Mofasir/bike-sharing-analysis/refs/heads/main/dashboard/clean_day.csv')
    day_df['date'] = pd.to_datetime(day_df['date'])
    
    # Hourly dataset
    hour_df = pd.read_csv('https://raw.githubusercontent.com/Mofasir/bike-sharing-analysis/refs/heads/main/dashboard/clean_hour.csv')
    hour_df['date'] = pd.to_datetime(hour_df['date'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar filters
st.sidebar.title('Filters')

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min(day_df['date'].min(), hour_df['date'].min()), max(day_df['date'].max(), hour_df['date'].max())],
    min_value=min(day_df['date'].min(), hour_df['date'].min()),
    max_value=max(day_df['date'].max(), hour_df['date'].max())
)

# Developer information
st.sidebar.markdown("""---""", unsafe_allow_html=True)
st.sidebar.markdown("### Connect with me!")
st.sidebar.link_button("My Github Profile", "https://github.com/mofasir")
st.sidebar.link_button("My Linkedin Profile", "https://www.linkedin.com/in/faikarnatsir")
st.sidebar.markdown("""
    <div style="display: flex; align-items: center; font-size: 15px;">
        &copy 2024 Mofasir. All Rights Reserved.
    </div>
""", unsafe_allow_html=True
)

# Apply filters
day_mask = (day_df['date'].dt.date >= date_range[0]) & (day_df['date'].dt.date <= date_range[1])
hour_mask = (hour_df['date'].dt.date >= date_range[0]) & (hour_df['date'].dt.date <= date_range[1])
filter_day_df = day_df[day_mask]
filter_hour_df = hour_df[hour_mask]

monthly_trends = create_monthly_trends(filter_day_df)
season_trends = create_season_trends(filter_hour_df)
user_type_patterns = create_user_type_patterns(filter_day_df)
hourly_patterns = create_hourly_patterns(filter_hour_df)
weather_user = create_weather_user(filter_hour_df)
temp_categories, atemp_categories, humidity_categories, windspeed_categories = create_env_categories(filter_day_df)

# Main dashboard
st.title('🚲 Bike Sharing Analysis Dashboard')

# Key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Rentals", f"{filter_day_df['count'].sum():,}")
with col2:
    st.metric("Casual Users", f"{filter_day_df['casual'].sum():,}")
with col3:
    st.metric("Registered Users", f"{filter_day_df['registered'].sum():,}")
with col4:
    st.metric("Average Daily Rentals", f"{filter_day_df['count'].mean():.0f}")

# Monthly rental trends
st.subheader("Monthly Rental Trends (2011 vs 2012)")
fig_monthly = go.Figure()
if 2011 in monthly_trends.index:
    fig_monthly.add_trace(go.Scatter(
        x=monthly_trends.columns,
        y=monthly_trends.loc[2011],
        name='2011',
        mode='lines+markers',
        line=dict(color='#1F77B4'),
        marker=dict(color='#1F77B4')
    ))   
if 2012 in monthly_trends.index:
    fig_monthly.add_trace(go.Scatter(
        x=monthly_trends.columns,
        y=monthly_trends.loc[2012],
        name='2012',
        mode='lines+markers',
        line=dict(color='#FF7F0E'),
        marker=dict(color='#FF7F0E')
    ))
fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Rentals",
    xaxis=dict(tickmode='array', tickvals=monthly_trends.columns, title='Month'),
    hovermode='x'
)
st.plotly_chart(fig_monthly, use_container_width=True)

# Average rentals by season and weather situation
st.subheader("Average Rentals by Season and Weather Situation")
fig_season_weather = go.Figure(data=[
    go.Bar(name=season, x=season_trends.index, y=season_trends[season])
    for season in season_trends.columns
])
fig_season_weather.update_layout(
    barmode='group',
    xaxis_title="Season",
    yaxis_title="Average Rentals",
    legend_title_text='Weather Situation'
)
st.plotly_chart(fig_season_weather, use_container_width=True)

# Average rentals by user type on workdays and weekends/holidays
st.subheader("Average Rentals by User Type on Workdays and Weekends/Holidays")
workdays_data = user_type_patterns[user_type_patterns["workingday"] == 1]
weekends_data = user_type_patterns[user_type_patterns["workingday"] == 0]
col1, col2 = st.columns(2)
with col1: 
    fig_user_workdays = px.bar(
        workdays_data,
        x='weekday',
        y=['casual', 'registered'],
        barmode='group',
        title="Average Rentals by User Type on Workdays",
        labels={'value': 'Average Rentals', 'variable': 'User Type', 'weekday': 'Day of Week'},
        color_discrete_sequence=px.colors.qualitative.D3
    )
    fig_user_workdays.update_layout(
        showlegend=False,
        yaxis=dict(range=[0,5000])
    )
    st.plotly_chart(fig_user_workdays, use_container_width=True)
with col2: 
    fig_user_weekends = px.bar(
        weekends_data,
        x='weekday',
        y=['casual', 'registered'],
        barmode='group',
        title="Average Rentals by User Type on Weekends/Holidays",
        labels={'value': '', 'variable': 'User Type', 'weekday': 'Day of Week'},
        color_discrete_sequence=px.colors.qualitative.D3
    )
    fig_user_weekends.update_layout(
        yaxis_title=None,
        yaxis=dict(range=[0,5000])
    )
    st.plotly_chart(fig_user_weekends, use_container_width=True)

# Hourly patterns
st.subheader("Hourly Rental Patterns (Workday vs Weekend)")
fig_hourly = go.Figure()
fig_hourly.add_trace(go.Scatter(
    x=hourly_patterns.index,
    y=hourly_patterns[0],
    name='Weekend',
    mode='lines+markers',
    line=dict(color='#1F77B4'),
    marker=dict(color='#1F77B4')
))
fig_hourly.add_trace(go.Scatter(
    x=hourly_patterns.index,
    y=hourly_patterns[1],
    name='Workday',
    mode='lines+markers',
    line=dict(color='#FF7F0E'),
    marker=dict(color='#FF7F0E')
))
fig_hourly.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Average Rentals",
    hovermode='x'
)
st.plotly_chart(fig_hourly, use_container_width=True)

# Weather and user type analysis
st.subheader("Average Rentals by Weather and User Type")
fig_weather = go.Figure(data=[
    go.Bar(
        name='Casual', 
        x=weather_user.index, 
        y=weather_user['casual'], 
        marker=dict(color='#1F77B4')
    ),
    go.Bar(
        name='Registered', 
        x=weather_user.index, 
        y=weather_user['registered'],
        marker=dict(color='#FF7F0E')
    )
])
fig_weather.update_layout(
    barmode='group',
    xaxis_title="Weather Situation",
    yaxis_title="Average Rentals"
)
st.plotly_chart(fig_weather, use_container_width=True)

st.subheader("Impact of Environmental Factors")
col1, col2 = st.columns(2)
with col1:
    # Temperature impact
    fig_temp = px.bar(
        temp_categories,
        x='temp_category',
        y='count',
        title='Average Rentals by Temperature',
        color='temp_category',
        color_discrete_sequence=['#0068C9', '#83C9FF', '#FFABAB', '#FF2B2B'],
        labels={'count': 'Average Rentals', 'temp_category': 'Temperature Category'}
    )
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Humidity impact
    fig_humidity = px.bar(
        humidity_categories,
        x='humidity_category',
        y='count',
        title='Average Rentals by Humidity',
        color='humidity_category',
        color_discrete_sequence=px.colors.sequential.haline,
        labels={'count': 'Average Rentals', 'humidity_category': 'Humidity Category'}
    )
    st.plotly_chart(fig_humidity, use_container_width=True)
with col2:
    # Felt Temperature impact
    fig_atemp = px.bar(
        atemp_categories,
        x='atemp_category',
        y='count',
        title='Average Rentals by Felt Temperature',
        color='atemp_category',
        color_discrete_sequence=['#0068C9', '#83C9FF', '#FFABAB', '#FF2B2B'],
        labels={'count': '', 'atemp_category': 'Felt Temperature Category'}
    )
    st.plotly_chart(fig_atemp, use_container_width=True)
    
    # Wind Speed impact
    fig_windspeed = px.bar(
        windspeed_categories,
        x='windspeed_category',
        y='count',
        title='Average Rentals by Wind Speed',
        color='windspeed_category',
        color_discrete_sequence=px.colors.sequential.Emrld,
        labels={'count': '', 'windspeed_category': 'Wind Speed Category'}
    )
    st.plotly_chart(fig_windspeed, use_container_width=True)
