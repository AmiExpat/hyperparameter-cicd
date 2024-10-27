import joblib
import json
from sklearn.metrics import mean_squared_error

def load_metrics(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def compare_models():
    # Load old and new model metrics
    old_metrics = load_metrics('artifacts/old_model_metrics.json')
    new_metrics = load_metrics('artifacts/new_model_metrics.json')

    if new_metrics['mse'] < old_metrics['mse']:
        print("New model outperforms the old one. Deploying...")
        return True
    else:
        print("New model did not outperform the old one.")
        return False

if __name__ == "__main__":
    result = compare_models()
    if not result:
        raise Exception("New model did not outperform the old one.")
