import joblib
import os
import pytest

@pytest.fixture(scope="session")
def loaded_model():
    model_path = "churn_rf_simple.pkl"
    assert os.path.exists(model_path), f" {model_path} not found in repo root"
    artifact = joblib.load(model_path)
    return artifact
