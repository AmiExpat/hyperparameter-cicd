# tests/test_inference.py
import unittest
import numpy as np
from src.inference import predict

class TestInference(unittest.TestCase):
    def test_predict(self):
        sample_input = np.array([[8.3252, 41.0, 6.984127, 1.02381, 322.0, 2.555556, 37.88, -122.23]])
        prediction = predict(sample_input)
        self.assertIsNotNone(prediction)
        self.assertEqual(len(prediction), 1)
        self.assertGreater(prediction[0], 0)

if __name__ == '__main__':
    unittest.main()
