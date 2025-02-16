from datetime import datetime,timedelta
import requests
import random

import sys,os
# 动态添加项目根目录到 sys.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MyCache import cacheFunc
from MyLogger import logger
API_KEY='213ede5029f2a898fa692dfc1bb718a4'
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"



@cacheFunc
def get_n_day_weather_forecast(city: str, n_days: int,units: str = "metric"):
    """
    获取指定城市的最近 N 天天气预报。

    :param city: 城市名称
    :param n_days: 预测天数
    :param units: 温度单位，可选值为 "metric"（摄氏度）或 "imperial"（华氏度）
    :return: 天气预报列表
    """
    
    city_location = next(filter(lambda c: c['name'] in city,city_locations),None)
    if city_location is None:
        raise ValueError(f"无法找到城市: '{city}'。")
    # 构建请求参数
    params = {
        "lat": city_location['lat'],
        "lon": city_location['lon'],
        "appid": API_KEY,
        "units": units,
        #"cnt": n_days * 8  # 每天有8个时间点的预报
        "cnt": n_days * 8 
    }
    try:
        logger.debug("get_n_day_weather_forecast send >>>>>>>>>>>>>>>> ： ")
        logger.debug(f"params:{params}")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.debug("get_n_day_weather_forecast receive >>>>>>>>>>>>>>>> ： ")
        #logger.debug(data)
        weather_forecast = []

        filterList = []
        i=0
        dateVar = datetime.now().date()
        for entry in data["list"]:
            _date = datetime.fromtimestamp(entry["dt"]).date()
            if dateVar == _date:
                filterList.append(entry)
                dateVar = dateVar + timedelta(days=1)

        for entry in filterList:
            date_time = str(datetime.fromtimestamp(entry["dt"]).date())
            temperature = entry["main"]["temp"] 
            description = entry["weather"][0]["description"]
            weather_forecast.append({
                "date_time": date_time,
                "temperature": temperature,
                "description": description
            })
        logger.debug("get_n_day_weather_forecast return >>>>>>>>>>>>>>>> ： ")
        logger.debug(weather_forecast)
        return weather_forecast
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    
def get_n_day_weather_forecast_mock(city: str, n_days: int,units: str = "metric"):
    today = datetime.now().date()
    return [{'date_time': str(today + timedelta(days=i)), 'temperature': random.randint(10, 20), 'description': 'few clouds'} for i in range(n_days)]

city_locations = [
    {
    "name":"深圳",
    "lat":22.5445741,
    "lon":114.0545429
    },

    {
    "name":"杭州",
    "lat":30.2489634,
    "lon":120.2052342
    },
    {
    "name":"北京",
    "lat":39.906217,
    "lon":116.3912757
    },
    {
    "name":"上海",
    "lat":31.2322758,
    "lon":121.4692071
    }
]    

if __name__ == "__main__":
    logger.debug(get_n_day_weather_forecast_mock("杭州",2))