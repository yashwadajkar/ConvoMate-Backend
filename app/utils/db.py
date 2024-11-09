# app/utils/db.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client.get_database("ConvoMate")  # Replace "ConvoMate" with your database name

# Function to get specific collections
def get_users_collection():
    return db["users"]

def get_documents_collection():
    return db["documents"]

def get_chat_history_collection():
    return db["chat_history"]

def get_analytics_collection():
    return db["analytics"]

def get_admin_logs_collection():
    return db["admin_logs"]

def get_settings_collection():
    return db["settings"]
