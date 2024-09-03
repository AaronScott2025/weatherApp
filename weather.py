import openmeteo_requests
from geopy.geocoders import Nominatim
import requests_cache
import pandas as pd
from retry_requests import retry


def get_weather(location):
    if not location:
        print("Location is None, cannot fetch weather.")
        return None, None

    # Ensure location has latitude and longitude
    if not hasattr(location, 'latitude') or not hasattr(location, 'longitude'):
        print("Invalid location object.")
        return None, None

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": ["temperature_2m", "weather_code", "wind_speed_10m"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"]
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None

    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    try:
        # Current values
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_weather_code = current.Variables(1).Value()
        current_wind_speed_10m = current.Variables(2).Value()

        print(f"Current time {current.Time()}")
        print(f"Current temperature_2m {current_temperature_2m}")
        print(f"Current weather_code {current_weather_code}")
        print(f"Current wind_speed_10m {current_wind_speed_10m}")

        # Process daily data
        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )}
        daily_data["weather_code"] = daily_weather_code
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min

        daily_dataframe = pd.DataFrame(data=daily_data)
        print(daily_dataframe)

        return (current, daily_dataframe)
    except Exception as e:
        print(f"Error processing weather data: {e}")
        return None, None


def get_coords(city_name):
    geolocator = Nominatim(user_agent="WeatheringPYPROJ")
    try:
        location = geolocator.geocode(city_name)
        if location:
            print(f"Lat: {location.latitude}, Lon: {location.longitude}")
        else:
            print("Location not found.")
        return location
    except Exception as e:
        print(f"Error geocoding city: {e}")
        return None


def getCondition(currentWeather):
    try:
        CWeather = int(currentWeather.Variables(2).Value())
        print(CWeather)

        if CWeather == 0:
            Condition = "Sunny"
        elif 1 <= CWeather <= 3:
            Condition = "Cloudy"
        elif 4 <= CWeather <= 12 or 30 <= CWeather <= 35 or 40 <= CWeather <= 49:
            Condition = "Foggy"
        elif 13 <= CWeather <= 19 or 29 == CWeather or 91 <= CWeather <= 99:
            Condition = "Thunder"
        elif 20 <= CWeather <= 28 or 50 <= CWeather <= 69 or 80 <= CWeather <= 90:
            Condition = "Rainy"
        elif 36 <= CWeather <= 39 or 70 <= CWeather <= 79:
            Condition = "Snowy"
        else:
            Condition = "Sunny"

        filepath = "GUI Elements/" + Condition + ".png"
    except Exception as e:
        print(f"Error determining condition: {e}")
        Condition = "Sunny"
        filepath = "GUI Elements/" + Condition + ".png"

    return filepath, Condition


# if __name__ == "__main__":
#   location = get_coords("New York")
#    if location:
#        current, daily_dataframe = get_weather(location)
