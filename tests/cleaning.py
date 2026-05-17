import pandas as pd
import numpy as np

def clean_churn_data(df):
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna(subset=["TotalCharges", "MonthlyCharges"])
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = df.drop(columns=["customerID"])
    return df.reset_index(drop=True)

def test_clean_churn_data_shape():
    df = pd.DataFrame({
        "customerID": ["1", "2", "3"],
        "TotalCharges": ["100", "200", "300"],
        "MonthlyCharges": [50, 60, 70],
        "Churn": ["Yes", "No", "Yes"]
    })
    cleaned = clean_churn_data(df)
    assert cleaned.shape == (3, 3)

def test_clean_churn_data_churn_encoding():
    df = pd.DataFrame({
        "customerID": ["1", "2"],
        "TotalCharges": ["100", "200"],
        "MonthlyCharges": [50, 60],
        "Churn": ["Yes", "No"]
    })
    cleaned = clean_churn_data(df)
    assert list(cleaned["Churn"]) == [1, 0]

def test_clean_churn_data_customerid_removed():
    df = pd.DataFrame({
        "customerID": ["1", "2"],
        "TotalCharges": ["100", "200"],
        "MonthlyCharges": [50, 60],
        "Churn": ["Yes", "No"]
    })
    cleaned = clean_churn_data(df)
    assert "customerID" not in cleaned.columns
