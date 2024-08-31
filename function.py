import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
	"latitude": 69.3535,
	"longitude": 88.2027,
	"current": ["nitrogen_dioxide", "sulphur_dioxide", "ozone"],
	"forecast_days": 1
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_nitrogen_dioxide = current.Variables(0).Value()
current_sulphur_dioxide = current.Variables(1).Value()
current_ozone = current.Variables(2).Value()

print(f"Current time {current.Time()}")
print(f"Current nitrogen_dioxide {current_nitrogen_dioxide}")
print(f"Current sulphur_dioxide {current_sulphur_dioxide}")
print(f"Current ozone {current_ozone}")

if current_nitrogen_dioxide <= 40:
    print("Количество Диоксид озота является хорошим")
elif current_nitrogen_dioxide <= 90:
    print("Количество Диоксид озота является нормальным")
elif current_nitrogen_dioxide <= 120:
    print("Количество Диоксид озота является средним")
elif current_nitrogen_dioxide <= 230:
    print("Количество Диоксид озота является плохим")
elif current_nitrogen_dioxide <= 450:
    print("Количество Диоксид озота является очень плохим")   
elif current_nitrogen_dioxide <= 1000:
    print("Количество Диоксид озота является смертельным")   

if current_sulphur_dioxide <= 100:
    print("Количество Диоксида серы является хорошим")
elif current_sulphur_dioxide <= 200:
    print("Количество Диоксида серы является нормальным")
elif current_sulphur_dioxide <= 350:
    print("Количество Диоксида серы является средним")
elif current_sulphur_dioxide <= 500:
    print("Количество Диоксида серы является плохим")
elif current_sulphur_dioxide <= 750:
    print("Количество Диоксида серы является очень плохим")   
elif current_sulphur_dioxide <= 1250:
    print("Количество Диоксида серы является смертельным")   

if current_ozone <= 50:
    print("Количество Озона является хорошим")
elif current_ozone <= 100:
    print("Количество Озона является нормальным")
elif current_ozone <= 130:
    print("Количество Озона является средним")
elif current_ozone <= 240:
    print("Количество Озона является плохим")
elif current_ozone <= 380:
    print("Количество Озона является очень плохим")   
elif current_ozone <= 800:
    print("Количество Озона является смертельным")  


