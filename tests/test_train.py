import os
import pytest
from src.train import train_model
from src.data_loader import load_data

def test_train_model():
    # Load data
    X, y = load_data()

    # Define simple hyperparameters for testing
    params = {
        'n_estimators': 10,
        'max_depth': 3,
        'learning_rate': 0.1,
        'subsample': 0.8
    }

    # Train model
    model, mse = train_model(params)

    # Check if model is not None
    assert model is not None

    # Check if MSE is a float value
    assert isinstance(mse, float)

    # Check if model file is saved
    model_file = 'models/test_model.joblib'
    assert os.path.exists(model_file)

    # Cleanup model file
    os.remove(model_file)
