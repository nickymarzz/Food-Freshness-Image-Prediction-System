"""
training_pipeline.py

Orchestrates the full training workflow:
  1. DataIngestion   – validates raw data and generates metadata
  2. DataTransformation – splits and preprocesses images
  3. ModelTrainer    – trains the freshness (Fresh/Rotten) model
  4. CategoryModelTrainer – trains the category (fruit/vegetable type) model
"""

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.category_trainer import CategoryModelTrainer


def run_training_pipeline(check_integrity: bool = False) -> None:
    """Run the end-to-end training pipeline."""

    print("=" * 60)
    print("STEP 1 – Data Ingestion")
    print("=" * 60)
    ingestion = DataIngestion()
    ingestion.initiate_data_ingestion(check_integrity=check_integrity)

    print("=" * 60)
    print("STEP 2 – Data Transformation (freshness split)")
    print("=" * 60)
    transformation = DataTransformation()
    transformation.transform_dataset_pipeline()

    print("=" * 60)
    print("STEP 3 – Freshness Model Training")
    print("=" * 60)
    trainer = ModelTrainer()
    trainer.model_trainer()

    print("=" * 60)
    print("STEP 4 – Category Classifier Training")
    print("=" * 60)
    cat_trainer = CategoryModelTrainer()
    cat_trainer.model_trainer()

    print("=" * 60)
    print("TRAINING PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_training_pipeline(check_integrity=True)
