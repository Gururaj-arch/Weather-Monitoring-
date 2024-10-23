import requests
import sqlite3
import os
import time
import schedule
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Constants
API_KEY = "99966e8a22f83a428865d92e6c829433"  # Your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITIES = ["Mumbai", "Chennai", "Bangalore"]
DATABASE = "weather_data.db"
ALERT_THRESHOLD = 35  # Example threshold

# Global variable to store latest weather data
latest_weather_data = {}

# Database Functions
def create_connection(db_file):
    """Create a database connection."""
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    """Create the daily_weather table if it does not exist."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_weather (
            date TEXT PRIMARY KEY,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')
    conn.commit()

def insert_daily_summary(conn, date, avg_temp, max_temp, min_temp, dominant_condition):
    """Insert or replace daily weather summary in the database."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO daily_weather (date, avg_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()

# Weather API Function
def get_weather_data(city):
    """Fetch weather data for a given city from OpenWeatherMap."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Get temperature in Celsius
    }
    response = requests.get(BASE_URL, params=params)
    
    # Check response status
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {city}: {response.status_code} - {response.text}")
        return None

# Alert Class
class WeatherAlert:
    def __init__(self, temperature_threshold):
        self.temperature_threshold = temperature_threshold

    def check_alert(self, current_temp):
        """Check if the current temperature exceeds the threshold."""
        if current_temp > self.temperature_threshold:
            print(f"Alert! Current temperature {current_temp}°C exceeds the threshold of {self.temperature_threshold}°C.")

# Visualization Function
def visualize_data(db_file):
    """Visualize daily weather summaries from the database."""
    conn = create_connection(db_file)
    df = pd.read_sql_query("SELECT * FROM daily_weather", conn)
    conn.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['avg_temp'], label='Average Temperature', marker='o')
    plt.plot(df['date'], df['max_temp'], label='Max Temperature', marker='o')
    plt.plot(df['date'], df['min_temp'], label='Min Temperature', marker='o')
    plt.xticks(rotation=45)
    plt.title('Daily Weather Summary')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Print Weather Data Function
def print_weather_data():
    """Print the latest weather data for each city."""
    print("Latest Weather Data:")
    for city, data in latest_weather_data.items():
        if data:
            temp = data['main']['temp']
            condition = data['weather'][0]['main']
            print(f"{city}: {temp}°C, Condition: {condition}")
        else:
            print(f"{city}: No data available.")

# Main Function
def fetch_and_process_weather():
    """Fetch weather data and process it for each city."""
    daily_data = {}
    
    for city in CITIES:
        data = get_weather_data(city)
        latest_weather_data[city] = data  # Store latest data for printing
        if data:
            current_temp = data['main']['temp']
            weather_condition = data['weather'][0]['main']
            
            date = datetime.now().strftime('%Y-%m-%d')
            daily_data.setdefault(date, []).append((current_temp, weather_condition))
            
            # Check alerts
            alert_system.check_alert(current_temp)

    # Roll up daily data
    for date, records in daily_data.items():
        avg_temp = sum(record[0] for record in records) / len(records)
        max_temp = max(record[0] for record in records)
        min_temp = min(record[0] for record in records)
        dominant_condition = max(set(record[1] for record in records), key=records.count)
        
        insert_daily_summary(conn, date, avg_temp, max_temp, min_temp, dominant_condition)

# Initialize database and alert system
conn = create_connection(DATABASE)
create_table(conn)
alert_system = WeatherAlert(ALERT_THRESHOLD)

# Schedule the weather fetching every 20 seconds
schedule.every(20).seconds.do(fetch_and_process_weather)

# Schedule printing of latest weather data every 15 seconds
schedule.every(15).seconds.do(print_weather_data)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the weather monitoring.")
finally:
    conn.close()
    visualize_data(DATABASE)
