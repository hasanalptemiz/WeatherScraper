from typing import List
from pydantic import BaseModel
from datetime import datetime

class SingleWeatherData(BaseModel):
    date: datetime
    day_temperature: float
    night_temperature: float

class WeatherInsertionData(BaseModel):
    provincial_plate: str
    date: datetime
    weather: dict

