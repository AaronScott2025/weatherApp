#Weather Application

Overview:

This project is a weather application built using Python's Tkinter library for the graphical user interface (GUI) and Open Meteo API for weather data. It allows users to input a city, retrieve current weather conditions and a 5-day forecast, and displays the information in a user-friendly interface. The application also handles errors and provides a default location if the user's location cannot be determined.

Features:

-Current Weather: Displays temperature, wind speed, and weather conditions. -5-Day Forecast: Shows daily weather conditions, including temperature ranges and weather icons. -Dynamic UI: Changes the UI color scheme based on the time of day. -Error Handling: Handles invalid inputs and API errors gracefully.

Prerequisites: -Python 3.x -Required Python packages: -tkinter (comes with Python standard library) -requests -requests_cache -pandas -geopy -openmeteo_requests (custom library for Open Meteo API) -retry_requests (custom library for retrying requests)
