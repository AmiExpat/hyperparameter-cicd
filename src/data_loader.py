# src/data_loader.py
from sklearn.datasets import fetch_california_housing
import pandas as pd

def load_data():
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    X = df.drop('MedHouseVal', axis=1)
    y = df['MedHouseVal']
    return X, y
