import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
print("Loading environment variables from .env file...")
load_dotenv()

# Connect to MongoDB with SSL verification skipped
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    print("Error: MONGODB_URI is not set in the environment variables.")
else:
    try:
        print("Connecting to MongoDB with SSL verification skipped...")
        client = MongoClient(MONGODB_URI, tls=True, tlsAllowInvalidCertificates=True)
        db = client.get_database("ConvoMate")  # Replace with your actual database name
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit(1)  # Exit if the connection fails

def load_data(collection_name, json_file):
    print(f"\nLoading data from {json_file} into '{collection_name}' collection...")
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
        if collection_name in db.list_collection_names():
            print(f"Clearing existing data in '{collection_name}' collection...")
            db[collection_name].delete_many({})  # Clear existing data
        db[collection_name].insert_many(data)
        print(f"Successfully loaded data into '{collection_name}' collection.")
    except FileNotFoundError:
        print(f"Error: File {json_file} not found.")
    except Exception as e:
        print(f"An error occurred while loading data into '{collection_name}': {e}")

if __name__ == "__main__":
    # Define the path to the data directory accurately
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")  # Assuming "data" is directly inside the root "load_database" directory

    # Define collection file paths
    collections_files = {
        "users": os.path.join(data_dir, "users.json"),
        "documents": os.path.join(data_dir, "documents.json"),
        "chat_history": os.path.join(data_dir, "chat_history.json"),
        "analytics": os.path.join(data_dir, "analytics.json"),
        "admin_logs": os.path.join(data_dir, "admin_logs.json"),
        "settings": os.path.join(data_dir, "settings.json")
    }

    # Load data into each collection
    for collection, file_path in collections_files.items():
        load_data(collection, file_path)

    print("\nData loading process completed.")
