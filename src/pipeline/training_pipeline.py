"""
training_pipeline.py

Orchestrates the full end-to-end training and evaluation workflow:
  1. DataIngestion          – validates raw data and generates metadata
  2. DataTransformation     – splits and preprocesses produce images
  3. ModelTrainer           – trains the freshness (Fresh/Rotten) MobileNetV2 model
  4. CategoryModelTrainer   – trains the 10-class produce category classifier
  5. ModelEvaluation        – evaluates freshness classifier & generates metrics/curves
  6. CategoryModelEvaluation– evaluates category classifier & generates metrics/curves
"""

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.category_trainer import CategoryModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.category_model_evaluation import CategoryModelEvaluation


def run_training_pipeline(check_integrity: bool = False, evaluate: bool = True) -> None:
    """Run the end-to-end training and evaluation pipeline."""

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

    if evaluate:
        print("=" * 60)
        print("STEP 5 – Freshness Model Quantitative Evaluation")
        print("=" * 60)
        fresh_eval = ModelEvaluation()
        fresh_eval.model_eval()

        print("=" * 60)
        print("STEP 6 – Category Classifier Quantitative Evaluation")
        print("=" * 60)
        cat_eval = CategoryModelEvaluation()
        cat_eval.model_eval()

    print("=" * 60)
    print("END-TO-END PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_training_pipeline(check_integrity=True, evaluate=True)

