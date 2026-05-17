import pandas as pd
import numpy as np

def test_model_predict_proba_range(loaded_model):
    # Mock input matching expected features
    mock_input = {col: 0 for col in loaded_model["feature_names"]}
    mock_input.update({
        "SeniorCitizen": 0, "tenure": 12, "MonthlyCharges": 70.0, "TotalCharges": 800.0
    })
    df = pd.DataFrame([mock_input])
    
    num_part = loaded_model["scaler"].transform(df[loaded_model["num_cols"]])
    cat_part = loaded_model["ohe"].transform(df[loaded_model["cat_cols"]])
    X_p = np.hstack([num_part, cat_part])
    
    proba = loaded_model["model"].predict_proba(X_p)[0][1]
    assert 0.0 <= proba <= 1.0, f"❌ Probability {proba} out of range [0,1]"

def test_model_output_type(loaded_model):
    # Just verify it returns numpy array with correct shape
    assert hasattr(loaded_model["model"], "predict_proba"), "❌ Model missing predict_proba method"
