import requests
import redis
import json


api_key = ""
url = "https://api.openweathermap.org/data/2.5/weather"

choice = input("Do you want to know the weather(press Y or N): ")
while choice == "Y":
    if choice == "Y" or choice == "y":
        city_to_search = input("Enter City name : ")

        r = redis.Redis(host="localhost", port=6379, decode_responses=True)

        params = {"q": city_to_search, "appid": api_key, "units": "metric"}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather_condition = data["weather"][0]["description"]
            min_temp = data["main"]["temp_min"]
            max_temp = data["main"]["temp_max"]
            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            wind_degree = data["wind"]["deg"]
            wind_gust = data["wind"]["gust"]
            city_name = data["name"]

            weather_data = {
                "temp": temp,
                "weather_condition": weather_condition,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "pressure": pressure,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "wind_degree": wind_degree,
                "wind_gust": wind_gust,
            }

            r.set(city_name, json.dumps(weather_data))

            print(
                f"\t{city_name}\nTemperature is {temp} Celcius\nMinimum Temperature: {min_temp} Celcius\nMaximum Temperature: {max_temp} Celcius\nWeather condition is {weather_condition}\nPressure: {pressure}\nHumidity: {humidity}\nWind Speed: {wind_speed}\nWind Degree: {wind_degree}\nWind Gust: {wind_gust}\n"
            )
        elif response.status_code != 200:
            raw_data = r.get(params["q"])

            if raw_data == None:
                print("Service Down.\n")
            else:
                weather_redis_data = json.loads(raw_data)
                temp = weather_redis_data["temp"]
                weather_condition = weather_redis_data["weather_condition"]
                min_temp = weather_redis_data["min_temp"]
                max_temp = weather_redis_data["max_temp"]
                pressure = weather_redis_data["pressure"]
                humidity = weather_redis_data["humidity"]
                wind_speed = weather_redis_data["wind_speed"]
                wind_degree = weather_redis_data["wind_degree"]
                wind_gust = weather_redis_data["wind_gust"]
                city_name = params["q"]
                print(
                    f"\t{city_name}\nTemperature is {temp} Celcius\nMinimum Temperature: {min_temp} Celcius\nMaximum Temperature: {max_temp} Celcius\nWeather condition is {weather_condition}\nPressure: {pressure}\nHumidity: {humidity}\nWind Speed: {wind_speed}\nWind Degree: {wind_degree}\nWind Gust: {wind_gust}\n"
                )

        choice = input("Do you want to search for another city(Press Y or N): ")
