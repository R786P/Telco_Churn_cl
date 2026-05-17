import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np

def clean_churn_data(df):
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna(subset=["TotalCharges", "MonthlyCharges"])
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = df.drop(columns=["customerID"])
    return df.reset_index(drop=True)

def test_clean_churn_data_removes_customer_id():
    df = pd.DataFrame({"customerID": ["001"], "TotalCharges": ["50"], "MonthlyCharges": [50], "Churn": ["No"]})
    cleaned = clean_churn_data(df)
    assert "customerID" not in cleaned.columns

def test_clean_churn_data_encodes_churn():
    df = pd.DataFrame({"customerID": ["001"], "TotalCharges": ["50"], "MonthlyCharges": [50], "Churn": ["Yes"]})
    cleaned = clean_churn_data(df)
    assert cleaned["Churn"].iloc[0] == 1

def test_clean_churn_data_handles_invalid_charges():
    df = pd.DataFrame({"customerID": ["001"], "TotalCharges": [" "], "MonthlyCharges": [50], "Churn": ["No"]})
    cleaned = clean_churn_data(df)
    assert len(cleaned) == 0  # Invalid TotalCharges -> dropna -> empty
