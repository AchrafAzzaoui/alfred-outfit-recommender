from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather(city: str) -> dict:
    """
    This is a docstring that describes what the function does.
    """
    api_key = os.getenv('WEATHER_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&cnt=6&units=imperial'  # 6 * 3-hour intervals = 18 hours
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200:
        return {"error": data.get('message', 'Unable to fetch weather data')}

    weather_data = {
        "temperature": [],
        "precipitation": [],
        "wind": []
    }

    for entry in data['list']:
        temp = entry['main']['temp']
        precipitation = entry.get('rain', {}).get('3h', 0)  # precipitation in the last 3 hours
        wind = entry['wind']['speed']
        
        weather_data["temperature"].append(temp)
        weather_data["precipitation"].append(precipitation)
        weather_data["wind"].append(wind)

    return weather_data
    

if __name__ == "__main__":
    # Test the function
    print(get_weather("London"))