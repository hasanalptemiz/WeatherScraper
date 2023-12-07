from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor
from app.repositories import WeatherRepository
from app.models import SingleWeatherData,WeatherInsertionData
from app.utils import convert_date_to_en, get_provincial_plate,get_havadurumux_links,get_random_user_agents

import requests


def scrape_and_insert_data(site_url,headers):
    try:
        response = requests.get(site_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        response = requests.get(site_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find Table
        table = soup.find('table', {'id': 'hor-minimalist-a'})

        weather_repository = WeatherRepository()

        # Get provincial plate
        provincial_plate = str(get_provincial_plate(site_url))
        # Empty list
        weekly_weather_data = []

        # Insert daily temperature data into the weekly_weather_data for 7 days.
        for row in table.find('tbody').find_all('tr')[:7]:  
            columns = row.find_all('td')
            date = columns[0].text.split(',')[0].strip()
            date = convert_date_to_en(date)
            day_temperature = float(columns[2].text.strip()[:-1])  # Remove temp sign
            night_temperature = float(columns[3].text.strip()[:-1])
            formatted_date = f"{date}"
            daily_data = SingleWeatherData(
                date=datetime.strptime(formatted_date, '%Y-%m-%d'), 
                day_temperature= day_temperature,
                night_temperature=night_temperature
            )
            weekly_weather_data.append(daily_data)
       
        # Insert daily temperature data into the Weather collection for each city.
        for daily_data in weekly_weather_data:
            provincial_plate_exists = weather_repository.is_provincial_plate_exists(provincial_plate)
            datetime_exists = weather_repository.is_data_exists_for_datetime(provincial_plate, daily_data.date)
            if not provincial_plate_exists or not datetime_exists:
                data_to_insert = WeatherInsertionData(
                    provincial_plate=provincial_plate,
                    date=daily_data.date,
                    weather={
                        'site1': {
                            'up': daily_data.day_temperature,
                            'down': daily_data.day_temperature
                            }
                        }
                    )
                weather_repository.insert_data(data=data_to_insert)
        return f"Data for {site_url} inserted successfully."
    except Exception as e:
        raise e
    


def multithread_scrape_and_insert():
    site_links = get_havadurumux_links()
    headers = get_random_user_agents()
    with ThreadPoolExecutor(max_workers=10) as executor:  
        futures = [executor.submit(scrape_and_insert_data, site_url ,headers) for site_url in site_links]
        for future in futures:
            future.result()



