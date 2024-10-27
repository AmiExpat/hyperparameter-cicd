# tests/test_train.py
import unittest
from src.train import train_model

class TestTrainModel(unittest.TestCase):
    def test_train_model(self):
        params = {
            'n_estimators': 10,
            'max_depth': 3,
            'learning_rate': 0.1,
            'subsample': 0.8
        }
        model, mse = train_model(params)
        self.assertIsNotNone(model)
        self.assertGreaterEqual(mse, 0)

if __name__ == '__main__':
    unittest.main()
