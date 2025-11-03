# 🌦 Weather API Monitoring Script

This project is a Python-based monitoring tool that periodically checks weather data for a specific city using the **OpenWeather API**.  
It logs weather information — including temperature, status codes, and API response status — into a local **SQLite database** for analysis.

---

## 🧠 Features

- 🌍 Fetches real-time weather data from the OpenWeather API  
- 🕒 Logs temperature, description, and API response status with timestamps  
- 🧱 Stores data in a local SQLite database (`weather-file.db`)  
- 🔁 Runs automatically at specified intervals  
- ⚠️ Handles network and API errors gracefully  
- 🔐 Uses `.env` file to securely store API keys  

---

## 🧩 Project Structure

	📂 Automated Weather Monitor/
	├── weather_monitor.py # Main Python script
	├── .env # Contains your API key (excluded from Git)
	├── .gitignore # Ensures .env and .db are not pushed
	├── weather-file.db # SQLite database (auto-created)
	└── README.md # Project documentation

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

	git clone https://github.com/yourusername/automated-weather-monitor.git
	cd automated weather monitor

### 2️⃣ Install Required Packages
	pip install requests python-dotenv

### 3️⃣ Create a .env File
	openweather_apikey=YOUR_API_KEY_HERE

## 🗄 Database

The script automatically creates an SQLite database named weather-file.db with the following schema:

	Column	      Type	        Description
	
	id	          INTEGER	      Auto-incrementing primary key
	
	timestamp	    TEXT	        When the request was made
	
	status_code	  INTEGER	      HTTP response code from API
	
	city	        TEXT	        City name (e.g., Abuja)
	
	temperature	  REAL	        Temperature in Celsius
	
	description	  TEXT	        Weather condition description

## 🚀 Running the Script

Run the monitor:

	python weather_monitor.py


By default, the script checks the API every 30 seconds.
You can change this interval in the monitor_loop() function:

monitor_loop(interval_seconds=3600)  # Check every hour

## 🔍 Viewing the Data

You can explore the stored weather logs using the SQLite command-line tool or a GUI like DB Browser for SQLite.

Example:

	sqlite3 weather-file.db
	SELECT * FROM weather;

## 🧰 .gitignore Setup

The .gitignore file ensures sensitive and unnecessary files are not pushed to GitHub:

	.env
	*.db
	__pycache__/
	venv/
	*.pyc
	.vscode/

## 🧯 Error Handling

The script handles:

Network errors

Invalid or missing API keys

JSON parsing errors

API downtime (with status code 0 in logs)

## 🏁 License

This project is open-source and available under the MIT License.

