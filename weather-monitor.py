import requests
import sqlite3
import os
import time
import argparse
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from datetime import datetime

# parser and argument
parser = argparse.ArgumentParser(description="Weather monitor script")
parser.add_argument("--city", type=str, default="Abuja", help="city name")
parser.add_argument("--interval", type=int, default=60, help="check interval in seconds")

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    'weather.log',
    maxBytes=50000,
    backupCount=20
)

file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Create the SQLite database and weather table if it doesn't already exist.
def database_setup():
    
    conn = sqlite3.connect('weather-file.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, status_code INTEGER, city TEXT, temperature REAL, description TEXT)")

    conn.commit()
    conn.close()

# Fetch current weather data from OpenWeather API
def check_api_status(city):
    # the env file and get the api key
    load_dotenv()
    api_key = os.getenv('openweather_apikey')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not api_key:
        logger.error("Missing OpenWeather API key in .env file.")
        return

    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        response.raise_for_status()
        data = response.json()

        weather_list = data.get('weather', [])
        description_value = weather_list[0].get('description') if weather_list else 'N/A'

        return {
            'timestamp': current_time,
            'status_code': response.status_code,
            'city': data.get('name'),
            'temperature': data.get('main', {}).get('temp'),
            'description': description_value
        }
    except requests.exceptions.RequestException as e:

        return {
            'timestamp': current_time,
            'status_code': 0, 'city': city,
            'temperature': None, 
            'description': f"Error: {str(e)}"
        }

# Insert a new weather record into the database
def log_data(log_record):
    
    conn = sqlite3.connect('weather-file.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO weather (timestamp, status_code, city, temperature, description)
    VALUES (?, ?, ?,?,?)
    ''', (log_record['timestamp'],
          log_record['status_code'],
          log_record['city'],
          log_record['temperature'],
          log_record['description']))

    conn.commit()
    conn.close()

# Orchestrates all components and runs API checks every <interval_seconds> seconds
def monitor_loop(city, interval_seconds=30):
    database_setup()

    logger.info(f"Monitoring started. Checking API every {interval_seconds} seconds.")

    while True:

        log_record = check_api_status(city)
        
        # Log the entire record (success or failure) to the database
        log_data(log_record)
        
        # Wait for the next check
        time.sleep(interval_seconds)
    

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        monitor_loop(args.city, args.interval)
    except KeyboardInterrupt:
        logger.info("\nAPI Monitoring stopped by user.")
    except Exception:
        logger.exception(f"\nAn unexpected fatal error occurred.")