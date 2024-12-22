from typing import Any

import requests
from pandas import DataFrame

from config import API_KEY
import pandas as pd
from datetime import datetime


def _get_location(lat, lon, api_key=API_KEY) -> Any | None:
    """Получает locationKey"""
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={lat},{lon}&language=ru-ru"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['Key']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")

        return None


def _get_weather_data(loc, api_key=API_KEY) -> DataFrame | None:
    """Получает данные о погоде"""
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{_get_location(loc[0], loc[1], api_key)}"
    params = {
            "apikey": API_KEY,
            "language": "ru-ru",
            "details": True,
            "metric": True
        }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        dates = []
        temperatures = []
        wind_speeds = []
        precip_probs = []
        humidities = []

        for day in data["DailyForecasts"]:
            dates.append(datetime.fromtimestamp(day["EpochDate"]).strftime('%Y-%m-%d'))
            temperatures.append(round((day["Temperature"]["Minimum"]["Value"] + day["Temperature"]["Maximum"]["Value"]) / 2, 1))
            wind_speeds.append(day["Day"]["Wind"]["Speed"]["Value"])
            precip_probs.append(day["Day"]["PrecipitationProbability"])
            humidities.append(
                round((day["Day"]["RelativeHumidity"]["Minimum"] + day["Day"]["RelativeHumidity"]["Maximum"]) / 2))

        return pd.DataFrame({
            "date": dates,
            "temperature": temperatures,
            "wind_speed": wind_speeds,
            "precip_prob": precip_probs,
            "humidities": humidities,
            "coordinates": f"{loc}"
        })

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def get_weather_data_sheet(coords_list, num_days) -> DataFrame:
    "Возвращает датасет данных о погоде на следующие 5 дней"
    all_data = []
    for cords in coords_list:
        df = _get_weather_data(cords)
        all_data.append(df.head(num_days))

    return pd.concat(all_data)










