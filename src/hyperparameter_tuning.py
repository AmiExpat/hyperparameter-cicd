# src/hyperparameter_tuning.py
import os
import sys
import json
from src.train import train_model
import joblib
import pandas as pd

def main():
    # Read hyperparameters from environment variables
    params = {
        'n_estimators': int(os.environ.get('N_ESTIMATORS', 100)),
        'max_depth': int(os.environ.get('MAX_DEPTH', 3)),
        'learning_rate': float(os.environ.get('LEARNING_RATE', 0.1)),
        'subsample': float(os.environ.get('SUBSAMPLE', 1.0)),
    }

    model, mse = train_model(params)
    print(f"Parameters: {params}")
    print(f"MSE: {mse}")

    # Save the model and metrics
    os.makedirs('/app/models', exist_ok=True)
    os.makedirs('/app/artifacts', exist_ok=True)

    # Save model
    model_filename = f"model_n{params['n_estimators']}_d{params['max_depth']}_lr{params['learning_rate']}_ss{params['subsample']}.joblib"
    model_path = os.path.join('/app/models', model_filename)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    # Save metrics
    metrics = {
        'params': params,
        'mse': mse,
    }
    metrics_path = os.path.join('/app/artifacts', f"metrics_{model_filename.replace('.joblib', '.json')}")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)
    print(f"Metrics saved to {metrics_path}")

if __name__ == "__main__":
    main()
