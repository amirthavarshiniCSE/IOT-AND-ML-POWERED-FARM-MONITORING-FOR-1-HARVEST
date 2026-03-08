import requests
import time
import csv
import json
from datetime import datetime

TOKEN = "BMMdpSQNtaxnS_XMk7vfO6Ju6XkLg8ZJ"

url_ph = f"https://blynk.cloud/external/api/get?token={TOKEN}&v0"
url_Nvalue = f"https://blynk.cloud/external/api/get?token={TOKEN}&v1"
url_Pvalue = f"https://blynk.cloud/external/api/get?token={TOKEN}&v2"
url_Kvalue = f"https://blynk.cloud/external/api/get?token={TOKEN}&v3"
url_dustvalue = f"https://blynk.cloud/external/api/get?token={TOKEN}&v4"


# CSV Header
with open("sensor_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time","pH","Nitrogen","Phosphorous","Potassium","Dust","Moisture"])


while True:

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fetch values
    ph = float(requests.get(url_ph).text)
    Nvalue = float(requests.get(url_Nvalue).text)
    Pvalue = float(requests.get(url_Pvalue).text)
    Kvalue = float(requests.get(url_Kvalue).text)
    dustvalue = float(requests.get(url_dustvalue).text)

    # -------- Moisture Prediction Logic --------
    moisture = (
        40
        + (Nvalue * 0.10)
        + (Pvalue * 0.05)
        + (Kvalue * 0.05)
        - (dustvalue * 0.08)
        - (abs(ph - 7) * 2)
    )

    # limit range
    if moisture < 5:
        moisture = 5
    if moisture > 95:
        moisture = 95

    moisture = round(moisture, 2)

    # Print output
    print("Time:", time_now)
    print("pH:", ph)
    print("Nitrogen:", Nvalue)
    print("Phosphorous:", Pvalue)
    print("Potassium:", Kvalue)
    print("Dust:", dustvalue)
    print("Moisture:", moisture, "%")
    print("----------------------------------")

    # ---------- Save to CSV ----------
    with open("sensor_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time_now, ph, Nvalue, Pvalue, Kvalue, dustvalue, moisture])

    # ---------- Save to JSON ----------
    data = {
        "time": time_now,
        "pH": ph,
        "Nitrogen": Nvalue,
        "Phosphorous": Pvalue,
        "Potassium": Kvalue,
        "Dust": dustvalue,
        "Predicted_Moisture": moisture
    }

    with open("sensor_data.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

    time.sleep(5)