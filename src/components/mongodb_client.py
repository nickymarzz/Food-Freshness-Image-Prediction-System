import pymongo
from datetime import datetime
from src.config import Config

class MongoDBClient:
    def __init__(self, uri=Config.MONGODB_URI, db_name=Config.DB_NAME, collection_name=Config.COLLECTION_NAME):
        """
        Initializes the MongoDB client.
        """
        try:
            self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Trigger a connection to verify
            self.client.server_info()
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"Successfully connected to MongoDB: {db_name}.{collection_name}")
        except Exception as e:
            print(f"Warning: Could not connect to MongoDB: {e}")
            self.client = None
            self.db = None
            self.collection = None

    def save_prediction(self, prediction_data):
        """
        Saves a prediction result to the database.
        """
        if self.collection is None:
            return None
        
        record = {
            "timestamp": datetime.utcnow(),
            "category": prediction_data.get("category", {}).get("label"),
            "category_score": float(prediction_data.get("category", {}).get("score", 0.0)),
            "freshness": prediction_data.get("freshness", {}).get("label"),
            "freshness_score": float(prediction_data.get("freshness", {}).get("score", 0.0)),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            result = self.collection.insert_one(record)
            return result.inserted_id
        except Exception as e:
            print(f"Error saving prediction to MongoDB: {e}")
            return None

    def get_history(self, limit=5):
        """
        Retrieves the most recent predictions from the database.
        """
        if self.collection is None:
            return []
        
        try:
            cursor = self.collection.find().sort("timestamp", pymongo.DESCENDING).limit(limit)
            history = []
            for doc in cursor:
                history.append({
                    "time": doc.get("timestamp").strftime("%H:%M:%S"),
                    "label": f"{doc.get('freshness')} {doc.get('category')}",
                    "freshness": doc.get("freshness")
                })
            return history
        except Exception as e:
            print(f"❌ Error fetching history from MongoDB: {e}")
            return []

if __name__ == "__main__":
    # Quick test
    client = MongoDBClient()
    if client.client:
        test_data = {
            "category": {"label": "Apple", "score": 0.99},
            "freshness": {"label": "Fresh", "score": 0.95}
        }
        inserted_id = client.save_prediction(test_data)
        print(f"Test prediction saved with ID: {inserted_id}")
        
        history = client.get_history(limit=1)
        print(f"Latest history: {history}")
