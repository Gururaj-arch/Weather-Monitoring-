# Weather-Monitoring-
The primary goal of this project is to develop a real-time data processing system that monitors weather conditions across various metropolitan cities in India. The system retrieves weather data from the OpenWeatherMap API, processes it to provide summarized insights, and alerts users based on configurable thresholds. 
Real-Time Data Retrieval:

Continuously fetch weather data for predefined cities every 5 minutes.
Retrieve key weather parameters such as current temperature, perceived temperature, and main weather condition.
Data Processing and Analysis:

Convert temperature readings from Kelvin to Celsius.
Aggregate daily weather data to calculate:
Average temperature
Maximum temperature
Minimum temperature
Dominant weather condition based on frequency.
Alerting Mechanism:

User-configurable thresholds for temperature and specific weather conditions.
Trigger alerts if conditions exceed predefined thresholds (e.g., temperature exceeding 35°C for two consecutive updates).
Data Storage:

Store daily weather summaries in a SQLite database for historical reference and further analysis.
Data Visualization:

Visualize daily weather summaries and trends using Matplotlib, allowing users to analyze historical data easily.
User-Friendly:

Simple console output for alerts and weather summaries.
Capability to run indefinitely until interrupted, with visual output at the end of the session.
Architecture
Components:
API Integration: The system connects to the OpenWeatherMap API to fetch real-time weather data.
Database: SQLite is used to persist daily weather summaries and allow historical data retrieval.
Scheduler: The schedule library is utilized to execute data retrieval tasks at specified intervals.
Visualization: Matplotlib is used for visualizing the weather data, providing insights into temperature trends.
