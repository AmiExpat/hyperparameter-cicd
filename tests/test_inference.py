import pytest
from src.inference import predict

def test_predict():
    # Sample input for the inference model
    sample_input = [-122.23, 37.88, 41, 880, 129, 322, 126, 8.3252]

    # Call the prediction function
    prediction = predict(sample_input)

    # Check if the prediction is a list
    assert isinstance(prediction, list)

    # Check if prediction contains a float value
    assert isinstance(prediction[0], float)
