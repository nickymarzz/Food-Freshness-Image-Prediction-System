import logging
from pathlib import Path
from src.config import Config
import tensorflow as tf 
from keras.callbacks import EarlyStopping
import json




class ModelTrainer:
    def __init__(self, config: Config = None):
        
        self.config = config or Config()
        self.processed_data_dir = Path(config.PROCESSED_DATA_DIR)
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        logger = logging.getLogger('ModelTrainer')
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        if not logger.hasHandlers():
            logger.addHandler(ch)
        return logger
    
    def load_data(self, img_size=(224, 224), batch_size=32):
        train_ds = tf.keras.utils.image_dataset_from_directory(
            self.processed_data_dir / "train",
            label_mode="int",
            image_size=img_size,
            batch_size=batch_size
        )
        val_ds = tf.keras.utils.image_dataset_from_directory(
            self.processed_data_dir / "val",
            label_mode="int",
            image_size=img_size,
            batch_size=batch_size
        )
        test_ds = tf.keras.utils.image_dataset_from_directory(
            self.processed_data_dir / "test",
            label_mode="int",
            image_size=img_size,
            batch_size=batch_size,
            shuffle=False
        )
        return train_ds, val_ds, test_ds
    
    def build_model(self, input_shape=(224, 224, 3), num_classes=2):
    
        base_model = tf.keras.applications.MobileNetV2(
            weights='imagenet',
            input_shape=input_shape,
            include_top=False
        )
        base_model.trainable = False  

        inputs = tf.keras.Input(shape=input_shape)
        x = base_model(inputs, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
        model = tf.keras.Model(inputs, outputs)

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
            loss='sparse_categorical_crossentropy',
            metrics=["accuracy"]
        )
        return model
    
    def train(self, model, train_ds, val_ds, epochs=50):
        
        normalization_layer = tf.keras.layers.Rescaling(1./255)
        train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
        val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
        
        early_stopping = EarlyStopping(
            monitor='val_loss',    
            patience=5,
            restore_best_weights=True
        )

        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[early_stopping]  
        )
    
        return history
    
    def save_model(self, model, filename="mobilenetv2_baseline.keras"):
        save_path = Path(Config.MODEL_DIR) / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)
        model.save(save_path)
        self.logger.info(f"Model saved to {save_path}")

    def save_metrics(self, history, filename="baseline_history.json"):
        save_path = Path(Config.MODEL_DIR) / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)
        metrics = {k: [float(v) for v in vals] for k, vals in history.history.items()}
        with open(save_path, "w") as f:
            json.dump(metrics, f, indent=4)
        self.logger.info(f"Training metrics saved to {save_path}")


    def model_trainer(self):
    
        train_ds, val_ds, test_ds = self.load_data()
    
        model = self.build_model(num_classes=2)
        
        history = self.train(model, train_ds, val_ds)
        
        self.save_model(model)
        self.save_metrics(history)
        self.logger.info("Baseline model training complete.")

if __name__ == "__main__":
    mt = ModelTrainer()
    mt.model_trainer()