import pandas as pd
import requests
import json

# WEATHER API
LAT = "38.462"
LON = "-99.903"
API_KEY = "83f927c25ed545d914c5e5207d0d8bb4"

weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

weather = requests.get(weather_url).json()

temperature = weather["list"][0]["main"]["temp"]
humidity = weather["list"][0]["main"]["humidity"]
rain_prob = weather["list"][0].get("pop",0) * 100

# READ SENSOR CSV
data = pd.read_csv("sensor_data.csv")
data.columns = data.columns.str.strip()

recommendations = []

for index,row in data.iterrows():

    ph = row["pH"]
    N = row["Nitrogen"]
    P = row["Phosphorous"]
    K = row["Potassium"]
    dust = row["Dust"]
    moisture = row["Moisture"]

    recommendation = "Normal conditions"

    # ---- Rain detection ----
    if rain_prob > 70:
        recommendation = "⚠ Heavy rain expected. Protect crops and stop irrigation."

    # ---- Sunny / Heat detection ----
    elif temperature > 32 and humidity < 40:
        recommendation = "☀ High temperature detected. Increase irrigation by 30%."

    # ---- Dry soil ----
    elif moisture < 25:
        recommendation = "⚠ Soil moisture low. Add irrigation."

    # ---- Dust anomaly ----
    elif dust > 250:
        recommendation = "⚠ Dust levels high. Soil may be dry."

    recommendations.append({
        "Time": row["Time"],
        "pH": ph,
        "Nitrogen": N,
        "Phosphorous": P,
        "Potassium": K,
        "Dust": dust,
        "Moisture": moisture,
        "Temperature": temperature,
        "RainProbability": rain_prob,
        "Recommendation": recommendation
    })

# SAVE FOR HTML
with open("recommendation.json","w") as f:
    json.dump(recommendations,f,indent=4)

print("Recommendations generated.")