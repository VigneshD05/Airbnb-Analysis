
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

# MongoDB Atlas connection string
connection_string = "mongodb+srv://vigneshd:Tn12*au8950@vignesh.ruekie1.mongodb.net/?retryWrites=true&w=majority&appName=vignesh"

# Create a new client and connect to the server
client = MongoClient(connection_string, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Access your database and collection
db = client["sample_airbnb"]
collection = db["listingsAndReviews"]

# Retrieve data from MongoDB and convert it to a Pandas DataFrame
data = list(collection.find({}))
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
df.to_csv("mongodb_data.csv", index=False)

print("Data downloaded and saved successfully as 'mongodb_data.csv'.")



