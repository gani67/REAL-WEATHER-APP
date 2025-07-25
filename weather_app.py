import streamlit as st
import requests
import datetime
import pytz
import matplotlib.pyplot as plt

# Your OpenWeatherMap API key
API_KEY = "64968385b259ad809d282552be1064e5"

# Temperature unit mapping
unit_map = {
    "Celsius (°C)": "metric",
    "Fahrenheit (°F)": "imperial"
}

icon_map = {
    "Rain": "🌧️",
    "Clouds": "☁️",
    "Clear": "☀️",
    "Snow": "❄️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Mist": "🌫️",
    "Smoke": "🌫️",
    "Haze": "🌫️",
    "Dust": "🌪️",
    "Fog": "🌁",
    "Sand": "🌪️",
    "Ash": "🌋",
    "Squall": "💨",
    "Tornado": "🌪️"
}

def get_weather_data(city, unit):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_forecast_data(city, unit):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units={unit}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

def format_sun_time(timestamp, timezone_offset):
    tz = datetime.timezone(datetime.timedelta(seconds=timezone_offset))
    return datetime.datetime.fromtimestamp(timestamp, tz).strftime("%H:%M")

def plot_forecast_chart(forecast_data, unit):
    temps = []
    dates = []
    for item in forecast_data["list"]:
        dt = datetime.datetime.fromtimestamp(item["dt"])
        temps.append(item["main"]["temp"])
        dates.append(dt.strftime("%d %b %H:%M"))

    plt.figure(figsize=(10, 4))
    plt.plot(dates, temps, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel("Date Time")
    plt.ylabel(f"Temp ({'°C' if unit == 'metric' else '°F'})")
    plt.title("5-Day Forecast")
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit App
st.title("🌍 Real-Time Weather App")

# User Inputs
city = st.text_input("Enter a city:", "New York")
unit_label = st.radio("Select temperature unit:", list(unit_map.keys()))
unit = unit_map[unit_label]

if city:
    weather = get_weather_data(city, unit)
    forecast = get_forecast_data(city, unit)

    if weather.get("cod") != 200:
        st.error(f"City not found: {weather.get('message')}")
    else:
        st.subheader(f"Current Weather in {city}")

        main = weather["weather"][0]["main"]
        icon = icon_map.get(main, "🌡️")

        st.markdown(f"**{main}** {icon}")
        st.write(f"**Temperature**: {weather['main']['temp']}°")
        st.write(f"**Humidity**: {weather['main']['humidity']}%")

        timezone_offset = weather["timezone"]
        sunrise = format_sun_time(weather["sys"]["sunrise"], timezone_offset)
        sunset = format_sun_time(weather["sys"]["sunset"], timezone_offset)

        st.write(f"**Sunrise**: {sunrise}")
        st.write(f"**Sunset**: {sunset}")

        st.subheader("📈 5-Day Forecast")
        plot_forecast_chart(forecast, unit)
