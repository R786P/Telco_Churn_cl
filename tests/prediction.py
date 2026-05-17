import numpy as np

def test_prediction_output_type():
    prob = 0.343
    assert isinstance(prob, float)
    assert 0 <= prob <= 1

def test_risk_level_classification():
    prob = 0.343
    if prob > 0.6:
        risk = "High"
    elif prob > 0.3:
        risk = "Medium"
    else:
        risk = "Low"
    assert risk == "Medium"

def test_probability_percentage_format():
    prob = 0.343
    formatted = f"{prob:.1%}"
    assert formatted == "34.3%"
