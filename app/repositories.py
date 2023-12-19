from pymongo import MongoClient
from bson import ObjectId


class WeatherRepository:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['hasanalp_temiz']
        self.collection = self.db['Weathers']
        
    def insert_data(self, data):
        try:
            data_to_insert = data.dict()
            self.collection.insert_one(data_to_insert)
            print(f"Data inserted successfully: {data_to_insert}")
        except Exception as e:
            print(f"Error during data insertion: {str(e)}")

    
    def get_city_data(self, data):
        try :
            result = self.collection.find({"provincial_plate":data})
            city_data = [self.convert_object_id_to_str(item) for item in result]
            return city_data
        except Exception as e:
            print(f"Error during data insertion: {str(e)}")

    def convert_object_id_to_str(self, item):
        if "_id" in item and isinstance(item["_id"], ObjectId):
            item["_id"] = str(item["_id"])
        return item

    def is_provincial_plate_exists(self, provincial_plate):
        return self.collection.find_one({"provincial_plate": provincial_plate}) is not None

    def is_data_exists_for_datetime(self, provincial_plate, datetime_value):
        return self.collection.find_one({
            "provincial_plate": provincial_plate,
            "date": datetime_value
        }) is not None

    def clear_collection(self):
        try:
           self.collection.delete_many({})
           print("Data inserted successfully.")
        except Exception as e:
            print(f"Error during data insertion: {str(e)}")
