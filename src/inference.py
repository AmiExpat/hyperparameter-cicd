# src/inference.py
import joblib
import os
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the best model
model_path = '/app/models/best_model.joblib'
model = joblib.load(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
