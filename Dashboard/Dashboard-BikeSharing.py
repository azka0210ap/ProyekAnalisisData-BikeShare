# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data
path_dataset1 = "/Data/Bike_Share.csv"
path_dataset2 = "/Data/Bike_Share_hour.csv"

df_day= pd.read_csv(path_dataset1)
df_hour= pd.read_csv(path_dataset1)

# Functions
def create_byseason_df(df):
    byseason_df = df.groupby(by='season').cnt.sum().sort_values(ascending=False).reset_index()
    return byseason_df

def create_monthly_counts_df(df):
    monthly_counts_df = df.groupby(by=['mnth','yr']).agg({
    'cnt': 'sum'
    }).reset_index()
    return monthly_counts_df

def create_byweather_df(df):
    byweather_df = df.groupby(by='weathersit').agg({
    'cnt': 'sum'
    })
    return byweather_df

def create_daily_share_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df

def create_daily_casual_df(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

def create_daily_registered_df(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by='holiday').agg({
    'cnt': ['mean']
    }).reset_index()
    return byholiday_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by='weekday').agg({
    'cnt': ['mean']
    }).reset_index()
    return byweekday_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by='workingday').agg({
    'cnt': ['mean']
    }).reset_index()
    return byworkingday_df

# Date Column
datetime_columns = ['dteday']
df_day.sort_values(by='dteday', inplace=True)
df_day.reset_index(inplace=True)   

df_hour.sort_values(by="dteday", inplace=True)
df_hour.reset_index(inplace=True)

for column in datetime_columns:
    df_day[column] = pd.to_datetime(df_day[column])
    df_hour[column] = pd.to_datetime(df_hour[column])

min_date_days = df_day['dteday'].min()
max_date_days = df_day['dteday'].max()

min_date_hour = df_hour['dteday'].min()
max_date_hour = df_hour['dteday'].max()

# Sidebar
st.sidebar.markdown("**Name: Aghnia Azka Privanna**")
st.sidebar.markdown("**Email: [azkaprivanna@gmail.com](azkaprivanna@gmail.com)**")
st.sidebar.markdown("**Dicoding: [aghniaazkap]**")

with st.sidebar:
    # Add Logo
    st.image("https://jugnoo.io/wp-content/uploads/2022/05/on-demand-bike-sharing-1-1024x506.jpg")
    # Retrieve start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_day = df_day[(df_day['dteday'] >= str(start_date)) & (df_day['dteday'] <= str(end_date))]
main_df_hour = df_hour[(df_hour['dteday'] >= str(start_date)) & (df_hour['dteday'] <= str(end_date))]

# Dataframe
daily_monthly_counts_df = create_monthly_counts_df(main_df_day)
daily_byweather_df = create_byweather_df(main_df_day)
daily_rent_df = create_daily_share_df(main_df_day)
daily_casual_rent_df = create_daily_casual_df(main_df_day)
daily_registered_rent_df = create_daily_registered_df(main_df_day)
daily_byholiday_df = create_byholiday_df(main_df_day)
daily_byweekday_df = create_byweekday_df(main_df_day)
daily_byworkingday_df = create_byworkingday_df(main_df_day)

# Dashboard
st.header('Bike Share Dashboard')
st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total User', value= daily_rent_total)

# Visualization
# Question 1 
st.subheader('Registered User vs Casual User')

labels = 'Casual', 'Registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=["#A52A2A", "#008B8B"])
ax1.axis('equal')  

st.pyplot(fig1)

# Question 2
st.subheader('Weatherly Rentals')

fig, ax = plt.subplots(figsize=(12, 9))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=daily_byweather_df.index,
    y=daily_byweather_df['cnt'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(daily_byweather_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Question 3
st.subheader('Weekday, Workingday, and Holiday Rentals')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,20))

data_list = [('workingday', 'Workingday'),
             ('holiday', 'Holiday'),
             ('weekday', 'Weeks')]

for i, (column, title) in enumerate(data_list):
    sns.barplot(
        x=column, y='cnt', data=df_day, ax=axes[i])
    axes[i].set_title(f'Bike Renter by {title}')
    axes[i].set_xlabel(title)
    axes[i].set_ylabel('Number of Bike Renters')

plt.tight_layout()
st.pyplot(fig)

# Question 4
st.subheader('Total Bicycles Rent')

fig, axes = plt.subplots(figsize=(10,5))

sns.lineplot(
    data=daily_monthly_counts_df,
    x='mnth',y='cnt',hue='yr',palette='viridis',marker='o')

plt.title('Total Bikes Rented by Month & Year')
plt.legend(title='Year', loc='upper right')
plt.tight_layout()
st.pyplot(fig)


