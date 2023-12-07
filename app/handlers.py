from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.repositories import WeatherRepository
from app.yaml_reader import yaml_provincial_parser,yaml_reader

router = APIRouter()

@router.post("/weathers/clean-collection/")
async def clear_collection_handler():
    try:
        weather_repository = WeatherRepository()
        weather_repository.clear_collection()
        return JSONResponse(content={"message": "Collection is cleared successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weathers/{city_name}")
async def get_city_weather_handler(city_name: str):
    try:
        city_name = city_name.capitalize()
        weather_repository = WeatherRepository()
        provincial_plates = yaml_provincial_parser(yaml_reader("provincials.yaml"))
        city_data = weather_repository.get_city_data(str(provincial_plates[city_name]))
        if not city_data:
            raise HTTPException(status_code=404, detail=f"No data found for {city_name} in the last 7 days")

        return city_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_router():

    return router

