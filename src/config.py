import os


class Config:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DATA_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'data')
    RAW_DATA_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'data', 'raw')
    PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'data', 'processed')
    MODEL_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'models')
    RESULTS_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'results')

    METADATA_FILE = os.path.join(PROJECT_ROOT, 'artifacts', 'data', 'metadata.json')
    CATEGORY_NAMES = ['Fruits', 'Vegetables']
    FRUIT_NAMES = ['Apple', 'Banana', 'Mango', 'Orange', 'Strawberry']
    VEGETABLE_NAMES = ['Bellpepper', 'Carrot', 'Cucumber', 'Potato', 'Tomato']
    CLASS_NAMES = ['Fresh', 'Rotten']

    # API Server Configuration (Localhost default)
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_URL = os.getenv("API_URL", f"http://{API_HOST}:{API_PORT}")

    # Web Dashboard Configuration (Localhost default)
    WEB_HOST = os.getenv("WEB_HOST", "127.0.0.1")
    WEB_PORT = int(os.getenv("WEB_PORT", 7860))
    WEB_URL = os.getenv("WEB_URL", f"http://{WEB_HOST}:{WEB_PORT}")

    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "food_freshness_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "predictions")
