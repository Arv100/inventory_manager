from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from os import environ
from datetime import datetime

load_dotenv()

uri = environ.get('MONGODB_URI')

def client_connection():
    return MongoClient(uri, server_api=ServerApi('1'))

def main():
    with client_connection() as client:

        db = client['inventory_manager']
        inventory = db['inventory']

        insert_result = inventory.insert_one({
            "item_name" : "Milk",
            "item_price" : 24,
            "item_quantity" : 25,
            "item_brand" : 'Amul',
            "inserted_timestamp" : datetime.now()
        })

        print(insert_result.inserted_id)

        print(inventory.find_one())

if __name__ == '__main__':
    main()